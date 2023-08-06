/***************************************************************************
 *  tools/benchmark_files.cpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2002-2003 Roman Dementiev <dementiev@mpi-sb.mpg.de>
 *  Copyright (C) 2007-2011 Andreas Beckmann <beckmann@cs.uni-frankfurt.de>
 *  Copyright (C) 2009 Johannes Singler <singler@ira.uka.de>
 *  Copyright (C) 2013 Timo Bingmann <tb@panthema.net>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

/*
   example gnuplot command for the output of this program:
   (x-axis: file offset in GiB, y-axis: bandwidth in MiB/s)

   plot \
        "file.log" using ($3/1024):($14) w l title "read", \
        "file.log" using ($3/1024):($7)  w l title "write"
 */

#include <algorithm>
#include <cstring>
#include <iomanip>
#include <sstream>
#include <vector>

#include <tlx/cmdline_parser.hpp>
#include <tlx/logger.hpp>

#include <foxxll/common/aligned_alloc.hpp>
#include <foxxll/common/timer.hpp>
#include <foxxll/io.hpp>
#include <foxxll/version.hpp>

using foxxll::request_ptr;
using foxxll::file;
using foxxll::timestamp;
using foxxll::external_size_type;

#ifdef BLOCK_ALIGN
 #undef BLOCK_ALIGN
#endif

#define BLOCK_ALIGN  4096

#define POLL_DELAY 1000

#if FOXXLL_WINDOWS
const char* default_file_type = "wincall";
#else
const char* default_file_type = "syscall";
#endif

#ifdef WATCH_TIMES
void watch_times(request_ptr reqs[], size_t n, double* out)
{
    bool* finished = new bool[n];
    size_t count = 0;
    for (size_t i = 0; i < n; i++)
        finished[i] = false;

    while (count != n)
    {
        usleep(POLL_DELAY);
        for (size_t i = 0; i < n; i++)
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

void out_stat(double start, double end, double* times, size_t n, const std::vector<std::string>& names)
{
    for (size_t i = 0; i < n; i++)
    {
        LOG1 << i << " " << names[i] << " took " << 100. * (times[i] - start) / (end - start) << " %";
    }
}
#endif

#define MB (1024 * 1024)

// returns throughput in MiB/s
static inline double throughput(external_size_type bytes, double seconds)
{
    if (seconds == 0.0)
        return 0.0;
    return static_cast<double>(bytes) / (1024 * 1024) / seconds;
}

int benchmark_files(int argc, char* argv[])
{
    external_size_type offset = 0, length = 0;

    bool no_direct_io = false;
    bool sync_io = false;
    bool resize_after_open = false;
    std::string file_type = default_file_type;
    external_size_type block_size = 0;
    unsigned int batch_size = 1;
    std::string opstr = "wv";
    uint32_t pattern = 0;

    std::vector<std::string> files_arr;

    tlx::CmdlineParser cp;

    cp.add_param_bytes(
        "length", length,
        "Length to write in file."
    );

    cp.add_param_stringlist(
        "filename", files_arr,
        "File path to run benchmark on."
    );

    cp.add_bytes(
        'o', "offset", offset,
        "Starting offset to write in file."
    );

    cp.add_bool(
        0, "no-direct", no_direct_io,
        "open files without O_DIRECT"
    );

    cp.add_bool(
        0, "sync", sync_io,
        "open files with O_SYNC|O_DSYNC|O_RSYNC"
    );

    cp.add_bool(
        0, "resize", resize_after_open,
        "resize the file size after opening, "
        "needed e.g. for creating mmap files"
    );

    cp.add_bytes(
        0, "block_size", block_size,
        "block size for operations (default 8 MiB)"
    );

    cp.add_unsigned(
        0, "batch_size", batch_size,
        "increase (default 1) to submit several I/Os at once "
        "and report average rate"
    );

    cp.add_string(
        'f', "file-type", file_type,
        "Method to open file (syscall|mmap|wincall|...) "
        "default: " + file_type
    );

    cp.add_string(
        'p', "operations", opstr,
        "[w]rite pattern, [r]ead without verification, "
        "read and [v]erify pattern (default: 'wv')"
    );

    cp.add_unsigned(
        0, "pattern", pattern,
        "32-bit pattern to write (default: block index)"
    );

    cp.set_description(
        "Open a file using one of FOXXLL's file abstractions and perform "
        "write/read/verify tests on the file. "
        "Block sizes and batch size can be adjusted via command line. "
        "If length == 0 , then operation will continue till end of space "
        "(please ignore the write error). "
        "Memory consumption: block_size * batch_size * num_files"
    );

    if (!cp.process(argc, argv))
        return -1;

    external_size_type endpos = offset + length;

    if (block_size == 0)
        block_size = 8 * MB;

    if (batch_size == 0)
        batch_size = 1;

    bool do_read = false, do_write = false, do_verify = false;

    // deprecated, use --no-direct instead
    if (opstr.find("nd") != std::string::npos || opstr.find("ND") != std::string::npos) {
        no_direct_io = true;
    }

    if (opstr.find('r') != std::string::npos || opstr.find('R') != std::string::npos) {
        do_read = true;
    }
    if (opstr.find('v') != std::string::npos || opstr.find('V') != std::string::npos) {
        do_verify = true;
    }
    if (opstr.find('w') != std::string::npos || opstr.find('W') != std::string::npos) {
        do_write = true;
    }

    const char* myself = strrchr(argv[0], '/');
    if (!myself || !*(++myself))
        myself = argv[0];

    LOG1 << "# " << myself << " " << foxxll::get_version_string_long();
#if FOXXLL_DIRECT_IO_OFF
    LOG1 << " FOXXLL_DIRECT_IO_OFF";
#endif

    for (size_t ii = 0; ii < files_arr.size(); ii++)
    {
        LOG1 << "# Add file: " << files_arr[ii];
    }

    const size_t nfiles = files_arr.size();
    bool verify_failed = false;

    const size_t step_size = block_size * batch_size;
    const size_t block_size_int = block_size / sizeof(uint32_t);
    const size_t step_size_int = step_size / sizeof(uint32_t);

    uint32_t* buffer = static_cast<uint32_t*>(foxxll::aligned_alloc<BLOCK_ALIGN>(step_size * nfiles));
    std::vector<foxxll::file_ptr> files(nfiles);
    std::vector<request_ptr> reqs(nfiles* batch_size);

#ifdef WATCH_TIMES
    double* r_finish_times = new double[nfiles];
    double* w_finish_times = new double[nfiles];
#endif

    double totaltimeread = 0, totaltimewrite = 0;
    external_size_type totalsizeread = 0, totalsizewrite = 0;

    // fill buffer with pattern
    for (size_t i = 0; i < nfiles * step_size_int; i++)
        buffer[i] = (pattern ? pattern : static_cast<uint32_t>(i));

    // open files
    for (size_t i = 0; i < nfiles; i++)
    {
        int openmode = file::CREAT | file::RDWR;
        if (!no_direct_io) {
            openmode |= file::DIRECT;
        }
        if (sync_io) {
            openmode |= file::SYNC;
        }

        files[i] = foxxll::create_file(file_type, files_arr[i], openmode, static_cast<int>(i));
        if (resize_after_open)
            files[i]->set_size(endpos);
    }

    LOG1 << "# Step size: "
         << step_size << " bytes per file ("
         << batch_size << " block" << (batch_size == 1 ? "" : "s") << " of "
         << block_size << " bytes)"
         << " file_type=" << file_type
         << " O_DIRECT=" << (no_direct_io ? "no" : "yes")
         << " O_SYNC=" << (sync_io ? "yes" : "no");

    foxxll::timer t_total(true);
    try {
        while (offset + step_size <= endpos || length == 0)
        {
            const size_t current_step_size = (length == 0) ? step_size : static_cast<size_t>(std::min<external_size_type>(step_size, endpos - offset));
            const size_t current_step_size_int = current_step_size / sizeof(uint32_t);
            const size_t current_num_blocks = foxxll::div_ceil(current_step_size, block_size);
            std::stringstream ss;

            ss << "File offset    " << std::setw(8) << offset / MB << " MiB: " << std::fixed;

            double begin = timestamp(), end = begin, elapsed;

            if (do_write)
            {
                // write block number (512 byte blocks) into each block at position 42 * sizeof(uint32_t)
                for (external_size_type j = 42, b = offset >> 9; j < current_step_size_int; j += 512 / sizeof(uint32_t), ++b)
                {
                    for (size_t i = 0; i < nfiles; i++)
                        buffer[current_step_size_int * i + j] = static_cast<uint32_t>(b);
                }

                for (size_t i = 0; i < nfiles; i++)
                {
                    for (size_t j = 0; j < current_num_blocks; j++)
                        reqs[i * current_num_blocks + j] =
                            files[i]->awrite(
                                buffer + current_step_size_int * i + j * block_size_int,
                                offset + j * block_size,
                                block_size
                            );
                }

 #ifdef WATCH_TIMES
                watch_times(reqs, nfiles, w_finish_times);
 #else
                wait_all(reqs.begin(), reqs.end());
 #endif

                end = timestamp();
                elapsed = end - begin;
                totalsizewrite += current_step_size;
                totaltimewrite += elapsed;
            }
            else {
                elapsed = 0.0;
            }

 #ifdef WATCH_TIMES
            out_stat(begin, end, w_finish_times, nfiles, files_arr);
 #endif
            ss << std::setw(2) << nfiles << " * "
               << std::setw(8) << std::setprecision(3)
               << (throughput(current_step_size, elapsed)) << " = "
               << std::setw(8) << std::setprecision(3)
               << (throughput(current_step_size, elapsed) * nfiles) << " MiB/s write,";

            begin = end = timestamp();

            if (do_read || do_verify)
            {
                for (size_t i = 0; i < nfiles; i++)
                {
                    for (size_t j = 0; j < current_num_blocks; j++)
                        reqs[i * current_num_blocks + j] =
                            files[i]->aread(
                                buffer + current_step_size_int * i + j * block_size_int,
                                offset + j * block_size,
                                block_size
                            );
                }

 #ifdef WATCH_TIMES
                watch_times(reqs, nfiles, r_finish_times);
 #else
                wait_all(reqs.begin(), reqs.end());
 #endif

                end = timestamp();
                elapsed = end - begin;
                totalsizeread += current_step_size;
                totaltimeread += elapsed;
            }
            else {
                elapsed = 0.0;
            }

            ss << std::setw(2) << nfiles << " * "
               << std::setw(8) << std::setprecision(3)
               << (throughput(current_step_size, elapsed)) << " = "
               << std::setw(8) << std::setprecision(3)
               << (throughput(current_step_size, elapsed) * nfiles) << " MiB/s read";

            LOG1 << ss.str();

#ifdef WATCH_TIMES
            out_stat(begin, end, r_finish_times, nfiles, files_arr);
#endif

            if (do_verify)
            {
                for (size_t d = 0; d < nfiles; ++d)
                {
                    for (size_t s = 0; s < (current_step_size >> 9); ++s) {
                        size_t i = d * current_step_size_int + s * (512 / sizeof(uint32_t)) + 42;
                        external_size_type b = (offset >> 9) + s;
                        if (buffer[i] != b)
                        {
                            verify_failed = true;
                            LOG1 << "Error on file " << d << " sector " << std::hex << std::setw(8) << b
                                 << " got: " << std::hex << std::setw(8) << buffer[i] << " wanted: " << std::hex << std::setw(8) << b
                                 << std::dec;
                        }
                        buffer[i] = (pattern ? pattern : static_cast<int32_t>(i));
                    }
                }

                for (size_t i = 0; i < nfiles * current_step_size_int; i++)
                {
                    if (buffer[i] != (pattern ? pattern : i))
                    {
                        size_t ibuf = i / current_step_size_int;
                        size_t pos = i % current_step_size_int;

                        LOG1 << "Error on file " << ibuf << " position " << std::hex << std::setw(8) << offset + pos * sizeof(uint32_t)
                             << "  got: " << std::hex << std::setw(8) << buffer[i] << " wanted: " << std::hex << std::setw(8) << i
                             << std::dec;

                        i = (ibuf + 1) * current_step_size_int; // jump to next

                        verify_failed = true;
                    }
                }
            }

            offset += current_step_size;
        }
    }
    catch (const std::exception& ex)
    {
        LOG1 << ex.what();
    }
    t_total.stop();

    LOG1 << "=============================================================================================\n";
    // the following line of output is parsed by misc/filebench-avgplot.sh
    LOG1 << "# Average over " << std::setw(8) << std::max(totalsizewrite, totalsizeread) / MB << " MiB: "
         << std::setw(2) << nfiles << " * "
         << std::setw(8) << std::setprecision(3)
         << (throughput(totalsizewrite, totaltimewrite)) << " = "
         << std::setw(8) << std::setprecision(3)
         << (throughput(totalsizewrite, totaltimewrite) * nfiles) << " MiB/s write,"

         << std::setw(2) << nfiles << " * "
         << std::setw(8) << std::setprecision(3)
         << (throughput(totalsizeread, totaltimeread)) << " = "
         << std::setw(8) << std::setprecision(3)
         << (throughput(totalsizeread, totaltimeread) * nfiles) << " MiB/s read";

    if (totaltimewrite != 0.0)
        LOG1 << "# Write time   " << std::setw(8) << std::setprecision(3) << totaltimewrite << " s";
    if (totaltimeread != 0.0)
        LOG1 << "# Read time    " << std::setw(8) << std::setprecision(3) << totaltimeread << " s";

    LOG1 << "# Non-I/O time " << std::setw(8) << std::setprecision(3)
         << (t_total.seconds() - totaltimewrite - totaltimeread) << " s, average throughput "
         << std::setw(8) << std::setprecision(3)
         << (throughput(totalsizewrite + totalsizeread, t_total.seconds() - totaltimewrite - totaltimeread) * nfiles) << " MiB/s";

    LOG1 << "# Total time   " << std::setw(8) << std::setprecision(3) << t_total.seconds() << " s, average throughput "
         << std::setw(8) << std::setprecision(3)
         << (throughput(totalsizewrite + totalsizeread, t_total.seconds()) * nfiles) << " MiB/s";

    if (do_verify)
    {
        LOG1 << "# Verify: " << (verify_failed ? "FAILED." : "all okay.");
    }

#ifdef WATCH_TIMES
    delete[] r_finish_times;
    delete[] w_finish_times;
#endif
    foxxll::aligned_dealloc<BLOCK_ALIGN>(buffer);

    return (verify_failed ? 1 : 0);
}

/**************************************************************************/
