/***************************************************************************
 *  tools/create_files.cpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2003 Roman Dementiev <dementiev@mpi-sb.mpg.de>
 *  Copyright (C) 2007 Andreas Beckmann <beckmann@mpi-inf.mpg.de>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#include <cstdio>
#include <iomanip>
#include <sstream>
#include <vector>

#include <tlx/cmdline_parser.hpp>
#include <tlx/logger.hpp>

#include <foxxll/common/aligned_alloc.hpp>
#include <foxxll/io.hpp>

#if !FOXXLL_WINDOWS
 #include <unistd.h>
#endif

using foxxll::request_ptr;
using foxxll::file;
using foxxll::timestamp;
using foxxll::external_size_type;

#ifdef BLOCK_ALIGN
 #undef BLOCK_ALIGN
#endif

#define BLOCK_ALIGN  4096

#define NOREAD

//#define DO_ONLY_READ

#define POLL_DELAY 1000

#define RAW_ACCESS

//#define WATCH_TIMES

#define CHECK_AFTER_READ 0

#ifdef WATCH_TIMES
void watch_times(request_ptr reqs[], unsigned n, double* out)
{
    bool* finished = new bool[n];
    unsigned count = 0;
    unsigned i = 0;
    for (i = 0; i < n; i++)
        finished[i] = false;

    while (count != n)
    {
        usleep(POLL_DELAY);
        i = 0;
        for (i = 0; i < n; i++)
        {
            if (!finished[i])
                if (reqs[i]->poll())
                {
                    finished[i] = true;
                    out[i] = timestamp();
                    count++;
                }
        }
    }
    delete[] finished;
}

void out_stat(double start, double end, double* times, unsigned n, const std::vector<std::string>& names)
{
    for (unsigned i = 0; i < n; i++)
    {
        LOG1 << i << " " << names[i] << " took " << 100. * (times[i] - start) / (end - start) << " %" << std::endl;
    }
}
#endif

#define MB (1024 * 1024)

int create_files(int argc, char* argv[])
{
    std::vector<std::string> disks_arr;
    external_size_type offset = 0, length;

    tlx::CmdlineParser cp;
    cp.add_param_bytes(
        "filesize", length,
        "Number of bytes to write to files."
    );
    cp.add_param_stringlist(
        "filename", disks_arr,
        "Paths to files to write."
    );

    if (!cp.process(argc, argv))
        return -1;

    external_size_type endpos = offset + length;

    for (size_t i = 0; i < disks_arr.size(); ++i)
    {
        unlink(disks_arr[i].c_str());
        LOG1 << "# Add disk: " << disks_arr[i];
    }

    const size_t ndisks = disks_arr.size();

#if FOXXLL_WINDOWS
    size_t buffer_size = 64 * MB;
#else
    size_t buffer_size = 256 * MB;
#endif
    const size_t buffer_size_int = buffer_size / sizeof(int);

    unsigned chunks = 2;
    const size_t chunk_size = buffer_size / chunks;
    const size_t chunk_size_int = chunk_size / sizeof(int);

    size_t i = 0, j = 0;

    auto* buffer = static_cast<int*>(foxxll::aligned_alloc<BLOCK_ALIGN>(buffer_size * ndisks));
    file** disks = new file*[ndisks];
    request_ptr* reqs = new request_ptr[ndisks * chunks];
#ifdef WATCH_TIMES
    double* r_finish_times = new double[ndisks];
    double* w_finish_times = new double[ndisks];
#endif

    for (i = 0; i < ndisks * buffer_size_int; i++)
        buffer[i] = static_cast<int>(i);

    for (i = 0; i < ndisks; i++)
    {
#if FOXXLL_WINDOWS
 #ifdef RAW_ACCESS
        disks[i] = new foxxll::wincall_file(
                disks_arr[i],
                file::CREAT | file::RDWR | file::DIRECT, static_cast<int>(i)
            );
 #else
        disks[i] = new foxxll::wincall_file(
                disks_arr[i],
                file::CREAT | file::RDWR, static_cast<int>(i)
            );
 #endif
#else
 #ifdef RAW_ACCESS
        disks[i] = new foxxll::syscall_file(
                disks_arr[i],
                file::CREAT | file::RDWR | file::DIRECT, static_cast<int>(i)
            );
 #else
        disks[i] = new foxxll::syscall_file(
                disks_arr[i],
                file::CREAT | file::RDWR, static_cast<int>(i)
            );
 #endif
#endif
    }

    while (offset < endpos)
    {
        std::stringstream ss;

        const size_t current_block_size =
            length
            ? static_cast<size_t>(std::min<external_size_type>(buffer_size, endpos - offset))
            : buffer_size;

        const size_t current_chunk_size = current_block_size / chunks;

        ss << "Disk offset " << std::setw(7) << offset / MB << " MiB: " << std::fixed;

        double begin = timestamp(), end;

#ifndef DO_ONLY_READ
        for (i = 0; i < ndisks; i++)
        {
            for (j = 0; j < chunks; j++)
                reqs[i * chunks + j] =
                    disks[i]->awrite(
                        buffer + buffer_size_int * i + j * chunk_size_int,
                        offset + j * current_chunk_size,
                        current_chunk_size
                    );
        }

 #ifdef WATCH_TIMES
        watch_times(reqs, ndisks, w_finish_times);
 #else
        wait_all(reqs, ndisks * chunks);
 #endif

        end = timestamp();

 #ifdef WATCH_TIMES
        out_stat(begin, end, w_finish_times, ndisks, disks_arr);
 #endif
        ss << std::setw(7) << int(double(current_block_size) / MB / (end - begin)) << " MiB/s,";
#endif

#ifndef NOREAD
        begin = timestamp();

        for (i = 0; i < ndisks; i++)
        {
            for (j = 0; j < chunks; j++)
                reqs[i * chunks + j] = disks[i]->aread(
                        buffer + buffer_size_int * i + j * chunk_size_int,
                        offset + j * current_chunk_size,
                        current_chunk_size
                    );
        }

 #ifdef WATCH_TIMES
        watch_times(reqs, ndisks, r_finish_times);
 #else
        wait_all(reqs, ndisks * chunks);
 #endif

        end = timestamp();

        ss << int(double(current_block_size) / MB / (end - begin)) << " MiB/s";
        ss.str();

#ifdef WATCH_TIMES
        out_stat(begin, end, r_finish_times, ndisks, disks_arr);
#endif

        if (CHECK_AFTER_READ) {
            for (size_t i = 0; i < ndisks * buffer_size_int; i++)
            {
                if (buffer[i] != static_cast<int>(i))
                {
                    size_t ibuf = i / buffer_size_int;
                    size_t pos = i % buffer_size_int;

                    LOG1 << "Error on disk " << ibuf << " position " << std::hex << std::setw(8) << offset + pos * sizeof(int)
                         << "  got: " << std::hex << std::setw(8) << buffer[i] << " wanted: " << std::hex << std::setw(8) << static_cast<int>(i)
                         << std::dec;

                    i = (ibuf + 1) * buffer_size_int; // jump to next
                }
            }
        }
#else
        LOG1 << ss.str();
#endif

        offset += current_block_size;
    }

#ifdef WATCH_TIMES
    delete[] r_finish_times;
    delete[] w_finish_times;
#endif
    delete[] reqs;
    for (i = 0; i < ndisks; i++)
        delete disks[i];
    delete[] disks;
    foxxll::aligned_dealloc<BLOCK_ALIGN>(buffer);

    return 0;
}

/**************************************************************************/
