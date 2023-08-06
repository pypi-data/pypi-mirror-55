/***************************************************************************
 *  foxxll/io/linuxaio_file.hpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2011 Johannes Singler <singler@kit.edu>
 *  Copyright (C) 2014 Timo Bingmann <tb@panthema.net>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#ifndef FOXXLL_IO_LINUXAIO_FILE_HEADER
#define FOXXLL_IO_LINUXAIO_FILE_HEADER

#include <foxxll/config.hpp>

#if FOXXLL_HAVE_LINUXAIO_FILE

#include <string>

#include <foxxll/io/disk_queued_file.hpp>
#include <foxxll/io/linuxaio_queue.hpp>
#include <foxxll/io/ufs_file_base.hpp>

namespace foxxll {

class linuxaio_queue;

//! \addtogroup foxxll_fileimpl
//! \{

//! Implementation of \c file based on the Linux kernel interface for
//! asynchronous I/O
class linuxaio_file final : public ufs_file_base, public disk_queued_file
{
    friend class linuxaio_request;

private:
    int desired_queue_length_;

public:
    //! Constructs file object
    //! \param filename path of file
    //! \param mode open mode, see \c foxxll::file::open_modes
    //! \param queue_id disk queue identifier
    //! \param allocator_id linked disk_allocator
    //! \param device_id physical device identifier
    //! \param desired_queue_length queue length requested from kernel
    linuxaio_file(
        const std::string& filename, int mode,
        int queue_id = DEFAULT_LINUXAIO_QUEUE,
        int allocator_id = NO_ALLOCATOR,
        unsigned int device_id = DEFAULT_DEVICE_ID,
        int desired_queue_length = 0)
        : file(device_id),
          ufs_file_base(filename, mode),
          disk_queued_file(queue_id, allocator_id),
          desired_queue_length_(desired_queue_length)
    { }

    void serve(void* buffer, offset_type offset, size_type bytes,
               request::read_or_write op) final;

    request_ptr aread(
        void* buffer, offset_type pos, size_type bytes,
        const completion_handler& on_cmpl = completion_handler()) final;

    request_ptr awrite(
        void* buffer, offset_type pos, size_type bytes,
        const completion_handler& on_cmpl = completion_handler()) final;

    const char * io_type() const final;

    int get_desired_queue_length() const
    { return desired_queue_length_; }
};

//! \}

} // namespace foxxll

#endif // #if FOXXLL_HAVE_LINUXAIO_FILE

#endif // !FOXXLL_IO_LINUXAIO_FILE_HEADER

/**************************************************************************/
