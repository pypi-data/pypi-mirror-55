/***************************************************************************
 *  foxxll/mng/async_schedule.cpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2002, 2009 Roman Dementiev <dementiev@mpi-sb.mpg.de>
 *  Copyright (C) 2009, 2010 Andreas Beckmann <beckmann@cs.uni-frankfurt.de>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

// Implements the "prudent prefetching" as described in
// D. Hutchinson, P. Sanders, J. S. Vitter: Duality between prefetching
// and queued writing on parallel disks, 2005
// DOI: 10.1137/S0097539703431573

#include <algorithm>
#include <cassert>
#include <functional>
#include <queue>
#include <utility>
#include <vector>

#include <tlx/simple_vector.hpp>
#include <tlx/unused.hpp>

#include <foxxll/common/types.hpp>
#include <foxxll/io/file.hpp>
#include <foxxll/mng/async_schedule.hpp>

namespace foxxll {
namespace async_schedule_local {

constexpr static bool debug = false;

// only one type of event: WRITE COMPLETED
struct sim_event
{
    size_t timestamp;
    size_t iblock;
    inline sim_event(size_t t, size_t b) : timestamp(t), iblock(b) { }
};

struct sim_event_cmp : public std::binary_function<sim_event, sim_event, bool>
{
    inline bool operator () (const sim_event& a, const sim_event& b) const
    {
        return a.timestamp > b.timestamp;
    }
};

using write_time_pair = std::pair<size_t, size_t>;
struct write_time_cmp : public std::binary_function<write_time_pair, write_time_pair, bool>
{
    inline bool operator () (const write_time_pair& a, const write_time_pair& b) const
    {
        return a.second > b.second;
    }
};

static inline size_t get_disk(size_t i, const size_t* disks, size_t D)
{
    size_t disk = disks[i];
    if (disk == file::DEFAULT_DEVICE_ID)
        disk = D;      // remap to sentinel
    assert(disk <= D);
    return disk;
}

size_t simulate_async_write(
    const size_t* disks,
    const size_t L,
    const size_t m_init,
    const size_t D,
    std::pair<size_t, size_t>* o_time)
{
    using event_queue_type = std::priority_queue<sim_event, std::vector<sim_event>, sim_event_cmp>;
    using disk_queue_type = std::queue<size_t>;
    assert(L >= D);
    // + sentinel for remapping NO_ALLOCATOR
    tlx::simple_vector<disk_queue_type> disk_queues(D + 1);
    event_queue_type event_queue;

    size_t m = m_init;
    size_t i = L;
    size_t oldtime = 0;
    tlx::simple_vector<bool> disk_busy(D + 1);

    while (m && (i > 0))
    {
        i--;
        m--;
        size_t disk = get_disk(i, disks, D);
        disk_queues[disk].push(i);
    }

    for (size_t ii = 0; ii <= D; ii++)
        if (!disk_queues[ii].empty())
        {
            size_t j = disk_queues[ii].front();
            disk_queues[ii].pop();
            event_queue.push(sim_event(1, j));
            TLX_LOG << "Block " << j << " scheduled";
        }

    while (!event_queue.empty())
    {
        sim_event cur = event_queue.top();
        event_queue.pop();
        if (oldtime != cur.timestamp)
        {
            // clear disk_busy
            for (size_t j = 0; j <= D; j++)
                disk_busy[j] = false;

            oldtime = cur.timestamp;
        }

        TLX_LOG << "Block " << cur.iblock << " put out, time "
                << cur.timestamp << " disk: " << disks[cur.iblock];
        o_time[cur.iblock] = std::pair<size_t, size_t>(cur.iblock, cur.timestamp);

        if (i > 0)
        {
            size_t disk = get_disk(i - 1, disks, D);
            if (disk_busy[disk])
            {
                disk_queues[disk].push(--i);
            }
            else
            {
                if (!disk_queues[disk].empty())
                {
                    TLX_LOG << "c Block " << disk_queues[disk].front()
                            << " scheduled for time " << cur.timestamp + 1;
                    event_queue.push(sim_event(cur.timestamp + 1, disk_queues[disk].front()));
                    disk_queues[disk].pop();
                }
                else
                {
                    TLX_LOG << "a Block " << (i - 1)
                            << " scheduled for time " << cur.timestamp + 1;
                    event_queue.push(sim_event(cur.timestamp + 1, --i));
                }
                disk_busy[disk] = true;
            }
        }

        // add next block to write
        size_t disk = get_disk(cur.iblock, disks, D);
        if (!disk_busy[disk] && !disk_queues[disk].empty())
        {
            TLX_LOG << "b Block " << disk_queues[disk].front()
                    << " scheduled for time " << cur.timestamp + 1;
            event_queue.push(sim_event(cur.timestamp + 1, disk_queues[disk].front()));
            disk_queues[disk].pop();
            disk_busy[disk] = true;
        }
    }

    assert(i == 0);
    for (size_t j = 0; j <= D; j++)
        assert(disk_queues[j].empty());

    return (oldtime - 1);
}

} // namespace async_schedule_local

void compute_prefetch_schedule(
    const size_t* first,
    const size_t* last,
    size_t* out_first,
    size_t m,
    size_t D)
{
    constexpr bool debug = false;

    using pair_type = std::pair<size_t, size_t>;
    size_t L = last - first;
    if (L <= D)
    {
        for (size_t i = 0; i < L; ++i)
            out_first[i] = i;

        return;
    }
    pair_type* write_order = new pair_type[L];

    size_t w_steps = async_schedule_local::simulate_async_write(first, L, m, D, write_order);

    TLX_LOG << "Write steps: " << w_steps;

    for (size_t i = 0; i < L; i++)
        TLX_LOG << first[i] << " " << write_order[i].first << " " << write_order[i].second;

    std::stable_sort(write_order, write_order + L, async_schedule_local::write_time_cmp());

    for (size_t i = 0; i < L; i++)
    {
        out_first[i] = write_order[i].first;
        //if(out_first[i] != i)
        TLX_LOG << i << " " << out_first[i];
    }

    delete[] write_order;
    tlx::unused(w_steps);
}

} // namespace foxxll

/**************************************************************************/
