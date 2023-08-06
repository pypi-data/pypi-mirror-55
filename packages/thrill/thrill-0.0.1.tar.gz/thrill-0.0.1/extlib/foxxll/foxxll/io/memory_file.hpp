/***************************************************************************
 *  foxxll/io/memory_file.hpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2008 Andreas Beckmann <beckmann@cs.uni-frankfurt.de>
 *  Copyright (C) 2009 Johannes Singler <singler@ira.uka.de>
 *  Copyright (C) 2014 Timo Bingmann <tb@panthema.net>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#ifndef FOXXLL_IO_MEMORY_FILE_HEADER
#define FOXXLL_IO_MEMORY_FILE_HEADER

#include <mutex>

#include <foxxll/io/disk_queued_file.hpp>
#include <foxxll/io/request.hpp>

namespace foxxll {

//! \addtogroup foxxll_fileimpl
//! \{

//! Implementation of file based on new[] and memcpy.
class memory_file final : public disk_queued_file
{
    //! pointer to memory area of "file"
    char* ptr_;

    //! size of memory area
    offset_type size_;

    //! sequentialize function calls
    std::mutex mutex_;

public:
    //! constructs file object.
    memory_file(
        int queue_id = DEFAULT_QUEUE,
        int allocator_id = NO_ALLOCATOR,
        unsigned int device_id = DEFAULT_DEVICE_ID)
        : file(device_id),
          disk_queued_file(queue_id, allocator_id),
          ptr_(nullptr), size_(0)
    { }
    void serve(void* buffer, offset_type offset, size_type bytes,
               request::read_or_write op) final;
    ~memory_file();
    offset_type size() final;
    void set_size(offset_type newsize) final;
    void lock() final;
    void discard(offset_type offset, offset_type size) final;
    const char * io_type() const final;
};

//! \}

} // namespace foxxll

#endif // !FOXXLL_IO_MEMORY_FILE_HEADER

/**************************************************************************/
