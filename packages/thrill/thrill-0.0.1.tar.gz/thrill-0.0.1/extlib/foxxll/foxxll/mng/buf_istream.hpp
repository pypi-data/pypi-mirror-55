/***************************************************************************
 *  foxxll/mng/buf_istream.hpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2002-2004 Roman Dementiev <dementiev@mpi-sb.mpg.de>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#ifndef FOXXLL_MNG_BUF_ISTREAM_HEADER
#define FOXXLL_MNG_BUF_ISTREAM_HEADER

#include <algorithm>

#include <foxxll/mng/async_schedule.hpp>
#include <foxxll/mng/block_prefetcher.hpp>
#include <foxxll/mng/config.hpp>

#include <tlx/define/likely.hpp>

namespace foxxll {

//! \addtogroup foxxll_schedlayer
//! \{

// a paranoid check
#define BUF_ISTREAM_CHECK_END

//! Buffered input stream.
//!
//! Reads data records from the stream of blocks.
//! \remark Reading performed in the background, i.e. with overlapping of I/O and computation
template <typename BlockType, typename BidIteratorType>
class buf_istream
{
public:
    using block_type = BlockType;
    using bid_iterator_type = BidIteratorType;

private:
    buf_istream() { }

protected:
    using prefetcher_type = block_prefetcher<block_type, bid_iterator_type>;
    prefetcher_type* prefetcher;
    size_t current_elem;
    block_type* current_blk;
    size_t* prefetch_seq;
#ifdef BUF_ISTREAM_CHECK_END
    bool not_finished;
#endif

public:
    using reference = typename block_type::reference;
    using self_type = buf_istream<block_type, bid_iterator_type>;

    //! Constructs input stream object.
    //! \param begin \c bid_iterator pointing to the first block of the stream
    //! \param end \c bid_iterator pointing to the ( \b last + 1 ) block of the stream
    //! \param nbuffers number of buffers for internal use
    buf_istream(bid_iterator_type begin, bid_iterator_type end, size_t nbuffers)
        : current_elem(0)
#ifdef BUF_ISTREAM_CHECK_END
          , not_finished(true)
#endif
    {
        const size_t ndisks = config::get_instance()->disks_number();
        const size_t mdevid = config::get_instance()->max_device_id();
        const size_t seq_length = end - begin;
        prefetch_seq = new size_t[seq_length];

        // obvious schedule
        //for(size_t i = 0; i < seq_length; ++i)
        //      prefetch_seq[i] = i;

        // optimal schedule
        nbuffers = std::max(2 * ndisks, size_t(nbuffers - 1));
        compute_prefetch_schedule(
            begin, end, prefetch_seq,
            nbuffers, mdevid
        );

        prefetcher = new prefetcher_type(begin, end, prefetch_seq, nbuffers);

        current_blk = prefetcher->pull_block();
    }

    //! non-copyable: delete copy-constructor
    buf_istream(const buf_istream&) = delete;
    //! non-copyable: delete assignment operator
    buf_istream& operator = (const buf_istream&) = delete;

    //! Input stream operator, reads in \c record.
    //! \param record reference to the block record type,
    //!        contains value of the next record in the stream after the call of the operator
    //! \return reference to itself (stream object)
    self_type& operator >> (reference record)
    {
#ifdef BUF_ISTREAM_CHECK_END
        assert(not_finished);
#endif

        record = current_blk->elem[current_elem++];

        if (TLX_UNLIKELY(current_elem >= block_type::size))
        {
            current_elem = 0;
#ifdef BUF_ISTREAM_CHECK_END
            not_finished = prefetcher->block_consumed(current_blk);
#else
            prefetcher->block_consumed(current_blk);
#endif
        }

        return (*this);
    }

    //! Returns reference to the current record in the stream.
    reference current()     /* const */
    {
        return current_blk->elem[current_elem];
    }

    //! Returns reference to the current record in the stream.
    reference operator * ()     /* const */
    {
        return current_blk->elem[current_elem];
    }

    //! Moves to the next record in the stream.
    //! \return reference to itself after the advance
    self_type& operator ++ ()
    {
#ifdef BUF_ISTREAM_CHECK_END
        assert(not_finished);
#endif

        current_elem++;

        if (TLX_UNLIKELY(current_elem >= block_type::size))
        {
            current_elem = 0;
#ifdef BUF_ISTREAM_CHECK_END
            not_finished = prefetcher->block_consumed(current_blk);
#else
            prefetcher->block_consumed(current_blk);
#endif
        }
        return *this;
    }

    //! Frees used internal objects.
    ~buf_istream()
    {
        delete prefetcher;
        delete[] prefetch_seq;
    }
};

//! \}

} // namespace foxxll

#endif // !FOXXLL_MNG_BUF_ISTREAM_HEADER

/**************************************************************************/
