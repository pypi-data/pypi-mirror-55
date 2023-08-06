/***************************************************************************
 *  tests/mng/test_block_manager.cpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2002 Roman Dementiev <dementiev@mpi-sb.mpg.de>
 *  Copyright (C) 2018 Manuel Penschuck <foxxll@manuel.jetzt>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

//! \example mng/test_mng.cpp
//! This is an example of use of completion handlers, \c foxxll::block_manager, and
//! \c foxxll::typed_block

#include <iostream>
#include <memory>
#include <vector>

#include <tlx/die.hpp>
#include <tlx/logger.hpp>

#include <foxxll/io.hpp>
#include <foxxll/mng.hpp>

constexpr size_t block_size = 512 * 1024;

struct MyType
{
    size_t integer;
    //char chars[4];
    ~MyType() { }
};

struct my_handler
{
    void operator () (foxxll::request* req, bool /* success */)
    {
        LOG1 << req << " done, type=" << req->io_type();
    }
};

template class foxxll::typed_block<block_size, int>;    // forced instantiation
template class foxxll::typed_block<block_size, MyType>; // forced instantiation

using block_type = foxxll::typed_block<block_size, MyType>;

int main()
{
    LOG1 << sizeof(MyType) << " " << (block_size % sizeof(MyType));
    LOG1 << sizeof(block_type) << " " << block_size;

    constexpr size_t nblocks = 2;
    foxxll::BIDArray<block_size> bids(nblocks);

    std::unique_ptr<foxxll::request_ptr[]> reqs(new foxxll::request_ptr[nblocks]);
    foxxll::block_manager* bm = foxxll::block_manager::get_instance();
    bm->new_blocks(foxxll::striping(), bids.begin(), bids.end());

    std::unique_ptr<block_type[]> block(new block_type[nblocks]);

    LOG1 << std::hex;
    LOG1 << "Allocated block address    : " << reinterpret_cast<size_t>(block.get());
    LOG1 << "Allocated block address + 1: " << reinterpret_cast<size_t>(block.get() + 1);
    LOG1 << std::dec;

    for (size_t i = 0; i < nblocks; i++) {
        for (size_t j = 0; j < block_type::size; ++j) {
            block[i].elem[j].integer = i + j;
        }
    }

    for (size_t i = 0; i < nblocks; ++i)
        reqs[i] = block[i].write(bids[i], my_handler());

    LOG1 << "Waiting";
    wait_all(reqs.get(), nblocks);

    for (size_t i = 0; i < nblocks; i++) {
        for (size_t j = 0; j < block_type::size; ++j) {
            block[i].elem[j].integer = 0xdeadbeaf;
        }
    }

    for (size_t i = 0; i < nblocks; ++i)
    {
        reqs[i] = block[i].read(bids[i], my_handler());
        reqs[i]->wait();
        for (size_t j = 0; j < block_type::size; ++j)
        {
            die_verbose_unless(
                i + j == block[i].elem[j].integer,
                "Error in block " << std::hex << i << " pos: " << j
                                  << " value read: " << block[i].elem[j].integer
            );
        }
    }

    bm->delete_blocks(bids.begin(), bids.end());
}

/**************************************************************************/
