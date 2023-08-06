/***************************************************************************
 *  foxxll/io/request_interface.hpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2002 Roman Dementiev <dementiev@mpi-sb.mpg.de>
 *  Copyright (C) 2008, 2009, 2011 Andreas Beckmann <beckmann@cs.uni-frankfurt.de>
 *  Copyright (C) 2009 Johannes Singler <singler@ira.uka.de>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#ifndef FOXXLL_IO_REQUEST_INTERFACE_HEADER
#define FOXXLL_IO_REQUEST_INTERFACE_HEADER

#include <ostream>

#include <foxxll/common/types.hpp>

namespace foxxll {

//! \addtogroup foxxll_reqlayer
//! \{

class onoff_switch;

//! Functional interface of a request.
//!
//! Since all library I/O operations are asynchronous,
//! one needs to keep track of their status:
//! e.g. whether an I/O operation completed or not.
class request_interface
{
public:
    //! type for offsets within a file
    using offset_type = uint64_t;
    //! type for block transfer sizes
    using size_type = size_t;

    enum read_or_write { READ, WRITE };

public:
    virtual bool add_waiter(onoff_switch* sw) = 0;
    virtual void delete_waiter(onoff_switch* sw) = 0;

protected:
    virtual void notify_waiters() = 0;

protected:
    virtual void completed(bool canceled) = 0;

public:
    request_interface() = default;

    //! non-copyable: delete copy-constructor
    request_interface(const request_interface&) = delete;
    //! non-copyable: delete assignment operator
    request_interface& operator = (const request_interface&) = delete;

    virtual ~request_interface() { }

    //! Suspends calling thread until completion of the request.
    virtual void wait(bool measure_time = true) = 0;

    /*!
     * Cancel a request.
     *
     * The request is canceled unless already being processed.  However,
     * cancelation cannot be guaranteed.  Canceled requests must still be waited
     * for in order to ensure correct operation.  If the request was canceled
     * successfully, the completion handler will not be called.
     *
     * \return \c true iff the request was canceled successfully
     */
    virtual bool cancel() = 0;

    //! Polls the status of the request.
    //! \return \c true if request is completed, otherwise \c false
    virtual bool poll() = 0;

    /*!
     * Identifies the type of I/O implementation.
     *
     * \return pointer to null terminated string of characters, containing the
     * name of I/O implementation
     */
    virtual const char * io_type() const = 0;

    //! Dumps properties of a request.
    virtual std::ostream & print(std::ostream& out) const = 0;
};

//! \}

} // namespace foxxll

#endif // !FOXXLL_IO_REQUEST_INTERFACE_HEADER

/**************************************************************************/
