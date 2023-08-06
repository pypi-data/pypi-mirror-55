/***************************************************************************
 *  foxxll/io/wincall_file.hpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2005-2006 Roman Dementiev <dementiev@ira.uka.de>
 *  Copyright (C) 2008 Andreas Beckmann <beckmann@cs.uni-frankfurt.de>
 *  Copyright (C) 2009-2010 Johannes Singler <singler@kit.edu>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#ifndef FOXXLL_IO_WINCALL_FILE_HEADER
#define FOXXLL_IO_WINCALL_FILE_HEADER

#include <foxxll/config.hpp>

#ifndef FOXXLL_HAVE_WINCALL_FILE
#if FOXXLL_WINDOWS
 #define FOXXLL_HAVE_WINCALL_FILE 1
#else
 #define FOXXLL_HAVE_WINCALL_FILE 0
#endif
#endif

#if FOXXLL_HAVE_WINCALL_FILE

#include <string>

#include <foxxll/io/disk_queued_file.hpp>
#include <foxxll/io/wfs_file_base.hpp>

namespace foxxll {

//! \addtogroup foxxll_fileimpl
//! \{

//! Implementation of file based on Windows native I/O calls.
class wincall_file final : public wfs_file_base, public disk_queued_file
{
public:
    //! Constructs file object.
    //! \param filename path of file
    //! \param mode open mode, see \c foxxll::file::open_modes
    //! \param queue_id disk queue identifier
    //! \param allocator_id linked disk_allocator
    //! \param device_id physical device identifier
    //! \param file_stats file-specific stats
    wincall_file(
        const std::string& filename,
        int mode,
        int queue_id = DEFAULT_QUEUE,
        int allocator_id = NO_ALLOCATOR,
        unsigned int device_id = DEFAULT_DEVICE_ID,
        file_stats* file_stats = nullptr)
        : file(device_id, file_stats),
          wfs_file_base(filename, mode),
          disk_queued_file(queue_id, allocator_id)
    { }
    void serve(void* buffer, offset_type offset, size_type bytes,
               request::read_or_write op) final;
    const char * io_type() const final;
};

//! \}

} // namespace foxxll

#endif // #if FOXXLL_HAVE_WINCALL_FILE

#endif // !FOXXLL_IO_WINCALL_FILE_HEADER

/**************************************************************************/
