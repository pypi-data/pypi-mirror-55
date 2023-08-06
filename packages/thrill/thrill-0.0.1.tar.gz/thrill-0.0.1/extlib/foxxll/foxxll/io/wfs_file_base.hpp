/***************************************************************************
 *  foxxll/io/wfs_file_base.hpp
 *
 *  Windows file system file base
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2005 Roman Dementiev <dementiev@ira.uka.de>
 *  Copyright (C) 2008, 2010 Andreas Beckmann <beckmann@cs.uni-frankfurt.de>
 *  Copyright (C) 2009, 2010 Johannes Singler <singler@kit.edu>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#ifndef FOXXLL_IO_WFS_FILE_BASE_HEADER
#define FOXXLL_IO_WFS_FILE_BASE_HEADER

#include <foxxll/config.hpp>

#if FOXXLL_WINDOWS

#include <mutex>
#include <string>

#include <foxxll/io/file.hpp>
#include <foxxll/io/request.hpp>

namespace foxxll {

//! \addtogroup foxxll_fileimpl
//! \{

//! Base for Windows file system implementations.
class wfs_file_base : public virtual file
{
protected:
    using HANDLE = void*;

    std::mutex fd_mutex_;  // sequentialize function calls involving file_des_
    HANDLE file_des_;      // file descriptor
    int mode_;             // open mode
    const std::string filename_;
    offset_type bytes_per_sector_;
    bool locked_;
    wfs_file_base(const std::string& filename, int mode);
    offset_type _size();
    void close();

public:
    ~wfs_file_base();
    offset_type size();
    void set_size(offset_type newsize);
    void lock();
    const char * io_type() const;
    void close_remove();
};

//! \}

} // namespace foxxll

#endif // FOXXLL_WINDOWS

#endif // !FOXXLL_IO_WFS_FILE_BASE_HEADER

/**************************************************************************/
