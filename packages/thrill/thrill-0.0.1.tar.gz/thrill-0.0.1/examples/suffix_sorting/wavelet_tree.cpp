/*******************************************************************************
 * examples/suffix_sorting/wavelet_tree.cpp
 *
 * Part of Project Thrill - http://project-thrill.org
 *
 * Copyright (C) 2016 Timo Bingmann <tb@panthema.net>
 *
 * All rights reserved. Published under the BSD-2 license in the LICENSE file.
 ******************************************************************************/

#include <thrill/api/collapse.hpp>
#include <thrill/api/dia.hpp>
#include <thrill/api/generate.hpp>
#include <thrill/api/max.hpp>
#include <thrill/api/print.hpp>
#include <thrill/api/read_binary.hpp>
#include <thrill/api/sort.hpp>
#include <thrill/api/write_binary.hpp>
#include <thrill/common/logger.hpp>
#include <tlx/cmdline_parser.hpp>
#include <tlx/math/integer_log2.hpp>

#include <algorithm>
#include <limits>
#include <random>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace examples {
namespace suffix_sorting {

static constexpr bool debug = false;

using namespace thrill; // NOLINT

template <typename InputDIA>
auto ConstructWaveletTree(const InputDIA& input_dia) {

    uint64_t max_value = input_dia.Max();
    sLOG << "max_value" << max_value;

    uint64_t level = tlx::integer_log2_ceil(max_value);
    uint64_t mask = (~uint64_t(0)) << level;
    uint64_t maskbit = uint64_t(1) << level;

    DIA<uint64_t> wt = input_dia.Collapse();
    if (debug) wt.Print("wt");

    while (mask != (~uint64_t(0))) {

        // switch to next level
        --level;
        mask = (mask >> 1) | 0x8000000000000000llu;
        maskbit >>= 1;

        sLOG << "maskbit" << maskbit << "mask" << std::hex << mask;

        wt.Map(
            [maskbit](const uint64_t& a) {
                return (a & maskbit) != 0;
            })
        .WriteBinary(tlx::ssprintf("wt-%04u-", unsigned(level)));

        wt = wt.Sort(
            [mask](const uint64_t& a, const uint64_t& b) {
                return (a & mask) < (b & mask);
            });

        if (debug) wt.Print("wt");
    }
}

} // namespace suffix_sorting
} // namespace examples

int main(int argc, char* argv[]) {

    using namespace thrill; // NOLINT
    using namespace examples::suffix_sorting;

    tlx::CmdlineParser cp;

    cp.set_author("Timo Bingmann <tb@panthema.net>");

    std::string input_path;

    cp.add_opt_param_string("input", input_path,
                            "Path to input file.");

    if (!cp.process(argc, argv))
        return -1;

    return Run(
        [&](Context& ctx) {
            if (input_path.size()) {
                auto input_dia = ReadBinary<uint64_t>(ctx, input_path);
                ConstructWaveletTree(input_dia);
            }
            else {
                std::default_random_engine rng(std::random_device { } ());
                auto input_dia =
                    Generate(ctx, 32,
                             [&](size_t) { return uint64_t(rng() % 32); });
                ConstructWaveletTree(input_dia);
            }
        });
}

/******************************************************************************/
