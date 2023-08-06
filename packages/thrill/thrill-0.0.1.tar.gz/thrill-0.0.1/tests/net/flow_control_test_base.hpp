/*******************************************************************************
 * tests/net/flow_control_test_base.hpp
 *
 * Part of Project Thrill - http://project-thrill.org
 *
 * Copyright (C) 2015 Timo Bingmann <tb@panthema.net>
 *
 * All rights reserved. Published under the BSD-2 license in the LICENSE file.
 ******************************************************************************/

#pragma once
#ifndef THRILL_TESTS_NET_FLOW_CONTROL_TEST_BASE_HEADER
#define THRILL_TESTS_NET_FLOW_CONTROL_TEST_BASE_HEADER

#include <gtest/gtest.h>
#include <thrill/net/dispatcher.hpp>
#include <thrill/net/flow_control_channel.hpp>
#include <thrill/net/flow_control_manager.hpp>
#include <thrill/net/group.hpp>

#include <functional>
#include <string>
#include <thread>
#include <vector>

using namespace thrill; // NOLINT

/*!
 * Calculates a prefix sum over all worker ids.
 */
static void TestSingleThreadPrefixSum(net::Group* net) {
    net::FlowControlChannelManager manager(*net, 1);
    net::FlowControlChannel& channel = manager.GetFlowControlChannel(0);
    size_t my_rank = net->my_host_rank();
    size_t initial = 42;

    size_t resInclusive =
        channel.PrefixSum(my_rank, std::plus<size_t>(), initial);
    size_t resExclusive =
        channel.ExPrefixSum(my_rank, std::plus<size_t>(), initial);
    size_t expectedInclusive = initial;
    size_t expectedExclusive = initial;

    for (size_t i = 0; i <= my_rank; i++) {
        expectedInclusive += i;
    }

    for (size_t i = 0; i < my_rank; i++) {
        expectedExclusive += i;
    }

    ASSERT_EQ(expectedInclusive, resInclusive);
    ASSERT_EQ(expectedExclusive, resExclusive);
}

static void TestSingleThreadVectorPrefixSum(net::Group* net) {
    net::FlowControlChannelManager manager(*net, 1);
    net::FlowControlChannel& channel = manager.GetFlowControlChannel(0);
    size_t size = 3;
    size_t my_rank = net->my_host_rank();
    std::vector<size_t> initial(size);
    std::fill(initial.begin(), initial.end(), 42);
    std::vector<size_t> val(size);
    std::fill(val.begin(), val.end(), my_rank);

    std::vector<size_t> resInclusive = channel.PrefixSum(
        val, common::ComponentSum<std::vector<size_t> >(), initial);
    std::vector<size_t> resExclusive = channel.ExPrefixSum(
        val, common::ComponentSum<std::vector<size_t> >(), initial);
    size_t expectedInclusive = 42;
    size_t expectedExclusive = 42;

    for (size_t i = 0; i <= my_rank; i++) {
        expectedInclusive += i;
    }

    for (size_t i = 0; i < my_rank; i++) {
        expectedExclusive += i;
    }

    for (size_t i = 0; i < size; i++) {
        ASSERT_EQ(expectedInclusive, resInclusive[i]);
        ASSERT_EQ(expectedExclusive, resExclusive[i]);
    }
}

/*!
 * Broadcasts the ID of the master, which is 0.
 */
static void TestSingleThreadBroadcast(net::Group* net) {
    net::FlowControlChannelManager manager(*net, 1);
    net::FlowControlChannel& channel = manager.GetFlowControlChannel(0);
    size_t magic = 1337;
    size_t my_rank = net->my_host_rank();
    size_t value = my_rank + magic;

    size_t res = channel.Broadcast(value);

    ASSERT_EQ(res, magic);
}

static void ExecuteMultiThreads(
    net::Group* net, size_t count,
    const std::function<void(net::FlowControlChannel&)>& function) {

    std::vector<std::thread> threads(count);
    net::FlowControlChannelManager manager(*net, count);

    for (size_t i = 0; i < count; i++) {
        threads[i] = std::thread(
            [i, function, &manager] {
                net::FlowControlChannel& fcc = manager.GetFlowControlChannel(i);
                function(fcc);
            });
    }

    for (size_t i = 0; i < count; i++) {
        threads[i].join();
    }
}

/*!
 * Broadcasts the ID of the master, which is 0.
 */
static void TestMultiThreadBroadcast(net::Group* net) {
    const size_t count = 4;
    const size_t magic = 1337;
    ExecuteMultiThreads(
        net, count, [=](net::FlowControlChannel& channel) {

            for (size_t origin = 0; origin < channel.num_workers(); ++origin) {

                size_t my_rank = origin == channel.my_rank() ? magic : 0;

                size_t res = channel.Broadcast(my_rank, origin);

                ASSERT_EQ(res, magic);
            }
        });
}

/*!
 * Calculates a sum over all worker and thread ids.
 */
static void TestMultiThreadReduce(net::Group* net) {

    const size_t count = 4;

    ExecuteMultiThreads(
        net, count, [=](net::FlowControlChannel& channel) {
            size_t my_rank = channel.my_rank();

            size_t root_rank = channel.num_workers() * 2 / 3;
            sLOG0 << "root_rank" << root_rank;

            size_t res = channel.Reduce(my_rank, root_rank);
            size_t expected = 0;
            for (size_t i = 0; i < net->num_hosts() * count; i++) {
                expected += i;
            }

            if (my_rank == root_rank) {
                ASSERT_EQ(res, expected);
            }
        });
}

/*!
 * Calculates a sum over all worker ids.
 */
static void TestSingleThreadAllReduce(net::Group* net) {
    net::FlowControlChannelManager manager(*net, 1);
    net::FlowControlChannel& channel = manager.GetFlowControlChannel(0);

    size_t my_rank = net->my_host_rank();

    size_t res = channel.AllReduce(my_rank);

    size_t expected = 0;
    for (size_t i = 0; i < net->num_hosts(); i++) {
        expected += i;
    }

    ASSERT_EQ(res, expected);
}

/*!
 * Calculates a sum over all worker and thread ids.
 */
static void TestMultiThreadAllReduce(net::Group* net) {

    const size_t count = 4;

    ExecuteMultiThreads(
        net, count, [=](net::FlowControlChannel& channel) {
            size_t my_rank = channel.my_rank();

            size_t res = channel.AllReduce(my_rank);
            size_t expected = 0;
            for (size_t i = 0; i < net->num_hosts() * count; i++) {
                expected += i;
            }

            ASSERT_EQ(res, expected);
        });
}

/*!
 * Calculates a sum over all worker and thread ids.
 */
static void TestMultiThreadPrefixSum(net::Group* net) {

    const size_t count = 4;

    ExecuteMultiThreads(
        net, count, [=](net::FlowControlChannel& channel) {
            size_t my_rank = channel.my_rank();
            size_t initial = 42;

            size_t resInclusive = channel.PrefixSum(
                my_rank, std::plus<size_t>(), initial);
            size_t resExclusive = channel.ExPrefixSum(
                my_rank, std::plus<size_t>(), initial);
            size_t expectedInclusive = 42;
            size_t expectedExclusive = 42;

            for (size_t i = 0; i <= my_rank; i++) {
                expectedInclusive += i;
            }

            for (size_t i = 0; i < my_rank; i++) {
                expectedExclusive += i;
            }

            ASSERT_EQ(expectedInclusive, resInclusive);
            ASSERT_EQ(expectedExclusive, resExclusive);
        });
}

// perform first test: PE must be items only from predecessor
static void TestPredecessorManyItems(net::Group* net) {

    const size_t thread_count = 4;

    ExecuteMultiThreads(
        net, thread_count,
        [=](net::FlowControlChannel& channel) {
            size_t my_rank = channel.my_rank();

            for (size_t r = 0; r < 10; ++r) {
                // each PE has three items
                std::vector<size_t> inval(3);
                inval[0] = r + my_rank;
                inval[1] = r + my_rank + 42;
                inval[2] = r + my_rank * my_rank;

                // get two predecessors
                std::vector<size_t> pre = channel.Predecessor(2, inval);

                if (my_rank == 0) {
                    ASSERT_EQ(0u, pre.size());
                }
                else {
                    ASSERT_EQ(r + (my_rank - 1) + 42, pre[0]);
                    ASSERT_EQ(r + (my_rank - 1) * (my_rank - 1), pre[1]);
                }
            }
        });
}

// perform second test: one PE must get elements from preceding two ones.
static void TestPredecessorFewItems(net::Group* net) {

    const size_t thread_count = 4;

    ExecuteMultiThreads(
        net, thread_count,
        [=](net::FlowControlChannel& channel) {
            size_t my_rank = channel.my_rank();

            for (size_t r = 0; r < 10; ++r) {
                // each PE has only one item
                std::vector<size_t> inval(1);
                inval[0] = r + my_rank;

                // get three predecessors
                std::vector<size_t> pre = channel.Predecessor(3, inval);

                if (my_rank == 0) {
                    ASSERT_EQ(0u, pre.size());
                }
                else if (my_rank == 1) {
                    ASSERT_EQ(1u, pre.size());
                    ASSERT_EQ(r + 0u, pre[0]);
                }
                else if (my_rank == 2) {
                    ASSERT_EQ(2u, pre.size());
                    ASSERT_EQ(r + 0u, pre[0]);
                    ASSERT_EQ(r + 1u, pre[1]);
                }
                else {
                    ASSERT_EQ(3u, pre.size());
                    ASSERT_EQ(r + my_rank - 3u, pre[0]);
                    ASSERT_EQ(r + my_rank - 2u, pre[1]);
                    ASSERT_EQ(r + my_rank - 1u, pre[2]);
                }
            }
        });
}

// perform third evil test: only first PE has an item
static void TestPredecessorOneItem(net::Group* net) {

    const size_t thread_count = 4;

    ExecuteMultiThreads(
        net, thread_count,
        [=](net::FlowControlChannel& channel) {
            size_t my_rank = channel.my_rank();

            for (size_t r = 0; r < 10; ++r) {
                // first PE has only one item
                std::vector<size_t> inval;
                if (my_rank == 0) {
                    inval.push_back(r);
                }

                // get three predecessors
                std::vector<size_t> pre = channel.Predecessor(3, inval);

                if (my_rank == 0) {
                    ASSERT_EQ(0u, pre.size());
                }
                else {
                    ASSERT_EQ(1u, pre.size());
                    ASSERT_EQ(r, pre[0]);
                }
            }
        });
}

/*!
 * Does a lot of operations to provoke race conditions.
 */
static void TestHardcoreRaceConditionTest(net::Group* net) {

    const size_t count = 4;
    sLOG0 << "hardware_concurrency: " << std::thread::hardware_concurrency();

    ExecuteMultiThreads(
        net, count, [=](net::FlowControlChannel& channel) {
            size_t my_rank = channel.my_rank();
            std::vector<size_t> pres;
            std::vector<size_t> rres;

            for (int i = 0; i < 20; i++) {
                // Make a prefix sum and push res
                pres.push_back(channel.PrefixSum(my_rank));
                // Make an all reduce and push res.
                rres.push_back(channel.AllReduce(my_rank));

                // Assert that broadcast gives us the result of the master
                size_t bRes = channel.Broadcast(i + net->my_host_rank());
                ASSERT_EQ(bRes, i);
            }
            size_t pexpected = 0;
            for (size_t i = 0; i <= channel.my_rank(); i++) {
                pexpected += i;
            }
            size_t rexpected = 0;
            for (size_t i = 0; i < net->num_hosts() * count; i++) {
                rexpected += i;
            }

            for (size_t i = 0; i < pres.size(); i++) {
                ASSERT_EQ(pexpected, pres[i]);
                ASSERT_EQ(rexpected, rres[i]);
            }
        });
}

/*!
 * single threaded test for allgather collective
 */
static void TestAllGather(net::Group* net) {
    net::FlowControlChannelManager manager(*net, 1);
    net::FlowControlChannel& channel = manager.GetFlowControlChannel(0);
    size_t my_rank = net->my_host_rank();
    size_t hosts = net->num_hosts();

    std::vector<size_t> expected(hosts);
    for (size_t i = 0; i < hosts; i++) {
        expected[i] = i;
    }

    auto res = channel.AllGather(my_rank);

    for (size_t i = 0; i < hosts; i++) {
        ASSERT_EQ(expected[i], res->at(i));
    }
}

/*!
 * multi threaded test for allgather collective
 */
static void TestAllGatherMultiThreaded(net::Group* net) {

    const size_t count = 4;
    size_t hosts = net->num_hosts();

    ExecuteMultiThreads(
        net, count, [=](net::FlowControlChannel& channel) {
            size_t my_rank = channel.my_rank();

            std::vector<size_t> expected(net->num_hosts());
            for (size_t i = 0; i < hosts; i++) {
                expected[i] = i;
            }

            auto res = channel.AllGather(my_rank);

            for (size_t i = 0; i < hosts; i++) {
                ASSERT_EQ(expected[i], res->at(i));
            }
        });
}

//! let group of p hosts perform an AllGather collective on std::string
static void TestAllGatherString(net::Group* net) {
    net::FlowControlChannelManager manager(*net, 1);
    net::FlowControlChannel& channel = manager.GetFlowControlChannel(0);
    size_t hosts = net->num_hosts();

    const std::string template_string = "abcdefghijklmnopqrstuvwxyz";

    std::string local_value = template_string.substr(0, net->my_host_rank());
    auto result = channel.AllGather(local_value);

    std::vector<std::string> expected(hosts);
    for (size_t i = 0; i < hosts; ++i) {
        expected[i] = template_string.substr(0, i);
    }

    for (size_t i = 0; i < hosts; ++i) {
        ASSERT_EQ(expected[i], result->at(i));
    }
}

#endif // !THRILL_TESTS_NET_FLOW_CONTROL_TEST_BASE_HEADER

/******************************************************************************/
