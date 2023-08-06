/***************************************************************************
 *  foxxll/io/serving_request.cpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2002 Roman Dementiev <dementiev@mpi-sb.mpg.de>
 *  Copyright (C) 2008 Andreas Beckmann <beckmann@cs.uni-frankfurt.de>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#include <iomanip>

#include <foxxll/common/exceptions.hpp>
#include <foxxll/common/shared_state.hpp>
#include <foxxll/io/file.hpp>
#include <foxxll/io/request_interface.hpp>
#include <foxxll/io/request_with_state.hpp>
#include <foxxll/io/serving_request.hpp>

namespace foxxll {

serving_request::serving_request(
    const completion_handler& on_cmpl,
    file* file, void* buffer, offset_type offset, size_type bytes,
    read_or_write op)
    : request_with_state(on_cmpl, file, buffer, offset, bytes, op)
{
#ifdef FOXXLL_CHECK_BLOCK_ALIGNING
    // Direct I/O requires file system block size alignment for file offsets,
    // memory buffer addresses, and transfer(buffer) size must be multiple
    // of the file system block size
    if (file->need_alignment())
        check_alignment();
#endif
}

void serving_request::serve()
{
    check_nref();
    TLX_LOG
        << "serving_request[" << static_cast<void*>(this) << "]::serve(): "
        << buffer_ << " @ ["
        << file_ << "|" << file_->get_allocator_id() << "]0x"
        << std::hex << std::setfill('0') << std::setw(8)
        << offset_ << "/0x" << bytes_
        << (op_ == request::READ ? " READ" : " WRITE");

    try
    {
        file_->serve(buffer_, offset_, bytes_, op_);
    }
    catch (const io_error& ex)
    {
        error_occured(ex.what());
    }

    check_nref(true);

    completed(false);
}

const char* serving_request::io_type() const
{
    return file_->io_type();
}

} // namespace foxxll

/**************************************************************************/
