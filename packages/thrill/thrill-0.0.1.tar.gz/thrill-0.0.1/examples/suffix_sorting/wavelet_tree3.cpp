/*******************************************************************************
 * examples/suffix_sorting/wavelet_tree3.cpp
 *
 * Part of Project Thrill - http://project-thrill.org
 *
 * Copyright (C) 2016 Timo Bingmann <tb@panthema.net>
 *
 * All rights reserved. Published under the BSD-2 license in the LICENSE file.
 ******************************************************************************/

#include <examples/suffix_sorting/construct_wt.hpp>

#include <thrill/api/generate.hpp>
#include <thrill/api/read_binary.hpp>
#include <thrill/api/write_binary.hpp>
#include <thrill/common/logger.hpp>
#include <tlx/cmdline_parser.hpp>

#include <algorithm>
#include <limits>
#include <random>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

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
            ctx.enable_consume();

            if (input_path.size()) {
                auto input_dia = ReadBinary<uint8_t>(ctx, input_path);
                ConstructWaveletTree(input_dia, "wt-bin");
            }
            else {
                std::string bwt = "aaaaaaaaaaabbbbaaaaaaaccccdddaacacaffatttttttttttyyyyaaaaa";
                auto input_dia =
                    Generate(ctx, bwt.size(),
                             [&](size_t i) { return (uint8_t)bwt[i]; });
                ConstructWaveletTree(input_dia, "wt-bin");
            }
        });
}

/******************************************************************************/
