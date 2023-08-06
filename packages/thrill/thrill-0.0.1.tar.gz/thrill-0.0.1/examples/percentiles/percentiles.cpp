/*******************************************************************************
 * examples/percentiles/percentiles.cpp
 *
 * Part of Project Thrill - http://project-thrill.org
 *
 * Copyright (C) 2016 Alexander Noe <aleexnoe@gmail.com>
 *
 * All rights reserved. Published under the BSD-2 license in the LICENSE file.
 ******************************************************************************/

#include <thrill/api/cache.hpp>
#include <thrill/api/dia.hpp>
#include <thrill/api/group_by_key.hpp>
#include <thrill/api/read_lines.hpp>
#include <thrill/api/size.hpp>
#include <thrill/api/sort.hpp>
#include <thrill/api/sum.hpp>
#include <thrill/common/string.hpp>
#include <tlx/cmdline_parser.hpp>

#include <tlx/string/split.hpp>

#include <algorithm>
#include <ctime>
#include <string>
#include <utility>
#include <vector>

using namespace thrill; // NOLINT

void Percentiles(api::Context& ctx, const std::string& input_path) {

    const bool use_detection = false;

    std::vector<std::string> splitted;

    auto temps =
        ReadLines(ctx, input_path)
        .FlatMap<std::pair<time_t, double> >(
            [&splitted](const std::string& input, auto emit) {
                tlx::split(&splitted, ',', input);
                if (splitted[0] != "time") {
                    time_t timet = std::stod(splitted[0]);
                    struct tm* tmstr = std::localtime(&timet);
                    double temp = std::stod(splitted[1]);
                    size_t time = 24 * tmstr->tm_yday + tmstr->tm_hour;
                    emit(std::make_pair(time, temp));
                }
            })
        .Cache().Execute();

    auto median_fn =
        [](auto& r, std::size_t) {
            std::vector<double> all;
            size_t time = 0;
            while (r.HasNext()) {
                auto next = r.Next();
                all.push_back(next.second);
                time = next.first;
            }
            std::sort(std::begin(all), std::end(all));
            return std::make_pair(time, all[all.size() / 2 - 1]);
        };

    auto time_keyfn =
        [](std::pair<time_t, double> input) {
            return input.first;
        };

    // group by to compute median
    ctx.net.Barrier();
    thrill::common::StatsTimerStart timer;
    temps.GroupByKey<std::pair<size_t, double> >(
        LocationDetectionFlag<use_detection>(),
        time_keyfn, median_fn).Size();

    ctx.net.Barrier();
    timer.Stop();

    if (ctx.my_rank() == 0) {
        if (use_detection) {
            LOG1 << "RESULT " << "benchmark=median " << "detection=ON"
                 << " time=" << timer
                 << " traffic=" << ctx.net_manager().Traffic()
                 << " hosts=" << ctx.num_hosts();
        }
        else {
            LOG1 << "RESULT " << "benchmark=median " << "detection=OFF"
                 << " time=" << timer
                 << " traffic=" << ctx.net_manager().Traffic()
                 << " hosts=" << ctx.num_hosts();
        }
    }
}

int main(int argc, char* argv[]) {

    tlx::CmdlineParser clp;

    std::string input_path;
    clp.add_param_string("input", input_path,
                         "input file pattern");

    if (!clp.process(argc, argv)) {
        return -1;
    }

    clp.print_result();

    return api::Run([&input_path](api::Context& ctx) {
                        return Percentiles(ctx, input_path);
                    });
}

/******************************************************************************/
