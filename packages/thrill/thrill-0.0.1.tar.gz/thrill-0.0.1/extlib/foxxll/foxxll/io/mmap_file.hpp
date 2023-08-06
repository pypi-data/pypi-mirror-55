/***************************************************************************
 *  foxxll/io/mmap_file.hpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2002 Roman Dementiev <dementiev@mpi-sb.mpg.de>
 *  Copyright (C) 2008 Andreas Beckmann <beckmann@cs.uni-frankfurt.de>
 *  Copyright (C) 2009 Johannes Singler <singler@ira.uka.de>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#ifndef FOXXLL_IO_MMAP_FILE_HEADER
#define FOXXLL_IO_MMAP_FILE_HEADER

#include <foxxll/config.hpp>

#if FOXXLL_HAVE_MMAP_FILE

#include <string>

#include <foxxll/io/disk_queued_file.hpp>
#include <foxxll/io/ufs_file_base.hpp>

namespace foxxll {

//! \addtogroup foxxll_fileimpl
//! \{

//! Implementation of memory mapped access file.
class mmap_file final : public ufs_file_base, public disk_queued_file
{
public:
    //! Constructs file object.
    //! \param filename path of file
    //! \param mode open mode, see \c foxxll::file::open_modes
    //! \param queue_id disk queue identifier
    //! \param allocator_id linked disk_allocator
    //! \param device_id physical device identifier
    //! \param file_stats file-specific stats
    inline mmap_file(
        const std::string& filename,
        int mode,
        int queue_id = DEFAULT_QUEUE,
        int allocator_id = NO_ALLOCATOR,
        unsigned int device_id = DEFAULT_DEVICE_ID,
        file_stats* file_stats = nullptr)
        : file(device_id, file_stats),
          ufs_file_base(filename, mode),
          disk_queued_file(queue_id, allocator_id)
    { }
    void serve(void* buffer, offset_type offset, size_type bytes,
               request::read_or_write op) final;
    const char * io_type() const final;
};

//! \}

} // namespace foxxll

#endif // #if FOXXLL_HAVE_MMAP_FILE

#endif // !FOXXLL_IO_MMAP_FILE_HEADER

/**************************************************************************/
