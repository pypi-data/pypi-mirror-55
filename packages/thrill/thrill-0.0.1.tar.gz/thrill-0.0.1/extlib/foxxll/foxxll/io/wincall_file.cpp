/***************************************************************************
 *  foxxll/io/wincall_file.cpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2005-2006 Roman Dementiev <dementiev@ira.uka.de>
 *  Copyright (C) 2008-2010 Andreas Beckmann <beckmann@cs.uni-frankfurt.de>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#include <foxxll/io/wincall_file.hpp>

#if FOXXLL_HAVE_WINCALL_FILE

#include <limits>

#ifndef NOMINMAX
  #define NOMINMAX
#endif
#include <windows.h>

#include <tlx/logger/core.hpp>

#include <foxxll/common/error_handling.hpp>
#include <foxxll/io/iostats.hpp>

namespace foxxll {

void wincall_file::serve(void* buffer, offset_type offset, size_type bytes,
                         request::read_or_write op)
{
    std::unique_lock<std::mutex> fd_lock(fd_mutex_);

    if (bytes > 32 * 1024 * 1024) {
        TLX_LOG1 << "Using a block size larger than 32 MiB"
                 << " may not work with the " << io_type() << " filetype";
    }

    HANDLE handle = file_des_;
    LARGE_INTEGER desired_pos;
    desired_pos.QuadPart = offset;
    if (!SetFilePointerEx(handle, desired_pos, nullptr, FILE_BEGIN))
    {
        FOXXLL_THROW_WIN_LASTERROR(
            io_error,
            "SetFilePointerEx in wincall_request::serve()" <<
                " offset=" << offset <<
                " this=" << this <<
                " buffer=" << buffer <<
                " bytes=" << bytes <<
                " op=" << ((op == request::READ) ? "READ" : "WRITE")
        );
    }
    else
    {
        file_stats::scoped_read_write_timer read_write_timer(
            file_stats_, bytes, op == request::WRITE);

        if (op == request::READ)
        {
            DWORD NumberOfBytesRead = 0;
            assert(bytes <= std::numeric_limits<DWORD>::max());
            if (!ReadFile(handle, buffer, (DWORD)bytes, &NumberOfBytesRead, nullptr))
            {
                FOXXLL_THROW_WIN_LASTERROR(
                    io_error,
                    "ReadFile" <<
                        " this=" << this <<
                        " offset=" << offset <<
                        " buffer=" << buffer <<
                        " bytes=" << bytes <<
                        " op=" << ((op == request::READ) ? "READ" : "WRITE") <<
                        " NumberOfBytesRead= " << NumberOfBytesRead
                );
            }
            else if (NumberOfBytesRead != bytes) {
                FOXXLL_THROW_WIN_LASTERROR(io_error, " partial read: missing " << (bytes - NumberOfBytesRead) << " out of " << bytes << " bytes");
            }
        }
        else
        {
            DWORD NumberOfBytesWritten = 0;
            assert(bytes <= std::numeric_limits<DWORD>::max());
            if (!WriteFile(handle, buffer, (DWORD)bytes, &NumberOfBytesWritten, nullptr))
            {
                FOXXLL_THROW_WIN_LASTERROR(
                    io_error,
                    "WriteFile" <<
                        " this=" << this <<
                        " offset=" << offset <<
                        " buffer=" << buffer <<
                        " bytes=" << bytes <<
                        " op=" << ((op == request::READ) ? "READ" : "WRITE") <<
                        " NumberOfBytesWritten= " << NumberOfBytesWritten
                );
            }
            else if (NumberOfBytesWritten != bytes) {
                FOXXLL_THROW_WIN_LASTERROR(io_error, " partial write: missing " << (bytes - NumberOfBytesWritten) << " out of " << bytes << " bytes");
            }
        }
    }
}

const char* wincall_file::io_type() const
{
    return "wincall";
}

} // namespace foxxll

#endif // #if FOXXLL_HAVE_WINCALL_FILE

/**************************************************************************/
