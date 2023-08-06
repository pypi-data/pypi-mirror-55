/***************************************************************************
 *  foxxll/io/create_file.cpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2002 Roman Dementiev <dementiev@mpi-sb.mpg.de>
 *  Copyright (C) 2008, 2010 Andreas Beckmann <beckmann@cs.uni-frankfurt.de>
 *  Copyright (C) 2008, 2009 Johannes Singler <singler@ira.uka.de>
 *  Copyright (C) 2013 Timo Bingmann <tb@panthema.net>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#include <foxxll/io/create_file.hpp>

#include <ostream>
#include <stdexcept>
#include <string>

#include <foxxll/common/error_handling.hpp>
#include <foxxll/common/exceptions.hpp>
#include <foxxll/io.hpp>
#include <foxxll/mng/config.hpp>

namespace foxxll {

file_ptr create_file(const std::string& io_impl,
                     const std::string& filename,
                     int options, int physical_device_id, int disk_allocator_id)
{
    // construct temporary disk_config structure
    disk_config cfg(filename, 0, io_impl);
    cfg.queue = physical_device_id;
    cfg.direct =
        (options& file::REQUIRE_DIRECT) ? disk_config::DIRECT_ON :
        (options& file::DIRECT) ? disk_config::DIRECT_TRY :
        disk_config::DIRECT_OFF;

    return create_file(cfg, options, disk_allocator_id);
}

file_ptr create_file(disk_config& cfg, int mode, int disk_allocator_id)
{
    // apply disk_config settings to open mode

    mode &= ~(file::DIRECT | file::REQUIRE_DIRECT); // clear DIRECT and REQUIRE_DIRECT

    switch (cfg.direct) {
    case disk_config::DIRECT_OFF:
        break;
    case disk_config::DIRECT_TRY:
        mode |= file::DIRECT;
        break;
    case disk_config::DIRECT_ON:
        mode |= file::DIRECT | file::REQUIRE_DIRECT;
        break;
    }

    // automatically enumerate disks as separate device ids

    if (cfg.device_id == file::DEFAULT_DEVICE_ID)
    {
        cfg.device_id = config::get_instance()->next_device_id();
    }
    else
    {
        config::get_instance()->update_max_device_id(cfg.device_id);
    }

    // *** Select fileio Implementation

    if (cfg.io_impl == "syscall")
    {
        tlx::counting_ptr<ufs_file_base> result =
            tlx::make_counting<syscall_file>(
                cfg.path, mode, cfg.queue, disk_allocator_id, cfg.device_id
            );
        result->lock();

        // if marked as device but file is not -> throw!
        if (cfg.raw_device && !result->is_device())
        {
            FOXXLL_THROW(
                io_error, "Disk " << cfg.path << " was expected to be "
                    "a raw block device, but it is a normal file!"
            );
        }

        // if is raw_device -> get size and remove some flags.
        if (result->is_device())
        {
            cfg.raw_device = true;
            cfg.size = result->size();
            cfg.autogrow = cfg.delete_on_exit = cfg.unlink_on_open = false;
        }

        if (cfg.unlink_on_open)
            result->unlink();

        return result;
    }
    else if (cfg.io_impl == "fileperblock_syscall")
    {
        tlx::counting_ptr<fileperblock_file<syscall_file> > result =
            tlx::make_counting<fileperblock_file<syscall_file> >(
                cfg.path, mode, cfg.queue, disk_allocator_id, cfg.device_id
            );
        result->lock();
        return result;
    }
    else if (cfg.io_impl == "memory")
    {
        tlx::counting_ptr<memory_file> result =
            tlx::make_counting<memory_file>(
                cfg.queue, disk_allocator_id, cfg.device_id
            );
        result->lock();
        return result;
    }
#if FOXXLL_HAVE_LINUXAIO_FILE
    // linuxaio can have the desired queue length, specified as queue_length=?
    else if (cfg.io_impl == "linuxaio")
    {
        // linuxaio_queue is a singleton.
        cfg.queue = file::DEFAULT_LINUXAIO_QUEUE;

        tlx::counting_ptr<ufs_file_base> result =
            tlx::make_counting<linuxaio_file>(
                cfg.path, mode, cfg.queue, disk_allocator_id,
                cfg.device_id, cfg.queue_length
            );

        result->lock();

        // if marked as device but file is not -> throw!
        if (cfg.raw_device && !result->is_device())
        {
            FOXXLL_THROW(
                io_error, "Disk " << cfg.path << " was expected to be "
                    "a raw block device, but it is a normal file!"
            );
        }

        // if is raw_device -> get size and remove some flags.
        if (result->is_device())
        {
            cfg.raw_device = true;
            cfg.size = result->size();
            cfg.autogrow = cfg.delete_on_exit = cfg.unlink_on_open = false;
        }

        if (cfg.unlink_on_open)
            result->unlink();

        return result;
    }
#endif
#if FOXXLL_HAVE_MMAP_FILE
    else if (cfg.io_impl == "mmap")
    {
        tlx::counting_ptr<ufs_file_base> result =
            tlx::make_counting<mmap_file>(
                cfg.path, mode, cfg.queue, disk_allocator_id, cfg.device_id
            );
        result->lock();

        if (cfg.unlink_on_open)
            result->unlink();

        return result;
    }
    else if (cfg.io_impl == "fileperblock_mmap")
    {
        tlx::counting_ptr<fileperblock_file<mmap_file> > result =
            tlx::make_counting<fileperblock_file<mmap_file> >(
                cfg.path, mode, cfg.queue, disk_allocator_id, cfg.device_id
            );
        result->lock();
        return result;
    }
#endif
#if FOXXLL_HAVE_WINCALL_FILE
    else if (cfg.io_impl == "wincall")
    {
        tlx::counting_ptr<wfs_file_base> result =
            tlx::make_counting<wincall_file>(
                cfg.path, mode, cfg.queue, disk_allocator_id, cfg.device_id
            );
        result->lock();
        return result;
    }
    else if (cfg.io_impl == "fileperblock_wincall")
    {
        tlx::counting_ptr<fileperblock_file<wincall_file> > result =
            tlx::make_counting<fileperblock_file<wincall_file> >(
                cfg.path, mode, cfg.queue, disk_allocator_id, cfg.device_id
            );
        result->lock();
        return result;
    }
#endif

    FOXXLL_THROW(
        std::runtime_error,
        "Unsupported disk I/O implementation '" << cfg.io_impl << "'."
    );
}

} // namespace foxxll

/**************************************************************************/
