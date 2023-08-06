/*******************************************************************************
 * examples/suffix_sorting/dc7.cpp
 *
 * Part of Project Thrill - http://project-thrill.org
 *
 * Copyright (C) 2015-2016 Timo Bingmann <tb@panthema.net>
 *
 * All rights reserved. Published under the BSD-2 license in the LICENSE file.
 ******************************************************************************/

#include <examples/suffix_sorting/check_sa.hpp>
#include <examples/suffix_sorting/suffix_sorting.hpp>

#include <thrill/api/all_gather.hpp>
#include <thrill/api/cache.hpp>
#include <thrill/api/collapse.hpp>
#include <thrill/api/dia.hpp>
#include <thrill/api/gather.hpp>
#include <thrill/api/max.hpp>
#include <thrill/api/merge.hpp>
#include <thrill/api/prefix_sum.hpp>
#include <thrill/api/print.hpp>
#include <thrill/api/size.hpp>
#include <thrill/api/sort.hpp>
#include <thrill/api/sum.hpp>
#include <thrill/api/union.hpp>
#include <thrill/api/window.hpp>
#include <thrill/api/zip_window.hpp>
#include <thrill/api/zip_with_index.hpp>
#include <thrill/common/radix_sort.hpp>
#include <thrill/common/uint_types.hpp>
#include <tlx/cmdline_parser.hpp>

#include <algorithm>
#include <iomanip>
#include <limits>
#include <random>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace examples {
namespace suffix_sorting {
namespace dc7_local {

//! A tuple with index (i,t_i,t_{i+1},t_{i+2},...,t_{i+6}).
template <typename AlphabetType>
struct Chars {
    AlphabetType ch[7];

    bool operator == (const Chars& b) const {
        return std::tie(ch[0], ch[1], ch[2], ch[3], ch[4], ch[5], ch[6])
               == std::tie(b.ch[0], b.ch[1], b.ch[2], b.ch[3],
                           b.ch[4], b.ch[5], b.ch[6]);
    }

    bool operator < (const Chars& b) const {
        return std::tie(ch[0], ch[1], ch[2], ch[3], ch[4], ch[5], ch[6])
               < std::tie(b.ch[0], b.ch[1], b.ch[2], b.ch[3],
                          b.ch[4], b.ch[5], b.ch[6]);
    }

    friend std::ostream& operator << (std::ostream& os, const Chars& chars) {
        return os << '[' << chars.ch[0] << ',' << chars.ch[1]
                  << ',' << chars.ch[2] << ',' << chars.ch[3]
                  << ',' << chars.ch[4] << ',' << chars.ch[5]
                  << ',' << chars.ch[6] << ']';
    }

    static Chars Lowest() {
        return Chars {
            {
                std::numeric_limits<AlphabetType>::lowest(),
                std::numeric_limits<AlphabetType>::lowest(),
                std::numeric_limits<AlphabetType>::lowest(),
                std::numeric_limits<AlphabetType>::lowest(),
                std::numeric_limits<AlphabetType>::lowest(),
                std::numeric_limits<AlphabetType>::lowest(),
                std::numeric_limits<AlphabetType>::lowest()
            }
        };
    }
} TLX_ATTRIBUTE_PACKED;

//! A tuple with index (i,t_i,t_{i+1},t_{i+2}).
template <typename Index, typename AlphabetType>
struct IndexChars {
    Index               index;
    Chars<AlphabetType> chars;

    const AlphabetType& at_radix(size_t depth) const { return chars.ch[depth]; }

    friend std::ostream& operator << (std::ostream& os, const IndexChars& tc) {
        return os << '[' << tc.index << '|' << tc.chars << ']';
    }
} TLX_ATTRIBUTE_PACKED;

//! A pair (index, rank)
template <typename Index>
struct IndexRank {
    Index index;
    Index rank;

    friend std::ostream& operator << (std::ostream& os, const IndexRank& tr) {
        return os << '(' << tr.index << '|' << tr.rank << ')';
    }
} TLX_ATTRIBUTE_PACKED;

//! fragments at string positions i = 0 mod 7.
template <typename Index, typename AlphabetType>
struct StringFragmentMod0 {
    Index        index;
    Index        r0, r1, r3;
    AlphabetType t[3];

    friend std::ostream& operator << (std::ostream& os,
                                      const StringFragmentMod0& sf) {
        return os << "i=" << sf.index
                  << " t0=" << sf.t[0] << " t1=" << sf.t[1] << " t2=" << sf.t[2]
                  << " r0=" << sf.r0 << " r1=" << sf.r1 << " r3=" << sf.r3;
    }
} TLX_ATTRIBUTE_PACKED;

//! fragments at string positions i = 1 mod 7.
template <typename Index, typename AlphabetType>
struct StringFragmentMod1 {
    Index        index;
    Index        r0, r2, r6;
    AlphabetType t[6];

    friend std::ostream& operator << (std::ostream& os,
                                      const StringFragmentMod1& sf) {
        return os << "i=" << sf.index
                  << " t0=" << sf.t[0] << " t1=" << sf.t[1] << " t2=" << sf.t[2]
                  << " t3=" << sf.t[3] << " t4=" << sf.t[4] << " t5=" << sf.t[5]
                  << " r0=" << sf.r0 << " r2=" << sf.r2 << " r6=" << sf.r6;
    }
} TLX_ATTRIBUTE_PACKED;

//! fragments at string positions i = 2 mod 7.
template <typename Index, typename AlphabetType>
struct StringFragmentMod2 {
    Index        index;
    Index        r1, r5, r6;
    AlphabetType t[6];

    friend std::ostream& operator << (std::ostream& os,
                                      const StringFragmentMod2& sf) {
        return os << "i=" << sf.index
                  << " t0=" << sf.t[0] << " t1=" << sf.t[1] << " t2=" << sf.t[2]
                  << " t3=" << sf.t[3] << " t4=" << sf.t[4] << " t5=" << sf.t[5]
                  << " r1=" << sf.r1 << " r5=" << sf.r5 << " r6=" << sf.r6;
    }
} TLX_ATTRIBUTE_PACKED;

//! fragments at string positions i = 3 mod 7.
template <typename Index, typename AlphabetType>
struct StringFragmentMod3 {
    Index        index;
    Index        r0, r4, r5;
    AlphabetType t[5];

    friend std::ostream& operator << (std::ostream& os,
                                      const StringFragmentMod3& sf) {
        return os << "i=" << sf.index
                  << " t0=" << sf.t[0] << " t1=" << sf.t[1] << " t2=" << sf.t[2]
                  << " t3=" << sf.t[3] << " t4=" << sf.t[4]
                  << " r0=" << sf.r0 << " r4=" << sf.r4 << " r5=" << sf.r5;
    }
} TLX_ATTRIBUTE_PACKED;

//! fragments at string positions i = 4 mod 7.
template <typename Index, typename AlphabetType>
struct StringFragmentMod4 {
    Index        index;
    Index        r3, r4, r6;
    AlphabetType t[6];

    friend std::ostream& operator << (std::ostream& os,
                                      const StringFragmentMod4& sf) {
        return os << "i=" << sf.index
                  << " t0=" << sf.t[0] << " t1=" << sf.t[1] << " t2=" << sf.t[2]
                  << " t3=" << sf.t[3] << " t4=" << sf.t[4] << " t5=" << sf.t[5]
                  << " r3=" << sf.r3 << " r4=" << sf.r4 << " r6=" << sf.r6;
    }
} TLX_ATTRIBUTE_PACKED;

//! fragments at string positions i = 5 mod 7.
template <typename Index, typename AlphabetType>
struct StringFragmentMod5 {
    Index        index;
    Index        r2, r3, r5;
    AlphabetType t[5];

    friend std::ostream& operator << (std::ostream& os,
                                      const StringFragmentMod5& sf) {
        return os << "i=" << sf.index
                  << " t0=" << sf.t[0] << " t1=" << sf.t[1] << " t2=" << sf.t[2]
                  << " t3=" << sf.t[3] << " t4=" << sf.t[4]
                  << " r2=" << sf.r2 << " r3=" << sf.r3 << " r5=" << sf.r5;
    }
} TLX_ATTRIBUTE_PACKED;

//! fragments at string positions i = 6 mod 7.
template <typename Index, typename AlphabetType>
struct StringFragmentMod6 {
    Index        index;
    Index        r1, r2, r4;
    AlphabetType t[4];

    friend std::ostream& operator << (std::ostream& os,
                                      const StringFragmentMod6& sf) {
        return os << "i=" << sf.index
                  << " t0=" << sf.t[0] << " t1=" << sf.t[1] << " t2=" << sf.t[2]
                  << " t3=" << sf.t[3]
                  << " r1=" << sf.r1 << " r2=" << sf.r2 << " r4=" << sf.r4;
    }
} TLX_ATTRIBUTE_PACKED;

//! Union of String Fragments with Index
template <typename Index, typename AlphabetType>
struct StringFragment {

    struct Common {
        Index        index;
        Index        ranks[3];
        AlphabetType text[6];
    } TLX_ATTRIBUTE_PACKED;

    union {
        Index                                   index;
        Common                                  common;
        StringFragmentMod0<Index, AlphabetType> mod0;
        StringFragmentMod1<Index, AlphabetType> mod1;
        StringFragmentMod2<Index, AlphabetType> mod2;
        StringFragmentMod3<Index, AlphabetType> mod3;
        StringFragmentMod4<Index, AlphabetType> mod4;
        StringFragmentMod5<Index, AlphabetType> mod5;
        StringFragmentMod6<Index, AlphabetType> mod6;
    } TLX_ATTRIBUTE_PACKED;

    StringFragment() = default;

    // conversion from StringFragmentMod0
    explicit StringFragment(
        const StringFragmentMod0<Index, AlphabetType>& _mod0) : mod0(_mod0) { }

    // conversion from StringFragmentMod1
    explicit StringFragment(
        const StringFragmentMod1<Index, AlphabetType>& _mod1) : mod1(_mod1) { }

    // conversion from StringFragmentMod2
    explicit StringFragment(
        const StringFragmentMod2<Index, AlphabetType>& _mod2) : mod2(_mod2) { }

    // conversion from StringFragmentMod3
    explicit StringFragment(
        const StringFragmentMod3<Index, AlphabetType>& _mod3) : mod3(_mod3) { }

    // conversion from StringFragmentMod4
    explicit StringFragment(
        const StringFragmentMod4<Index, AlphabetType>& _mod4) : mod4(_mod4) { }

    // conversion from StringFragmentMod5
    explicit StringFragment(
        const StringFragmentMod5<Index, AlphabetType>& _mod5) : mod5(_mod5) { }

    // conversion from StringFragmentMod6
    explicit StringFragment(
        const StringFragmentMod6<Index, AlphabetType>& _mod6) : mod6(_mod6) { }

    friend std::ostream& operator << (std::ostream& os,
                                      const StringFragment& tc) {
        os << '[' << std::to_string(tc.index) << '|';
        if (tc.index % 7 == 0)
            return os << "0|" << tc.mod0 << ']';
        else if (tc.index % 7 == 1)
            return os << "1|" << tc.mod1 << ']';
        else if (tc.index % 7 == 2)
            return os << "2|" << tc.mod2 << ']';
        else if (tc.index % 7 == 3)
            return os << "3|" << tc.mod3 << ']';
        else if (tc.index % 7 == 4)
            return os << "4|" << tc.mod4 << ']';
        else if (tc.index % 7 == 5)
            return os << "5|" << tc.mod5 << ']';
        else if (tc.index % 7 == 6)
            return os << "6|" << tc.mod6 << ']';
        abort();
    }

    AlphabetType at_radix(size_t depth) const { return common.text[depth]; }
    Index sort_rank() const { return common.ranks[0]; }
} TLX_ATTRIBUTE_PACKED;

static constexpr size_t fragment_comparator_params[7][7][3] =
{
    {
        { 0, 0, 0 }, { 0, 0, 0 }, { 1, 1, 0 }, { 0, 0, 0 },
        { 3, 2, 0 }, { 3, 2, 1 }, { 1, 1, 0 }
    },
    {
        { 0, 0, 0 }, { 0, 0, 0 }, { 6, 2, 2 }, { 0, 0, 0 },
        { 6, 2, 2 }, { 2, 1, 0 }, { 2, 1, 1 }
    },
    {
        { 1, 0, 1 }, { 6, 2, 2 }, { 1, 0, 0 }, { 5, 1, 2 },
        { 6, 2, 2 }, { 5, 1, 2 }, { 1, 0, 0 }
    },
    {
        { 0, 0, 0 }, { 0, 0, 0 }, { 5, 2, 1 }, { 0, 0, 0 },
        { 4, 1, 1 }, { 5, 2, 2 }, { 4, 1, 2 }
    },
    {
        { 3, 0, 2 }, { 6, 2, 2 }, { 6, 2, 2 }, { 4, 1, 1 },
        { 3, 0, 0 }, { 3, 0, 1 }, { 4, 1, 2 }
    },
    {
        { 3, 1, 2 }, { 2, 0, 1 }, { 5, 2, 1 }, { 5, 2, 2 },
        { 3, 1, 0 }, { 2, 0, 0 }, { 2, 0, 1 }
    },
    {
        { 1, 0, 1 }, { 2, 1, 1 }, { 1, 0, 0 }, { 4, 2, 1 },
        { 4, 2, 1 }, { 2, 1, 0 }, { 1, 0, 0 }
    },
};

template <typename StringFragment>
struct FragmentComparator {

    bool operator () (const StringFragment& a, const StringFragment& b) const {

        unsigned ai = a.index % 7, bi = b.index % 7;

        const size_t* params = fragment_comparator_params[ai][bi];

        for (size_t d = 0; d < params[0]; ++d)
        {
            if (a.common.text[d] == b.common.text[d]) continue;
            return (a.common.text[d] < b.common.text[d]);
        }

        return a.common.ranks[params[1]] < b.common.ranks[params[2]];
    }
};

template <typename Index, typename Char>
struct CharsRanks013 {
    Chars<Char> chars;
    Index       rank0;
    Index       rank1;
    Index       rank3;

    friend std::ostream& operator << (std::ostream& os,
                                      const CharsRanks013& c) {
        return os << "(ch=" << c.chars
                  << " r0=" << c.rank0 << " r1=" << c.rank1
                  << " r3=" << c.rank3 << ")";
    }
} TLX_ATTRIBUTE_PACKED;

template <typename Index, typename Char>
struct IndexCR013Pair {
    Index                      index;
    CharsRanks013<Index, Char> cr0;
    CharsRanks013<Index, Char> cr1;
} TLX_ATTRIBUTE_PACKED;

template <typename Type, size_t MaxDepth>
class RadixSortFragment
{
public:
    explicit RadixSortFragment(size_t K) : K_(K) { }
    template <typename CompareFunction>
    void operator () (
        typename std::vector<Type>::iterator begin,
        typename std::vector<Type>::iterator end,
        const CompareFunction& cmp) const {
        if (K_ <= 4096) {
            thrill::common::radix_sort_CI<MaxDepth>(
                begin, end, K_, cmp, [](auto begin, auto end, auto) {
                    // sub sorter: sort StringFragments by rank
                    std::sort(begin, end, [](const Type& a, const Type& b) {
                                  return a.sort_rank() < b.sort_rank();
                              });
                });
        }
        else {
            std::sort(begin, end, cmp);
        }
    }

private:
    const size_t K_;
};

} // namespace dc7_local

using namespace thrill; // NOLINT
using thrill::common::RingBuffer;

static inline bool IsDiffCover7(size_t i) {
    size_t m = i % 7;
    return m == 0 || m == 1 || m == 3;
}

template <typename Index, typename InputDIA>
DIA<dc7_local::StringFragment<Index, typename InputDIA::ValueType> >
DC7Recursive(const InputDIA& input_dia, size_t input_size, size_t K) {

    using Char = typename InputDIA::ValueType;
    using IndexChars = dc7_local::IndexChars<Index, Char>;
    using IndexRank = dc7_local::IndexRank<Index>;
    using Chars = dc7_local::Chars<Char>;

    Context& ctx = input_dia.context();

    auto tuple_sorted =
        input_dia.Keep()
        // map (t_i) -> (i,t_i,t_{i+1},...,t_{i+6}) where i = 0,1,3 mod 7
        .template FlatWindow<IndexChars>(
            7,
            [](size_t index, const RingBuffer<Char>& r, auto emit) {
                if (IsDiffCover7(index))
                    emit(IndexChars {
                             Index(index), {
                                 { r[0], r[1], r[2], r[3], r[4], r[5], r[6] }
                             }
                         });
            },
            [input_size](size_t index, const RingBuffer<Char>& r, auto emit) {
                // emit last sentinel items.
                if (IsDiffCover7(index)) {
                    emit(IndexChars {
                             Index(index), {
                                 { r.size() >= 1 ? r[0] : Char(),
                                   r.size() >= 2 ? r[1] : Char(),
                                   r.size() >= 3 ? r[2] : Char(),
                                   r.size() >= 4 ? r[3] : Char(),
                                   r.size() >= 5 ? r[4] : Char(),
                                   r.size() >= 6 ? r[5] : Char(),
                                   Char() }
                             }
                         });
                }

                if (index + 1 == input_size && input_size % 7 == 0) {
                    // emit a sentinel tuple for inputs n % 7 == 0 to
                    // separate mod0 and mod1 strings in recursive
                    // subproblem. example which needs this: aaaaaaaaaa.
                    emit(IndexChars { Index(input_size), Chars::Lowest() });
                }
                if (index + 1 == input_size && input_size % 7 == 1) {
                    // emit a sentinel tuple for inputs n % 7 == 1 to
                    // separate mod1 and mod3 strings in recursive
                    // subproblem. example which needs this: aaaaaaaaaa.
                    emit(IndexChars { Index(input_size), Chars::Lowest() });
                }
            })
        // sort tuples by contained letters
        .Sort([](const IndexChars& a, const IndexChars& b) {
                  return a.chars < b.chars;
              }, common::RadixSort<IndexChars, 7>(K));

    if (debug_print)
        tuple_sorted.Keep().Print("tuple_sorted");

    // save tuple's indexes (sorted by tuple content) -> less storage
    auto tuple_index_sorted =
        tuple_sorted
        .Map([](const IndexChars& tc) { return tc.index; })
        .Cache();

    auto tuple_prerank_sums =
        tuple_sorted
        .template FlatWindow<Index>(
            2, [](size_t index, const RingBuffer<IndexChars>& rb, auto emit) {
                assert(rb.size() == 2);

                // emit one sentinel for index 0.
                if (index == 0) emit(0);

                // emit 0 or 1 depending on whether previous tuple is equal
                emit(rb[0].chars == rb[1].chars ? 0 : 1);
            })
        .PrefixSum();

    if (debug_print)
        tuple_prerank_sums.Keep().Print("tuple_prerank_sums");

    // get the last element via an associative reduce.
    const Index max_lexname = tuple_prerank_sums.Keep().Max();

    // size of the mod0 part of the recursive subproblem
    const Index size_mod0 = Index(input_size / 7 + 1);

    // size of the mod1 part of the recursive subproblem
    const Index size_mod1 = Index(input_size / 7 + (input_size % 7 >= 1));

    // size of the mod3 part of the recursive subproblem
    const Index size_mod3 = Index(input_size / 7 + (input_size % 7 >= 4));

    // size of both the mod0 and mod1 parts
    const Index size_mod01 = size_mod0 + size_mod1;

    // compute the size of the 3/7 subproblem.
    const Index size_subp = size_mod01 + size_mod3;

    if (debug_print) {
        sLOG1 << "max_lexname=" << max_lexname
              << " size_subp=" << size_subp
              << " size_mod0=" << size_mod0
              << " size_mod1=" << size_mod1
              << " size_mod3=" << size_mod3;
    }

    if (debug_print) {
        assert_equal(
            tuple_sorted.Keep().Filter([](const IndexChars& a) {
                                           return a.index % 7 == 0;
                                       }).Size(), size_mod0);

        assert_equal(
            tuple_sorted.Keep().Filter([](const IndexChars& a) {
                                           return a.index % 7 == 1;
                                       }).Size(), size_mod1);

        assert_equal(
            tuple_sorted.Keep().Filter([](const IndexChars& a) {
                                           return a.index % 7 == 3;
                                       }).Size(), size_mod3);
    }

    assert_equal(tuple_index_sorted.Keep().Size(), size_subp);

    DIA<IndexRank> ranks_mod013;

    if (max_lexname + Index(1) != size_subp) {
        // some lexical name is not unique -> perform recursion on three
        // substrings (mod 0, mod 1, and mod 3)

        // zip tuples and ranks.
        auto tuple_ranks =
            tuple_index_sorted
            .Zip(NoRebalanceTag,
                 tuple_prerank_sums,
                 [](const Index& tuple_index, const Index& rank) {
                     return IndexRank { tuple_index, rank };
                 });

        if (debug_print)
            tuple_ranks.Keep().Print("tuple_ranks");

        // construct recursion string with all ranks at mod 0 indices followed
        // by all ranks at mod 1 indices followed by all ranks at mod 3 indices.
        DIA<Index> string_mod013 =
            tuple_ranks
            .Sort([](const IndexRank& a, const IndexRank& b) {
                      if (a.index % 7 == b.index % 7)
                          return a.index < b.index;
                      else
                          return a.index % 7 < b.index % 7;
                  })
            .Map([](const IndexRank& tr) {
                     return tr.rank;
                 })
            .Cache();

        if (debug_print)
            string_mod013.Keep().Print("string_mod013");

        assert_equal(string_mod013.Keep().Size(), size_subp);

        using RecStringFragment = dc7_local::StringFragment<Index, Index>;

        DIA<RecStringFragment> suffix_array_rec = DC7Recursive<Index>(
            string_mod013, size_subp, max_lexname + Index(1));

        // reverse suffix array of recursion strings to find ranks for mod 0,
        // mod 1, and mod 3 positions.

        if (debug_print)
            suffix_array_rec.Keep().Print("suffix_array_rec");

        ranks_mod013 =
            suffix_array_rec
            .ZipWithIndex([](const RecStringFragment& sa, const size_t& i) {
                              // add one to ranks such that zero can be used as sentinel
                              // for suffixes beyond the end of the string.
                              return IndexRank { sa.index, Index(i + 1) };
                          })
            .Sort([size_mod0, size_mod01](
                      const IndexRank& a, const IndexRank& b) {

                      Index ai = (a.index < size_mod0 ? a.index :
                                  a.index < size_mod01 ? a.index - size_mod0 :
                                  a.index - size_mod01);

                      Index bi = (b.index < size_mod0 ? b.index :
                                  b.index < size_mod01 ? b.index - size_mod0 :
                                  b.index - size_mod01);

                      // use sort order to interleave ranks mod 0/1/3
                      return ai < bi || (ai == bi && a.index < b.index);
                  });

        if (debug_print) {
            // check that ranks are correctly interleaved
            ranks_mod013.Keep()
            .Window(
                DisjointTag, 3,
                [size_mod0, size_mod01](size_t, const std::vector<IndexRank>& ir) {
                    die_unless(ir[0].index < size_mod0);
                    die_unless(ir[1].index >= size_mod0 || ir[1].rank < size_mod01);
                    die_unless(ir[2].index >= size_mod01);
                    return true;
                })
            .Execute();
            ranks_mod013.Keep().Print("ranks_rec");
        }
    }
    else {
        if (ctx.my_rank() == 0)
            sLOG1 << "*** recursion finished ***";

        if (debug_print)
            tuple_index_sorted.Keep().Print("tuple_index_sorted");

        ranks_mod013 =
            tuple_index_sorted
            .ZipWithIndex(
                [](const Index& sa, const size_t& i) {
                    // add one to ranks such that zero can be used as sentinel
                    // for suffixes beyond the end of the string.
                    return IndexRank { sa, Index(i + 1) };
                })
            .Sort([](const IndexRank& a, const IndexRank& b) {
                      // use sort order for better locality later.
                      return a.index / 7 < b.index / 7 || (
                          a.index / 7 == b.index / 7 &&
                          a.index < b.index);
                  });

        if (debug_print) {
            // check that ranks are correctly interleaved
            ranks_mod013.Keep()
            .Window(
                DisjointTag, 3,
                [](size_t, const std::vector<IndexRank>& ir) {
                    die_unless(ir[0].index % 7 == 0);
                    die_unless(ir[1].index % 7 == 1);
                    die_unless(ir[2].index % 7 == 3);
                    return true;
                })
            .Execute();
            ranks_mod013.Keep().Print("ranks_rec");
        }
    }

    // *** construct StringFragments ***

    // Zip together the three arrays, create pairs, and extract needed
    // tuples into string fragments.

    using StringFragmentMod0 = dc7_local::StringFragmentMod0<Index, Char>;
    using StringFragmentMod1 = dc7_local::StringFragmentMod1<Index, Char>;
    using StringFragmentMod2 = dc7_local::StringFragmentMod2<Index, Char>;
    using StringFragmentMod3 = dc7_local::StringFragmentMod3<Index, Char>;
    using StringFragmentMod4 = dc7_local::StringFragmentMod4<Index, Char>;
    using StringFragmentMod5 = dc7_local::StringFragmentMod5<Index, Char>;
    using StringFragmentMod6 = dc7_local::StringFragmentMod6<Index, Char>;

    using CharsRanks013 = dc7_local::CharsRanks013<Index, Char>;
    using IndexCR013Pair = dc7_local::IndexCR013Pair<Index, Char>;

    auto zip_tuple_pairs1 =
        ZipWindow(
            ArrayTag, PadTag, /* window_size */ {
                { 7, 3 }
            },
            [](const std::array<Char, 7>& ch, const std::array<IndexRank, 3>& mod013) {
                return CharsRanks013 {
                    {
                        { ch[0], ch[1], ch[2], ch[3], ch[4], ch[5], ch[6] }
                    },
                    mod013[0].rank, mod013[1].rank, mod013[2].rank
                };
            },
            std::make_tuple(std::numeric_limits<Char>::lowest(), IndexRank { 0, 0 }),
            input_dia, ranks_mod013);

    if (debug_print)
        zip_tuple_pairs1.Keep().Print("zip_tuple_pairs1");

    auto zip_tuple_pairs =
        zip_tuple_pairs1
        .template FlatWindow<IndexCR013Pair>(
            2, [size_mod0](
                size_t index, const RingBuffer<CharsRanks013>& rb, auto emit) {
                emit(IndexCR013Pair { Index(7 * index), rb[0], rb[1] });
                if (index + 2 == size_mod0) {
                    // emit last sentinel
                    emit(IndexCR013Pair {
                             Index(7 * (index + 1)), rb[1],
                             CharsRanks013 { Chars::Lowest(), 0, 0, 0 }
                         });
                }
            });

    auto fragments_mod0 =
        zip_tuple_pairs
        .Map([](const IndexCR013Pair& ip) {
                 return StringFragmentMod0 {
                     ip.index,
                     ip.cr0.rank0, ip.cr0.rank1, ip.cr0.rank3,
                     { ip.cr0.chars.ch[0], ip.cr0.chars.ch[1],
                       ip.cr0.chars.ch[2] }
                 };
             })
        .Filter([input_size](const StringFragmentMod0& mod0) {
                    return mod0.index < Index(input_size);
                });

    auto fragments_mod1 =
        zip_tuple_pairs
        .Map([](const IndexCR013Pair& ip) {
                 return StringFragmentMod1 {
                     ip.index + Index(1),
                     ip.cr0.rank1, ip.cr0.rank3, ip.cr1.rank0,
                     { ip.cr0.chars.ch[1], ip.cr0.chars.ch[2],
                       ip.cr0.chars.ch[3], ip.cr0.chars.ch[4],
                       ip.cr0.chars.ch[5], ip.cr0.chars.ch[6] }
                 };
             })
        .Filter([input_size](const StringFragmentMod1& mod1) {
                    return mod1.index < Index(input_size);
                });

    auto fragments_mod2 =
        zip_tuple_pairs
        .Map([](const IndexCR013Pair& ip) {
                 return StringFragmentMod2 {
                     ip.index + Index(2),
                     ip.cr0.rank3, ip.cr1.rank0, ip.cr1.rank1,
                     { ip.cr0.chars.ch[2], ip.cr0.chars.ch[3],
                       ip.cr0.chars.ch[4], ip.cr0.chars.ch[5],
                       ip.cr0.chars.ch[6], ip.cr1.chars.ch[0] }
                 };
             })
        .Filter([input_size](const StringFragmentMod2& mod2) {
                    return mod2.index < Index(input_size);
                });

    auto fragments_mod3 =
        zip_tuple_pairs
        .Map([](const IndexCR013Pair& ip) {
                 return StringFragmentMod3 {
                     ip.index + Index(3),
                     ip.cr0.rank3, ip.cr1.rank0, ip.cr1.rank1,
                     { ip.cr0.chars.ch[3], ip.cr0.chars.ch[4],
                       ip.cr0.chars.ch[5], ip.cr0.chars.ch[6],
                       ip.cr1.chars.ch[0] }
                 };
             })
        .Filter([input_size](const StringFragmentMod3& mod3) {
                    return mod3.index < Index(input_size);
                });

    auto fragments_mod4 =
        zip_tuple_pairs
        .Map([](const IndexCR013Pair& ip) {
                 return StringFragmentMod4 {
                     ip.index + Index(4),
                     ip.cr1.rank0, ip.cr1.rank1, ip.cr1.rank3,
                     { ip.cr0.chars.ch[4], ip.cr0.chars.ch[5],
                       ip.cr0.chars.ch[6], ip.cr1.chars.ch[0],
                       ip.cr1.chars.ch[1], ip.cr1.chars.ch[2] }
                 };
             })
        .Filter([input_size](const StringFragmentMod4& mod4) {
                    return mod4.index < Index(input_size);
                });

    auto fragments_mod5 =
        zip_tuple_pairs
        .Map([](const IndexCR013Pair& ip) {
                 return StringFragmentMod5 {
                     ip.index + Index(5),
                     ip.cr1.rank0, ip.cr1.rank1, ip.cr1.rank3,
                     { ip.cr0.chars.ch[5], ip.cr0.chars.ch[6],
                       ip.cr1.chars.ch[0], ip.cr1.chars.ch[1],
                       ip.cr1.chars.ch[2] }
                 };
             })
        .Filter([input_size](const StringFragmentMod5& mod5) {
                    return mod5.index < Index(input_size);
                });

    auto fragments_mod6 =
        zip_tuple_pairs
        .Map([](const IndexCR013Pair& ip) {
                 return StringFragmentMod6 {
                     ip.index + Index(6),
                     ip.cr1.rank0, ip.cr1.rank1, ip.cr1.rank3,
                     { ip.cr0.chars.ch[6], ip.cr1.chars.ch[0],
                       ip.cr1.chars.ch[1], ip.cr1.chars.ch[2] }
                 };
             })
        .Filter([input_size](const StringFragmentMod6& mod6) {
                    return mod6.index < Index(input_size);
                });

    if (debug_print) {
        fragments_mod0.Keep().Print("fragments_mod0");
        fragments_mod1.Keep().Print("fragments_mod1");
        fragments_mod2.Keep().Print("fragments_mod2");
        fragments_mod3.Keep().Print("fragments_mod3");
        fragments_mod4.Keep().Print("fragments_mod4");
        fragments_mod5.Keep().Print("fragments_mod5");
        fragments_mod6.Keep().Print("fragments_mod6");
    }

    // Sort/Merge and map to only suffix array

    using StringFragment = dc7_local::StringFragment<Index, Char>;

    auto string_fragments_mod0 =
        fragments_mod0
        .Map([](const StringFragmentMod0& mod0)
             { return StringFragment(mod0); });

    auto string_fragments_mod1 =
        fragments_mod1
        .Map([](const StringFragmentMod1& mod1)
             { return StringFragment(mod1); });

    auto string_fragments_mod2 =
        fragments_mod2
        .Map([](const StringFragmentMod2& mod2)
             { return StringFragment(mod2); });

    auto string_fragments_mod3 =
        fragments_mod3
        .Map([](const StringFragmentMod3& mod3)
             { return StringFragment(mod3); });

    auto string_fragments_mod4 =
        fragments_mod4
        .Map([](const StringFragmentMod4& mod4)
             { return StringFragment(mod4); });

    auto string_fragments_mod5 =
        fragments_mod5
        .Map([](const StringFragmentMod5& mod5)
             { return StringFragment(mod5); });

    auto string_fragments_mod6 =
        fragments_mod6
        .Map([](const StringFragmentMod6& mod6)
             { return StringFragment(mod6); });

    auto suffix_array =
        Union(string_fragments_mod0,
              string_fragments_mod1,
              string_fragments_mod2,
              string_fragments_mod3,
              string_fragments_mod4,
              string_fragments_mod5,
              string_fragments_mod6)
        .Sort(dc7_local::FragmentComparator<StringFragment>())
        .Execute();

    // debug output

    if (debug_print) {
        std::vector<Char> input_vec = input_dia.Keep().Gather();
        std::vector<Index> vec =
            suffix_array.Keep()
            .Map([](const StringFragment& a) { return a.index; })
            .Gather();

        if (ctx.my_rank() == 0) {
            size_t p = 0;
            for (const Index& index : vec) {
                std::cout << std::setw(5) << p << std::setw(5) << index << " =";
                for (Index i = index;
                     i < index + Index(64) && i < Index(input_size); ++i) {
                    std::cout << ' ' << uint64_t(input_vec[i]);
                }
                std::cout << '\n';
                ++p;
            }
        }
    }

    // check intermediate result, requires an input_dia.Keep() above!
    // die_unless(CheckSA(input_dia, suffix_array.Keep()));

    return suffix_array.Collapse();
}

template <typename Index, typename InputDIA>
DIA<Index> DC7(const InputDIA& input_dia, size_t input_size, size_t K) {

    using Char = typename InputDIA::ValueType;
    using StringFragment = dc7_local::StringFragment<Index, Char>;

    return DC7Recursive<Index>(input_dia, input_size, K)
           .Map([](const StringFragment& a) { return a.index; })
           .Collapse();
}

template DIA<uint32_t> DC7<uint32_t>(
    const DIA<uint8_t>& input_dia, size_t input_size, size_t K);

#if !THRILL_ON_TRAVIS

template DIA<common::uint40> DC7<common::uint40>(
    const DIA<uint8_t>& input_dia, size_t input_size, size_t K);

template DIA<uint64_t> DC7<uint64_t>(
    const DIA<uint8_t>& input_dia, size_t input_size, size_t K);

#endif

} // namespace suffix_sorting
} // namespace examples

/******************************************************************************/
