/*******************************************************************************
 * tests/api/join_test.cpp
 *
 * Part of Project Thrill - http://project-thrill.org
 *
 * Copyright (C) 2016 Alexander Noe <aleexnoe@gmail.com>
 *
 * All rights reserved. Published under the BSD-2 license in the LICENSE file.
 ******************************************************************************/

#include <thrill/api/all_gather.hpp>
#include <thrill/api/generate.hpp>
#include <thrill/api/inner_join.hpp>
#include <thrill/api/sum.hpp>
#include <thrill/common/logger.hpp>

#include <gtest/gtest.h>

#include <algorithm>
#include <cstdlib>
#include <limits>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

using namespace thrill; // NOLINT

TEST(Join, PairsUnique) {

    auto start_func =
        [](Context& ctx) {

            using IntPair = std::pair<size_t, size_t>;
            using IntTuple = std::tuple<size_t, size_t, size_t>;

            size_t n = 9999;

            auto dia1 = Generate(ctx, n, [](const size_t& e) {
                                     return std::make_pair(e, e * e);
                                 });

            auto dia2 = Generate(ctx, n, [](const size_t& e) {
                                     return std::make_pair(e, e * e * e);
                                 });

            auto key_ex = [](IntPair input) {
                              return input.first;
                          };

            auto join_fn = [](IntPair input1, IntPair input2) {
                               return std::make_tuple(input1.first,
                                                      input1.second,
                                                      input2.second);
                           };

            auto joined = InnerJoin(dia1, dia2, key_ex, key_ex, join_fn);
            std::vector<IntTuple> out_vec = joined.AllGather();

            std::sort(out_vec.begin(), out_vec.end(),
                      [](const IntTuple& in1, const IntTuple& in2) {
                          return std::get<0>(in1) < std::get<0>(in2);
                      });

            ASSERT_EQ(n, out_vec.size());
            for (size_t i = 0; i < out_vec.size(); i++) {
                ASSERT_EQ(std::make_tuple(i, i * i, i * i * i), out_vec[i]);
            }
        };

    api::RunLocalTests(start_func);
}

TEST(Join, PairsSameKey) {

    auto start_func =
        [](Context& ctx) {

            using IntPair = std::pair<size_t, size_t>;

            size_t n = 333;

            auto dia1 = Generate(ctx, n, [](const size_t& e) {
                                     return std::make_pair(1, e);
                                 });

            auto dia2 = Generate(ctx, n, [](const size_t& e) {
                                     return std::make_pair(1, e * e);
                                 });

            auto key_ex = [](const IntPair& input) {
                              return input.first;
                          };

            auto join_fn = [](const IntPair& input1, const IntPair& input2) {
                               return std::make_pair(input1.second,
                                                     input2.second);
                           };

            auto joined = InnerJoin(dia1, dia2, key_ex, key_ex, join_fn);
            std::vector<IntPair> out_vec = joined.AllGather();

            std::sort(out_vec.begin(), out_vec.end(),
                      [](const IntPair& in1, const IntPair& in2) {
                          if (in1.first == in2.first) {
                              return in1.second < in2.second;
                          }
                          else {
                              return in1.first < in2.first;
                          }
                      });

            ASSERT_EQ(n * n, out_vec.size());
            for (size_t i = 0; i < out_vec.size(); i++) {
                ASSERT_EQ(std::make_pair(i / n, (i % n) * (i % n)), out_vec[i]);
            }
        };

    api::RunLocalTests(start_func);
}

TEST(Join, PairsSameKeyDiffSizes) {

    auto start_func =
        [](Context& ctx) {

            using IntPair = std::pair<size_t, size_t>;

            size_t n = 333;
            size_t m = 100;

            auto dia1 = Generate(ctx, m, [](const size_t& e) {
                                     return std::make_pair(1, e);
                                 });

            auto dia2 = Generate(ctx, n, [](const size_t& e) {
                                     return std::make_pair(1, e * e);
                                 });

            auto key_ex = [](const IntPair& input) {
                              return input.first;
                          };

            auto join_fn = [](const IntPair& input1, const IntPair& input2) {
                               return std::make_pair(input1.second,
                                                     input2.second);
                           };

            auto joined = InnerJoin(dia1, dia2, key_ex, key_ex, join_fn);
            std::vector<IntPair> out_vec = joined.AllGather();

            std::sort(out_vec.begin(), out_vec.end(),
                      [](const IntPair& in1, const IntPair& in2) {
                          if (in1.first == in2.first) {
                              return in1.second < in2.second;
                          }
                          else {
                              return in1.first < in2.first;
                          }
                      });

            ASSERT_EQ(n * m, out_vec.size());
            for (size_t i = 0; i < out_vec.size(); i++) {
                ASSERT_EQ(std::make_pair(i / n, (i % n) * (i % n)), out_vec[i]);
            }
        };

    api::RunLocalTests(start_func);
}

TEST(Join, DifferentTypes) {

    auto start_func =
        [](Context& ctx) {

            using IntPair = std::pair<size_t, size_t>;
            using intuple3 = std::tuple<size_t, size_t, size_t>;
            using intuple5 = std::tuple<size_t, size_t, size_t, size_t, size_t>;

            size_t n = 9999;

            auto dia1 = Generate(ctx, n, [](const size_t& e) {
                                     return std::make_pair(e, e * e);
                                 });

            auto dia2 = Generate(ctx, n, [](const size_t& e) {
                                     return std::make_tuple(e, e * e, e * e * e);
                                 });

            auto key_ex1 = [](IntPair input) {
                               return input.first;
                           };

            auto key_ex2 = [](intuple3 input) {
                               return std::get<0>(input);
                           };

            auto join_fn =
                [](IntPair input1, intuple3 input2) {
                    return std::make_tuple(
                        input1.first, input1.second,
                        std::get<0>(input2), std::get<1>(input2), std::get<2>(input2));
                };

            auto joined = InnerJoin(dia1, dia2, key_ex1, key_ex2, join_fn);
            std::vector<intuple5> out_vec = joined.AllGather();

            std::sort(out_vec.begin(), out_vec.end(),
                      [](const intuple5& in1, const intuple5& in2) {
                          return std::get<0>(in1) < std::get<0>(in2);
                      });

            ASSERT_EQ(n, out_vec.size());
            for (size_t i = 0; i < out_vec.size(); i++) {
                ASSERT_EQ(std::make_tuple(i, i * i, i, i * i, i * i * i),
                          out_vec[i]);
            }
        };

    api::RunLocalTests(start_func);
}

/******************************************************************************/
