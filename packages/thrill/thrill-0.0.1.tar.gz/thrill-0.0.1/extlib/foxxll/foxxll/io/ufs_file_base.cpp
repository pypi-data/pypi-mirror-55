/***************************************************************************
 *  foxxll/io/ufs_file_base.cpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2002, 2005, 2008 Roman Dementiev <dementiev@mpi-sb.mpg.de>
 *  Copyright (C) 2008 Ilja Andronov <sni4ok@yandex.ru>
 *  Copyright (C) 2008-2010 Andreas Beckmann <beckmann@cs.uni-frankfurt.de>
 *  Copyright (C) 2009 Johannes Singler <singler@ira.uka.de>
 *  Copyright (C) 2013 Timo Bingmann <tb@panthema.net>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#include <tlx/logger/core.hpp>

#include <foxxll/common/error_handling.hpp>
#include <foxxll/common/exceptions.hpp>
#include <foxxll/config.hpp>
#include <foxxll/io/file.hpp>
#include <foxxll/io/ufs_file_base.hpp>
#include <foxxll/io/ufs_platform.hpp>

namespace foxxll {

const char* ufs_file_base::io_type() const
{
    return "ufs_base";
}

ufs_file_base::ufs_file_base(const std::string& filename, int mode)
    : file_des_(-1), mode_(mode), filename_(filename)
{
    int flags = 0;

    if (mode & RDONLY)
    {
        flags |= O_RDONLY;
    }

    if (mode & WRONLY)
    {
        flags |= O_WRONLY;
    }

    if (mode & RDWR)
    {
        flags |= O_RDWR;
    }

    if (mode & CREAT)
    {
        flags |= O_CREAT;
    }

    if (mode & TRUNC)
    {
        flags |= O_TRUNC;
    }

    if ((mode & DIRECT) || (mode & REQUIRE_DIRECT))
    {
#ifdef __APPLE__
        // no additional open flags are required for Mac OS X
#elif !FOXXLL_DIRECT_IO_OFF
        flags |= O_DIRECT;
#else
        if (mode & REQUIRE_DIRECT) {
            TLX_LOG1 << "Error: open()ing " << filename_
                     << " with DIRECT mode required, but the system does not support it.";
            file_des_ = -1;
            return;
        }
        else {
            TLX_LOG1 << "Warning: open()ing " << filename_
                     << " without DIRECT mode, as the system does not support it.";
        }
#endif
    }

    if (mode & SYNC)
    {
        flags |= O_RSYNC;
        flags |= O_DSYNC;
        flags |= O_SYNC;
    }

#if FOXXLL_WINDOWS
    flags |= O_BINARY;                     // the default in MS is TEXT mode
#endif

#if FOXXLL_WINDOWS || defined(__MINGW32__)
    const int perms = S_IREAD | S_IWRITE;
#else
    const int perms = S_IREAD | S_IWRITE | S_IRGRP | S_IWGRP;
#endif

    if ((file_des_ = ::open(filename_.c_str(), flags, perms)) >= 0)
    {
        need_alignment_ = (mode & DIRECT) != 0;
        _after_open();
        return;
    }

#if !FOXXLL_DIRECT_IO_OFF
    if ((mode & DIRECT) && !(mode & REQUIRE_DIRECT) && errno == EINVAL)
    {
        TLX_LOG1 << "open() error on path=" << filename_
                 << " flags=" << flags << ", retrying without O_DIRECT.";

        flags &= ~O_DIRECT;
        mode &= ~DIRECT;

        if ((file_des_ = ::open(filename_.c_str(), flags, perms)) >= 0)
        {
            _after_open();
            return;
        }
    }
#endif

    FOXXLL_THROW_ERRNO(
        io_error, "open() rc=" << file_des_
                               << " path=" << filename_ << " flags=" << flags
    );
}

ufs_file_base::~ufs_file_base()
{
    close();
}

void ufs_file_base::_after_open()
{
    // stat file type
#if FOXXLL_WINDOWS || defined(__MINGW32__)
    struct _stat64 st;
    FOXXLL_THROW_ERRNO_NE_0(
        ::_fstat64(file_des_, &st), io_error,
        "_fstat64() path=" << filename_ << " fd=" << file_des_
    );
#else
    struct stat st;
    FOXXLL_THROW_ERRNO_NE_0(
        ::fstat(file_des_, &st), io_error,
        "fstat() path=" << filename_ << " fd=" << file_des_
    );
#endif
    is_device_ = S_ISBLK(st.st_mode) ? true : false;

#ifdef __APPLE__
    if (mode_ & REQUIRE_DIRECT) {
        FOXXLL_THROW_ERRNO_NE_0(
            fcntl(file_des_, F_NOCACHE, 1), io_error,
            "fcntl() path=" << filename_ << " fd=" << file_des_
        );
        FOXXLL_THROW_ERRNO_NE_0(
            fcntl(file_des_, F_RDAHEAD, 0), io_error,
            "fcntl() path=" << filename_ << " fd=" << file_des_
        );
    }
    else if (mode_ & DIRECT) {
        if (fcntl(file_des_, F_NOCACHE, 1) != 0) {
            TLX_LOG1
                << "fcntl(fd,F_NOCACHE,1) failed on path=" << filename_
                << " fd=" << file_des_ << " : " << strerror(errno);
        }
        if (fcntl(file_des_, F_RDAHEAD, 0) != 0) {
            TLX_LOG1 << "fcntl(fd,F_RDAHEAD,0) failed on path=" << filename_
                     << " fd=" << file_des_ << " : " << strerror(errno);
        }
    }
#endif

    // successfully opened file descriptor
    if (!(mode_ & NO_LOCK))
        lock();
}

void ufs_file_base::close()
{
    std::unique_lock<std::mutex> fd_lock(fd_mutex_);

    if (file_des_ == -1)
        return;

    if (::close(file_des_) < 0)
        FOXXLL_THROW_ERRNO(io_error, "close() fd=" << file_des_);

    file_des_ = -1;
}

void ufs_file_base::lock()
{
#if FOXXLL_WINDOWS || defined(__MINGW32__)
    // not yet implemented
#else
    std::unique_lock<std::mutex> fd_lock(fd_mutex_);
    struct flock lock_struct;
    lock_struct.l_type = static_cast<short>(mode_ & RDONLY ? F_RDLCK : F_RDLCK | F_WRLCK);
    lock_struct.l_whence = SEEK_SET;
    lock_struct.l_start = 0;
    lock_struct.l_len = 0; // lock all bytes
    if ((::fcntl(file_des_, F_SETLK, &lock_struct)) < 0)
        FOXXLL_THROW_ERRNO(io_error, "fcntl(,F_SETLK,) path=" << filename_ << " fd=" << file_des_);
#endif
}

file::offset_type ufs_file_base::_size()
{
    // We use lseek SEEK_END to find the file size. This works for raw devices
    // (where stat() returns zero), and we need not reset the position because
    // serve() always lseek()s before read/write.

    off_t rc = ::lseek(file_des_, 0, SEEK_END);
    if (rc < 0)
        FOXXLL_THROW_ERRNO(io_error, "lseek(fd,0,SEEK_END) path=" << filename_ << " fd=" << file_des_);

    // return value is already the total size
    return rc;
}

file::offset_type ufs_file_base::size()
{
    std::unique_lock<std::mutex> fd_lock(fd_mutex_);
    return _size();
}

void ufs_file_base::set_size(offset_type newsize)
{
    std::unique_lock<std::mutex> fd_lock(fd_mutex_);
    return _set_size(newsize);
}

void ufs_file_base::_set_size(offset_type newsize)
{
    offset_type cur_size = _size();

    if (!(mode_ & RDONLY) && !is_device_)
    {
#if FOXXLL_WINDOWS || defined(__MINGW32__)
        HANDLE hfile = (HANDLE)::_get_osfhandle(file_des_);
        FOXXLL_THROW_ERRNO_NE_0(
            (hfile == INVALID_HANDLE_VALUE), io_error,
            "_get_osfhandle() path=" << filename_ << " fd=" << file_des_
        );

        LARGE_INTEGER desired_pos;
        desired_pos.QuadPart = newsize;

        if (!SetFilePointerEx(hfile, desired_pos, nullptr, FILE_BEGIN))
            FOXXLL_THROW_WIN_LASTERROR(
                io_error,
                "SetFilePointerEx in ufs_file_base::set_size(..) oldsize=" << cur_size <<
                    " newsize=" << newsize << " "
            );

        if (!SetEndOfFile(hfile))
            FOXXLL_THROW_WIN_LASTERROR(
                io_error,
                "SetEndOfFile oldsize=" << cur_size <<
                    " newsize=" << newsize << " "
            );
#else
        FOXXLL_THROW_ERRNO_NE_0(
            ::ftruncate(file_des_, newsize), io_error,
            "ftruncate() path=" << filename_ << " fd=" << file_des_
        );
#endif
    }

#if !FOXXLL_WINDOWS
    if (newsize > cur_size)
        FOXXLL_THROW_IF(
            ::lseek(file_des_, newsize - 1, SEEK_SET) < 0, io_error,
            "lseek() path=" << filename_ << " fd=" << file_des_ << " pos=" << newsize - 1
        );
#endif
}

void ufs_file_base::close_remove()
{
    close();

    if (is_device_) {
        TLX_LOG1 << "remove() path=" << filename_
                 << " skipped as file is device node";
        return;
    }

    if (::remove(filename_.c_str()) != 0)
        TLX_LOG1 << "remove() error on path=" << filename_
                 << " error=" << strerror(errno);
}

void ufs_file_base::unlink()
{
    if (is_device_) {
        TLX_LOG1 << "unlink() path=" << filename_
                 << " skipped as file is device node";
        return;
    }

    if (::unlink(filename_.c_str()) != 0)
        FOXXLL_THROW_ERRNO(io_error, "unlink() path=" << filename_ << " fd=" << file_des_);
}

bool ufs_file_base::is_device() const
{
    return is_device_;
}

} // namespace foxxll

/**************************************************************************/
