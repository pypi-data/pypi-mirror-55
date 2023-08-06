/***************************************************************************
 *  foxxll/mng/buf_writer.hpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2002-2004 Roman Dementiev <dementiev@mpi-sb.mpg.de>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#ifndef FOXXLL_MNG_BUF_WRITER_HEADER
#define FOXXLL_MNG_BUF_WRITER_HEADER

#include <queue>
#include <vector>

#include <foxxll/io/disk_queues.hpp>
#include <foxxll/io/request_operations.hpp>

#include <tlx/define/likely.hpp>

namespace foxxll {

//! \defgroup foxxll_schedlayer Block Scheduling Sublayer
//! \ingroup foxxll_mnglayer
//! Group of classes which help in scheduling
//! sequences of read and write requests
//! via prefetching and buffered writing
//! \{

//! Encapsulates asynchronous buffered block writing engine.
//!
//! \c buffered_writer overlaps I/Os with filling of output buffer.
template <typename BlockType>
class buffered_writer
{
    constexpr static bool debug = false;
    using block_type = BlockType;
    using bid_type = typename block_type::bid_type;

protected:
    const size_t nwriteblocks;
    block_type* write_buffers;
    bid_type* write_bids;
    request_ptr* write_reqs;
    const size_t writebatchsize;

    std::vector<size_t> free_write_blocks;            // contains free write blocks
    std::vector<size_t> busy_write_blocks;            // blocks that are in writing, notice that if block is not in free_
    // an not in busy then block is not yet filled

    struct batch_entry
    {
        int64_t offset;
        size_t ibuffer;
        batch_entry(int64_t o, size_t b) : offset(o), ibuffer(b) { }
    };
    struct batch_entry_cmp
    {
        bool operator () (const batch_entry& a, const batch_entry& b) const
        {
            return (a.offset > b.offset);
        }
    };

    using batch_type = std::priority_queue<batch_entry, std::vector<batch_entry>, batch_entry_cmp>;
    batch_type batch_write_blocks;      // sorted sequence of blocks to write

public:
    //! Constructs an object.
    //! \param write_buf_size number of write buffers to use
    //! \param write_batch_size number of blocks to accumulate in
    //!        order to flush write requests (bulk buffered writing)
    buffered_writer(size_t write_buf_size, size_t write_batch_size)
        : nwriteblocks((write_buf_size > 2) ? write_buf_size : 2),
          writebatchsize(write_batch_size ? write_batch_size : 1)
    {
        write_buffers = new block_type[nwriteblocks];
        write_reqs = new request_ptr[nwriteblocks];

        write_bids = new bid_type[nwriteblocks];

        for (size_t i = 0; i < nwriteblocks; i++)
            free_write_blocks.push_back(i);

        disk_queues::get_instance()->set_priority_op(request_queue::WRITE);
    }

    //! non-copyable: delete copy-constructor
    buffered_writer(const buffered_writer&) = delete;
    //! non-copyable: delete assignment operator
    buffered_writer& operator = (const buffered_writer&) = delete;

    //! Returns free block from the internal buffer pool.
    //! \return pointer to the block from the internal buffer pool
    block_type * get_free_block()
    {
        size_t ibuffer;
        for (auto it = busy_write_blocks.begin(); it != busy_write_blocks.end(); ++it)
        {
            if (write_reqs[ibuffer = (*it)]->poll())
            {
                busy_write_blocks.erase(it);
                free_write_blocks.push_back(ibuffer);

                break;
            }
        }
        if (TLX_UNLIKELY(free_write_blocks.empty()))
        {
            size_t size = busy_write_blocks.size();
            request_ptr* reqs = new request_ptr[size];
            size_t i = 0;
            for ( ; i < size; ++i)
            {
                reqs[i] = write_reqs[busy_write_blocks[i]];
            }
            size_t completed = wait_any(reqs, size);
            size_t completed_global = busy_write_blocks[completed];
            delete[] reqs;
            busy_write_blocks.erase(busy_write_blocks.begin() + completed);

            return (write_buffers + completed_global);
        }
        ibuffer = free_write_blocks.back();
        free_write_blocks.pop_back();

        return (write_buffers + ibuffer);
    }
    //! Submits block for writing.
    //! \param filled_block pointer to the block
    //! \remark parameter \c filled_block must be value returned by \c get_free_block() or \c write() methods
    //! \param bid block identifier, a place to write data of the \c filled_block
    //! \return pointer to the new free block from the pool
    block_type * write(block_type* filled_block, const bid_type& bid)          // writes filled_block and returns a new block
    {
        if (batch_write_blocks.size() >= writebatchsize)
        {
            // flush batch
            while (!batch_write_blocks.empty())
            {
                size_t ibuffer = batch_write_blocks.top().ibuffer;
                batch_write_blocks.pop();

                if (write_reqs[ibuffer].valid())
                    write_reqs[ibuffer]->wait();

                write_reqs[ibuffer] = write_buffers[ibuffer].write(write_bids[ibuffer]);

                busy_write_blocks.push_back(ibuffer);
            }
        }
        TLX_LOG << "Adding write request to batch";

        size_t ibuffer = filled_block - write_buffers;
        write_bids[ibuffer] = bid;
        batch_write_blocks.push(batch_entry(bid.offset, ibuffer));

        return get_free_block();
    }
    //! Flushes not yet written buffers.
    void flush()
    {
        size_t ibuffer;
        while (!batch_write_blocks.empty())
        {
            ibuffer = batch_write_blocks.top().ibuffer;
            batch_write_blocks.pop();

            if (write_reqs[ibuffer].valid())
                write_reqs[ibuffer]->wait();

            write_reqs[ibuffer] = write_buffers[ibuffer].write(write_bids[ibuffer]);

            busy_write_blocks.push_back(ibuffer);
        }
        for (auto it = busy_write_blocks.begin(); it != busy_write_blocks.end(); it++)
        {
            ibuffer = *it;
            write_reqs[ibuffer]->wait();
        }

        assert(batch_write_blocks.empty());
        free_write_blocks.clear();
        busy_write_blocks.clear();

        for (size_t i = 0; i < nwriteblocks; i++)
            free_write_blocks.push_back(i);
    }

    //! Flushes not yet written buffers and frees used memory.
    ~buffered_writer()
    {
        size_t ibuffer;
        while (!batch_write_blocks.empty())
        {
            ibuffer = batch_write_blocks.top().ibuffer;
            batch_write_blocks.pop();

            if (write_reqs[ibuffer].valid())
                write_reqs[ibuffer]->wait();

            write_reqs[ibuffer] = write_buffers[ibuffer].write(write_bids[ibuffer]);

            busy_write_blocks.push_back(ibuffer);
        }
        for (auto it = busy_write_blocks.begin(); it != busy_write_blocks.end(); it++)
        {
            ibuffer = *it;
            write_reqs[ibuffer]->wait();
        }

        delete[] write_reqs;
        delete[] write_buffers;
        delete[] write_bids;
    }
};

//! \}

} // namespace foxxll

#endif // !FOXXLL_MNG_BUF_WRITER_HEADER

/**************************************************************************/
