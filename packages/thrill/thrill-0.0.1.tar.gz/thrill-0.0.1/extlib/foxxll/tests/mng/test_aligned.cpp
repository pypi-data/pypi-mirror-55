/***************************************************************************
 *  tests/mng/test_aligned.cpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2009 Andreas Beckmann <beckmann@cs.uni-frankfurt.de>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#include <iostream>
#include <vector>

#include <foxxll/mng.hpp>

#define BLOCK_SIZE (512 * 1024)

struct type
{
    int i;
    ~type() { }
};

using block_type = foxxll::typed_block<BLOCK_SIZE, type>;
template class foxxll::typed_block<BLOCK_SIZE, type>; // forced instantiation

void test_typed_block()
{
    block_type* a = new block_type;
    block_type* b = new block_type;
    block_type* A = new block_type[4];
    block_type* B = new block_type[1];
    block_type* C = nullptr;
    C = new block_type[0];
    delete a;
    a = b;
    b = 0;
    //-tb delete of nullptr is a noop
    //delete b;
    delete a;
    delete[] A;
    delete[] B;
    delete[] C;
}

void test_aligned_alloc()
{
    void* p = foxxll::aligned_alloc<1024>(4096);
    void* q = nullptr;
    void* r = foxxll::aligned_alloc<1024>(4096, 42);
    foxxll::aligned_dealloc<1024>(p);
    foxxll::aligned_dealloc<1024>(q);
    foxxll::aligned_dealloc<1024>(r);
}

void test_typed_block_vector()
{
    std::vector<block_type> v1(2);
    std::vector<block_type, foxxll::new_alloc<block_type> > v2(2);
}

int main()
{
    test_typed_block();
    test_aligned_alloc();
    test_typed_block_vector();

    return 0;
}

/**************************************************************************/
