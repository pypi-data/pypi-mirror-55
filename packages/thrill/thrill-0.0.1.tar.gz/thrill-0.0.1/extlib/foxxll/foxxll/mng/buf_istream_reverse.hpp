/***************************************************************************
 *  foxxll/mng/buf_istream_reverse.hpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2002-2004 Roman Dementiev <dementiev@mpi-sb.mpg.de>
 *  Copyright (C) 2013 Timo Bingmann <tb@panthema.net>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#ifndef FOXXLL_MNG_BUF_ISTREAM_REVERSE_HEADER
#define FOXXLL_MNG_BUF_ISTREAM_REVERSE_HEADER

#include <algorithm>

#include <foxxll/mng/async_schedule.hpp>
#include <foxxll/mng/bid.hpp>
#include <foxxll/mng/block_prefetcher.hpp>
#include <foxxll/mng/config.hpp>

#include <tlx/define/likely.hpp>

namespace foxxll {

//! \addtogroup foxxll_schedlayer
//! \{

// a paranoid check
#define BUF_ISTREAM_CHECK_END

//! Buffered input stream, reading the items in the blocks in reverse order.
//!
//! Reads data records from the stream of blocks in reverse order.
//! \remark Reading performed in the background, i.e. with overlapping of I/O and computation
template <typename BlockType, typename BidIteratorType>
class buf_istream_reverse
{
public:
    using block_type = BlockType;
    using bid_iterator_type = BidIteratorType;

    //-tb note that we redefine the BID type here, because there is no way to
    //-derive it from BidIteratorType (which is usually just a POD pointer).
    using bid_vector_type = BIDArray<block_type::raw_size>;

private:
    buf_istream_reverse() { }

protected:
    using prefetcher_type = block_prefetcher<block_type, typename bid_vector_type::iterator>;
    prefetcher_type* prefetcher;
    size_t current_elem;
    block_type* current_blk;
    size_t* prefetch_seq;
#ifdef BUF_ISTREAM_CHECK_END
    bool not_finished;
#endif
    bid_vector_type bids_;

public:
    using reference = typename block_type::reference;
    using self_type = buf_istream_reverse<block_type, bid_iterator_type>;

    //! Constructs input stream object, reading [first,last) blocks in reverse.
    //! \param begin \c bid_iterator pointing to the first block of the stream
    //! \param end \c bid_iterator pointing to the ( \b last + 1 ) block of the stream
    //! \param nbuffers number of buffers for internal use
    buf_istream_reverse(bid_iterator_type begin, bid_iterator_type end, size_t nbuffers)
        : current_elem(0),
#ifdef BUF_ISTREAM_CHECK_END
          not_finished(true),
#endif
          bids_(end - begin)
    {
        // copy list of bids in reverse
        std::reverse_copy(begin, end, bids_.begin());

        // calculate prefetch sequence
        const size_t ndisks = config::get_instance()->disks_number();
        const size_t mdevid = config::get_instance()->max_device_id();

        prefetch_seq = new size_t[bids_.size()];

        // optimal schedule
        nbuffers = std::max(2 * ndisks, nbuffers - 1);
        compute_prefetch_schedule(
            bids_.begin(), bids_.end(), prefetch_seq,
            nbuffers, mdevid
        );

        // create stream prefetcher
        prefetcher = new prefetcher_type(bids_.begin(), bids_.end(), prefetch_seq, nbuffers);

        // fetch block: last in sequence
        current_blk = prefetcher->pull_block();
        current_elem = block_type::size - 1;
    }

    //! non-copyable: delete copy-constructor
    buf_istream_reverse(const buf_istream_reverse&) = delete;
    //! non-copyable: delete assignment operator
    buf_istream_reverse& operator = (const buf_istream_reverse&) = delete;

    //! Input stream operator, reads in \c record.
    //! \param record reference to the block record type,
    //!        contains value of the next record in the stream after the call of the operator
    //! \return reference to itself (stream object)
    self_type& operator >> (reference record)
    {
#ifdef BUF_ISTREAM_CHECK_END
        assert(not_finished);
#endif

        record = current_blk->elem[current_elem];

        if (TLX_UNLIKELY(current_elem == 0))
        {
            current_elem = block_type::size - 1;
#ifdef BUF_ISTREAM_CHECK_END
            not_finished = prefetcher->block_consumed(current_blk);
#else
            prefetcher->block_consumed(current_blk);
#endif
        }
        else
        {
            current_elem--;
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

    //! Moves to the _previous_ record in the stream.
    //! \return reference to itself after the advance
    self_type& operator ++ ()
    {
#ifdef BUF_ISTREAM_CHECK_END
        assert(not_finished);
#endif

        if (TLX_UNLIKELY(current_elem == 0))
        {
            current_elem = block_type::size - 1;
#ifdef BUF_ISTREAM_CHECK_END
            not_finished = prefetcher->block_consumed(current_blk);
#else
            prefetcher->block_consumed(current_blk);
#endif
        }
        else
        {
            current_elem--;
        }

        return *this;
    }

    //! Frees used internal objects.
    ~buf_istream_reverse()
    {
        delete prefetcher;
        delete[] prefetch_seq;
    }
};

//! \}

} // namespace foxxll

#endif // !FOXXLL_MNG_BUF_ISTREAM_REVERSE_HEADER

/**************************************************************************/
