/***************************************************************************
 *  tools/foxxll_tool.cpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2007, 2009-2011 Andreas Beckmann <beckmann@cs.uni-frankfurt.de>
 *  Copyright (C) 2013 Timo Bingmann <tb@panthema.net>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#include <algorithm>

#include <tlx/logger.hpp>

#include <foxxll/common/utils.hpp>
#include <foxxll/io.hpp>
#include <foxxll/mng.hpp>
#include <foxxll/version.hpp>
#include <tlx/cmdline_parser.hpp>

int foxxll_info(int, char**)
{
    foxxll::config::get_instance();
    foxxll::block_manager::get_instance();
    foxxll::stats::get_instance();
    foxxll::disk_queues::get_instance();

    LOG1 << "sizeof(unsigned int)   = " << sizeof(unsigned int);
    LOG1 << "sizeof(uint64_t)       = " << sizeof(uint64_t);
    LOG1 << "sizeof(long)           = " << sizeof(long);
    LOG1 << "sizeof(size_t)         = " << sizeof(size_t);
    LOG1 << "sizeof(off_t)          = " << sizeof(off_t);
    LOG1 << "sizeof(void*)          = " << sizeof(void*);

#if defined(FOXXLL_HAVE_LINUXAIO_FILE)
    LOG1 << "FOXXLL_HAVE_LINUXAIO_FILE = " << FOXXLL_HAVE_LINUXAIO_FILE;
#endif

    return 0;
}

extern int create_files(int argc, char* argv[]);
extern int benchmark_disks(int argc, char* argv[]);
extern int benchmark_files(int argc, char* argv[]);
extern int benchmark_sort(int argc, char* argv[]);
extern int benchmark_disks_random(int argc, char* argv[]);
extern int benchmark_pqueue(int argc, char* argv[]);
extern int do_mlock(int argc, char* argv[]);
extern int do_mallinfo(int argc, char* argv[]);

struct SubTool
{
    const char* name;
    int (* func)(int argc, char* argv[]);
    bool shortline;
    const char* description;
};

struct SubTool subtools[] = {
    {
        "info", &foxxll_info, false,
        "Print out information about the build system and which optional "
        "modules where compiled into FOXXLL."
    },
    {
        "create_files", &create_files, false,
        "Precreate large files to keep file system allocation time out to measurements."
    },
    {
        "benchmark_disks", &benchmark_disks, false,
        "This program will benchmark the disks configured by the standard "
        ".foxxll disk configuration files mechanism."
    },
    {
        "benchmark_files", &benchmark_files, false,
        "Benchmark different file access methods, e.g. syscall or mmap_files."
    },
    {
        "benchmark_disks_random", &benchmark_disks_random, false,
        "Benchmark random block access time to .foxxll configured disks."
    },
    { nullptr, nullptr, false, nullptr }
};

int main_usage(const char* arg0)
{
    LOG1 << foxxll::get_version_string_long();
    LOG1 << "Usage: " << arg0 << " <subtool> ...\n"
        "Available subtools: ";

    int shortlen = 0;

    for (unsigned int i = 0; subtools[i].name; ++i)
    {
        if (!subtools[i].shortline) continue;
        shortlen = std::max(shortlen, static_cast<int>(strlen(subtools[i].name)));
    }

    for (unsigned int i = 0; subtools[i].name; ++i)
    {
        if (subtools[i].shortline) continue;
        LOG1 << "  " << subtools[i].name;
        tlx::CmdlineParser::output_wrap(std::cout, subtools[i].description, 80, 6, 6);
    }

    for (unsigned int i = 0; subtools[i].name; ++i)
    {
        if (!subtools[i].shortline) continue;
        LOG1 << "  " << std::left << std::setw(shortlen + 2)
             << subtools[i].name << subtools[i].description;
    }

    return 0;
}

int main(int argc, char** argv)
{
    static char progsub[256];

    if (foxxll::check_library_version() != 0)
        LOG1 << "version mismatch between headers and library";

    if (argc > 1)
    {
        for (unsigned int i = 0; subtools[i].name; ++i)
        {
            if (strcmp(subtools[i].name, argv[1]) == 0)
            {
                // replace argv[1] with call string of subtool.
                snprintf(progsub, sizeof(progsub), "%s %s", argv[0], argv[1]);
                argv[1] = progsub;
                return subtools[i].func(argc - 1, argv + 1);
            }
        }
        LOG1 << "Unknown subtool '" << argv[1] << "'";
    }

    return main_usage(argv[0]);
}

/**************************************************************************/
