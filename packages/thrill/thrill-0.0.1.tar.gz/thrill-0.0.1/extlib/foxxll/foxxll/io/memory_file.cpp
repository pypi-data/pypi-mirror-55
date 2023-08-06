/***************************************************************************
 *  foxxll/io/memory_file.cpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2008 Andreas Beckmann <beckmann@cs.uni-frankfurt.de>
 *  Copyright (C) 2013-2014 Timo Bingmann <tb@panthema.net>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#include <cassert>
#include <cstring>
#include <limits>

#include <tlx/logger/core.hpp>
#include <tlx/unused.hpp>

#include <foxxll/io/iostats.hpp>
#include <foxxll/io/memory_file.hpp>

namespace foxxll {

void memory_file::serve(void* buffer, offset_type offset, size_type bytes,
                        request::read_or_write op)
{
    std::unique_lock<std::mutex> lock(mutex_);

    if (op == request::READ)
    {
        file_stats::scoped_read_timer read_timer(file_stats_, bytes);
        memcpy(buffer, ptr_ + offset, bytes);
    }
    else
    {
        file_stats::scoped_write_timer write_timer(file_stats_, bytes);
        memcpy(ptr_ + offset, buffer, bytes);
    }
}

const char* memory_file::io_type() const
{
    return "memory";
}

memory_file::~memory_file()
{
    free(ptr_);
    ptr_ = nullptr;
}

void memory_file::lock()
{
    // nothing to do
}

file::offset_type memory_file::size()
{
    return size_;
}

void memory_file::set_size(offset_type newsize)
{
    std::unique_lock<std::mutex> lock(mutex_);
    assert(newsize <= std::numeric_limits<size_t>::max());

    ptr_ = static_cast<char*>(realloc(ptr_, static_cast<size_t>(newsize)));
    size_ = newsize;
}

void memory_file::discard(offset_type offset, offset_type size)
{
    std::unique_lock<std::mutex> lock(mutex_);
#ifndef FOXXLL_MEMFILE_DONT_CLEAR_FREED_MEMORY
    // overwrite the freed region with uninitialized memory
    TLX_LOG1 << "discard at " << offset << " len " << size;
    void* uninitialized = malloc(BlockAlignment);
    while (size >= BlockAlignment) {
        memcpy(ptr_ + offset, uninitialized, BlockAlignment);
        offset += BlockAlignment;
        size -= BlockAlignment;
    }
    assert(size <= std::numeric_limits<offset_type>::max());
    if (size > 0)
        memcpy(ptr_ + offset, uninitialized, static_cast<size_t>(size));
    free(uninitialized);
#else
    tlx::unused(offset);
    tlx::unused(size);
#endif
}

} // namespace foxxll

/******************************************************************************/

/**************************************************************************/
