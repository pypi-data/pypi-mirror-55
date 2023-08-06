/*******************************************************************************
 * tests/core/reduce_post_phase_test.cpp
 *
 * Part of Project Thrill - http://project-thrill.org
 *
 * Copyright (C) 2016 Timo Bingmann <tb@panthema.net>
 * Copyright (C) 2017 Tim Zeitz <dev.tim.zeitz@gmail.com>
 *
 * All rights reserved. Published under the BSD-2 license in the LICENSE file.
 ******************************************************************************/

#include <thrill/core/reduce_by_hash_post_phase.hpp>
#include <thrill/core/reduce_by_index_post_phase.hpp>

#include <gtest/gtest.h>

#include <algorithm>
#include <functional>
#include <utility>
#include <vector>

using namespace thrill;

struct MyStruct {
    size_t key, value;

    bool operator < (const MyStruct& b) const { return key < b.key; }

    friend std::ostream& operator << (std::ostream& os, const MyStruct& c) {
        return os << '(' << c.key << ',' << c.value << ')';
    }
};

/******************************************************************************/

template <core::ReduceTableImpl table_impl>
static void TestAddMyStructByHash(Context& ctx) {
    static constexpr bool debug = false;
    static constexpr size_t mod_size = 601;
    static constexpr size_t test_size = mod_size * 100;
    static constexpr size_t val_size = test_size / mod_size;

    auto key_ex = [](const MyStruct& in) {
                      return in.key % mod_size;
                  };

    auto red_fn = [](const MyStruct& in1, const MyStruct& in2) {
                      return MyStruct {
                          in1.key, in1.value + in2.value
                      };
                  };

    // collect all items
    std::vector<MyStruct> result;

    auto emit_fn = [&result](const MyStruct& in) {
                       result.emplace_back(in);
                   };

    using Phase = core::ReduceByHashPostPhase<
        MyStruct, size_t, MyStruct,
        decltype(key_ex), decltype(red_fn), decltype(emit_fn),
        /* VolatileKey */ false,
        core::DefaultReduceConfigSelect<table_impl> >;

    Phase phase(ctx, 0, key_ex, red_fn, emit_fn);
    phase.Initialize(/* limit_memory_bytes */ 64 * 1024);

    for (size_t i = 0; i < test_size; ++i) {
        phase.Insert(MyStruct { i, i / mod_size });
    }

    phase.PushData(/* consume */ true);

    // check result
    std::sort(result.begin(), result.end());

    ASSERT_EQ(mod_size, result.size());

    for (size_t i = 0; i < result.size(); ++i) {
        LOG << "result[" << i << "] = " << result[i] << " =? "
            << val_size * (val_size - 1) / 2;
    }

    for (size_t i = 0; i < result.size(); ++i) {
        LOG << "result[" << i << "] = " << result[i] << " =? "
            << val_size * (val_size - 1) / 2;
        ASSERT_EQ(i, result[i].key);
        ASSERT_EQ(val_size * (val_size - 1) / 2, result[i].value);
    }
}

TEST(ReduceHashPhase, BucketAddMyStructByHash) {
    api::RunLocalSameThread(
        [](Context& ctx) {
            TestAddMyStructByHash<core::ReduceTableImpl::BUCKET>(ctx);
        });
}

TEST(ReduceHashPhase, OldProbingAddMyStructByHash) {
    api::RunLocalSameThread(
        [](Context& ctx) {
            TestAddMyStructByHash<core::ReduceTableImpl::OLD_PROBING>(ctx);
        });
}

TEST(ReduceHashPhase, ProbingAddMyStructByHash) {
    api::RunLocalSameThread(
        [](Context& ctx) {
            TestAddMyStructByHash<core::ReduceTableImpl::PROBING>(ctx);
        });
}

/******************************************************************************/

TEST(ReduceHashPhase, PostReduceByIndex) {
    static constexpr bool debug = false;

    using IndexMap = core::ReduceByIndex<size_t>;

    IndexMap imap(0, 601);
    size_t num_partitions = 32;
    size_t num_buckets = 256;
    size_t num_buckets_per_partition = num_buckets / num_partitions;

    for (size_t key = 0; key < 601; ++key) {
        typename IndexMap::Result b
            = imap(key,
                   num_partitions, num_buckets_per_partition, num_buckets);

        sLOG << "imap" << key << "->"
             << "part" << b.partition_id
             << "global" << b.global_index
             << "local" << b.local_index(num_buckets_per_partition);

        die_unless(b.partition_id < num_partitions);
        die_unless(b.global_index < num_buckets);

        size_t inv = imap.inverse(b.global_index, num_buckets);

        sLOG << "inv" << b.global_index << "->" << inv;
        die_unless(inv <= key);
    }
}

/******************************************************************************/

template <core::ReduceTableImpl table_impl>
static void TestAddMyStructByIndex(Context& ctx) {
    static constexpr bool debug = false;
    static constexpr size_t mod_size = 601;
    static constexpr size_t test_size = mod_size * 100;
    static constexpr size_t val_size = test_size / mod_size;

    auto key_ex = [](const MyStruct& in) {
                      return in.key % mod_size;
                  };

    auto red_fn = [](const MyStruct& in1, const MyStruct& in2) {
                      return MyStruct {
                          in1.key, in1.value + in2.value
                      };
                  };

    // collect all items
    std::vector<MyStruct> result;

    auto emit_fn = [&result](const MyStruct& in) {
                       result.emplace_back(in);
                   };

    using Phase = core::ReduceByIndexPostPhase<
        MyStruct, size_t, MyStruct,
        decltype(key_ex), decltype(red_fn), decltype(emit_fn), false,
        core::DefaultReduceConfigSelect<table_impl> >;

    Phase phase(ctx, 0, key_ex, red_fn, emit_fn,
                typename Phase::ReduceConfig(),
                /* neutral_element */ MyStruct { 0, 0 });
    phase.SetRange(common::Range(0, mod_size));
    phase.Initialize(/* limit_memory_bytes */ 64 * 1024);

    for (size_t i = 0; i < test_size; ++i) {
        phase.Insert(MyStruct { i, i / mod_size });
    }

    phase.PushData(/* consume */ true);

    // check result
    ASSERT_EQ(mod_size, result.size());

    for (size_t i = 0; i < result.size(); ++i) {
        LOG << "result[" << i << "] = " << result[i] << " =? "
            << val_size * (val_size - 1) / 2;
    }

    for (size_t i = 0; i < result.size(); ++i) {
        LOG << "result[" << i << "] = " << result[i] << " =? "
            << val_size * (val_size - 1) / 2;
        ASSERT_EQ(i, result[i].key);
        ASSERT_EQ(val_size * (val_size - 1) / 2, result[i].value);
    }
}

TEST(ReduceHashPhase, BucketAddMyStructByIndex) {
    api::RunLocalSameThread(
        [](Context& ctx) {
            TestAddMyStructByIndex<core::ReduceTableImpl::BUCKET>(ctx);
        });
}

TEST(ReduceHashPhase, OldProbingAddMyStructByIndex) {
    api::RunLocalSameThread(
        [](Context& ctx) {
            TestAddMyStructByIndex<core::ReduceTableImpl::OLD_PROBING>(ctx);
        });
}

TEST(ReduceHashPhase, ProbingAddMyStructByIndex) {
    api::RunLocalSameThread(
        [](Context& ctx) {
            TestAddMyStructByIndex<core::ReduceTableImpl::PROBING>(ctx);
        });
}

/******************************************************************************/

template <core::ReduceTableImpl table_impl>
static void TestAddMyStructByIndexWithHoles(Context& ctx) {
    static constexpr bool debug = false;
    static constexpr size_t mod_size = 600;
    static constexpr size_t test_size = mod_size * 100;
    static constexpr size_t val_size = test_size / mod_size;

    auto key_ex = [](const MyStruct& in) {
                      return (in.key * 2) % mod_size;
                  };

    auto red_fn = [](const MyStruct& in1, const MyStruct& in2) {
                      return MyStruct {
                          in1.key, in1.value + in2.value
                      };
                  };

    // collect all items
    std::vector<MyStruct> result;

    auto emit_fn = [&result](const MyStruct& in) {
                       result.emplace_back(in);
                   };

    using Phase = core::ReduceByIndexPostPhase<
        MyStruct, size_t, MyStruct,
        decltype(key_ex), decltype(red_fn), decltype(emit_fn), false,
        core::DefaultReduceConfigSelect<table_impl> >;

    Phase phase(ctx, 0, key_ex, red_fn, emit_fn,
                typename Phase::ReduceConfig(),
                /* neutral_element */ MyStruct { 0, 0 });
    phase.SetRange(common::Range(0, mod_size));
    phase.Initialize(/* limit_memory_bytes */ 64 * 1024);

    for (size_t i = 0; i < test_size; ++i) {
        phase.Insert(MyStruct { i, i / mod_size });
    }

    phase.PushData(/* consume */ true);

    // check result
    ASSERT_EQ(mod_size, result.size());

    for (size_t i = 0; i < result.size(); ++i) {
        size_t correct = i % 2 == 0 ? val_size * (val_size - 1) : 0;

        LOG << "result[" << i << "] = " << result[i] << " =? " << correct;
    }

    for (size_t i = 0; i < result.size(); ++i) {
        size_t correct = i % 2 == 0 ? val_size * (val_size - 1) : 0;

        LOG << "result[" << i << "] = " << result[i] << " =? " << correct;

        ASSERT_EQ(i % 2 == 0 ? i / 2 : 0, result[i].key);
        ASSERT_EQ(correct, result[i].value);
    }
}

TEST(ReduceHashPhase, BucketAddMyStructByIndexWithHoles) {
    api::RunLocalSameThread(
        [](Context& ctx) {
            TestAddMyStructByIndexWithHoles<core::ReduceTableImpl::BUCKET>(ctx);
        });
}

TEST(ReduceHashPhase, OldProbingAddMyStructByIndexWithHoles) {
    api::RunLocalSameThread(
        [](Context& ctx) {
            TestAddMyStructByIndexWithHoles<core::ReduceTableImpl::OLD_PROBING>(ctx);
        });
}

TEST(ReduceHashPhase, ProbingAddMyStructByIndexWithHoles) {
    api::RunLocalSameThread(
        [](Context& ctx) {
            TestAddMyStructByIndexWithHoles<core::ReduceTableImpl::PROBING>(ctx);
        });
}

/******************************************************************************/
