/***************************************************************************
 *  tests/mng/test_bmlayer.cpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2007 Roman Dementiev <dementiev@ira.uka.de>
 *  Copyright (C) 2009 Andreas Beckmann <beckmann@cs.uni-frankfurt.de>
 *  Copyright (C) 2013 Timo Bingmann <tb@panthema.net>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#include <iostream>

#include <tlx/die.hpp>
#include <tlx/logger.hpp>

#include <foxxll/io/request_operations.hpp>
#include <foxxll/mng/block_manager.hpp>
#include <foxxll/mng/buf_istream.hpp>
#include <foxxll/mng/buf_ostream.hpp>
#include <foxxll/mng/prefetch_pool.hpp>
#include <foxxll/mng/typed_block.hpp>

static const size_t test_block_size = 1024 * 512;

struct MyType
{
    size_t integer;
    char chars[5];
};

struct my_handler
{
    void operator () (foxxll::request* req, bool /* success */)
    {
        LOG1 << req << " done, type=" << req->io_type();
    }
};

using block_type = foxxll::typed_block<test_block_size, MyType>;

void testIO()
{
    const unsigned nblocks = 2;
    foxxll::BIDArray<test_block_size> bids(nblocks);
    std::vector<int> disks(nblocks, 2);
    foxxll::request_ptr* reqs = new foxxll::request_ptr[nblocks];
    foxxll::block_manager* bm = foxxll::block_manager::get_instance();
    bm->new_blocks(foxxll::striping(), bids.begin(), bids.end());

    block_type* block = new block_type;
    LOG1 << std::hex;
    LOG1 << "Allocated block address    : " << reinterpret_cast<size_t>(block);
    LOG1 << "Allocated block address + 1: " << reinterpret_cast<size_t>(block + 1);
    LOG1 << std::dec;
    size_t i = 0;
    for (i = 0; i < block_type::size; ++i)
    {
        block->elem[i].integer = i;
        //memcpy (block->elem[i].chars, "STXXL", 4);
    }
    for (i = 0; i < nblocks; ++i)
        reqs[i] = block->write(bids[i], my_handler());

    LOG1 << "Waiting";
    foxxll::wait_all(reqs, nblocks);

    for (i = 0; i < nblocks; ++i)
    {
        reqs[i] = block->read(bids[i], my_handler());
        reqs[i]->wait();
        for (size_t j = 0; j < block_type::size; ++j)
        {
            die_unless(j == block->elem[j].integer);
        }
    }

    bm->delete_blocks(bids.begin(), bids.end());

    delete[] reqs;
    delete block;
}

void testIO2()
{
    using block_type = foxxll::typed_block<128* 1024, double>;
    std::vector<block_type::bid_type> bids(32);
    std::vector<foxxll::request_ptr> requests;
    foxxll::block_manager* bm = foxxll::block_manager::get_instance();
    bm->new_blocks(foxxll::striping(), bids.begin(), bids.end());
    block_type* blocks = new block_type[32];
    int vIndex;
    for (vIndex = 0; vIndex < 32; ++vIndex) {
        for (size_t vIndex2 = 0; vIndex2 < block_type::size; ++vIndex2) {
            blocks[vIndex][vIndex2] = double(vIndex2);
        }
    }
    for (vIndex = 0; vIndex < 32; ++vIndex) {
        requests.push_back(blocks[vIndex].write(bids[vIndex]));
    }
    foxxll::wait_all(requests.begin(), requests.end());
    bm->delete_blocks(bids.begin(), bids.end());
    delete[] blocks;
}

void testPrefetchPool()
{
    foxxll::prefetch_pool<block_type> pool(2);
    pool.resize(10);
    pool.resize(5);
    block_type* blk = new block_type;
    block_type::bid_type bid;
    foxxll::block_manager::get_instance()->new_block(foxxll::single_disk(), bid);
    pool.hint(bid);
    pool.read(blk, bid)->wait();
    delete blk;
}

void testWritePool()
{
    foxxll::write_pool<block_type> pool(100);
    pool.resize(10);
    pool.resize(5);
    block_type* blk = new block_type;
    block_type::bid_type bid;
    foxxll::block_manager::get_instance()->new_block(foxxll::single_disk(), bid);
    pool.write(blk, bid);
}

using block_type1 = foxxll::typed_block<test_block_size, int>;
using buf_ostream_type = foxxll::buf_ostream<block_type1, foxxll::BIDArray<test_block_size>::iterator>;
using buf_istream_type = foxxll::buf_istream<block_type1, foxxll::BIDArray<test_block_size>::iterator>;

void testStreams()
{
    const unsigned nblocks = 64;
    const unsigned nelements = nblocks * block_type1::size;
    foxxll::BIDArray<test_block_size> bids(nblocks);

    foxxll::block_manager* bm = foxxll::block_manager::get_instance();
    bm->new_blocks(foxxll::striping(), bids.begin(), bids.end());
    {
        buf_ostream_type out(bids.begin(), 2);
        for (unsigned i = 0; i < nelements; i++)
            out << i;
    }
    {
        buf_istream_type in(bids.begin(), bids.end(), 2);
        for (unsigned i = 0; i < nelements; i++)
        {
            int value;
            in >> value;
            die_unless(value == int(i));
        }
    }
    bm->delete_blocks(bids.begin(), bids.end());
}

int main()
{
    testIO();
    testIO2();
    testPrefetchPool();
    testWritePool();
    testStreams();

    foxxll::block_manager* bm = foxxll::block_manager::get_instance();
    LOG1 << "block_manager total allocation: " << bm->total_allocation();
    LOG1 << "block_manager current allocation: " << bm->current_allocation();
    LOG1 << "block_manager maximum allocation: " << bm->maximum_allocation();
}

/**************************************************************************/
