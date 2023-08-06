/***************************************************************************
 *  foxxll/io/iostats.hpp
 *
 *  Part of FOXXLL. See http://foxxll.org
 *
 *  Copyright (C) 2002-2004 Roman Dementiev <dementiev@mpi-sb.mpg.de>
 *  Copyright (C) 2008-2010 Andreas Beckmann <beckmann@cs.uni-frankfurt.de>
 *  Copyright (C) 2009, 2010 Johannes Singler <singler@kit.edu>
 *  Copyright (C) 2016 Alex Schickedanz <alex@ae.cs.uni-frankfurt.de>
 *  Copyright (C) 2017 Manuel Penschuck <manuel@ae.cs.uni-frankfurt.de>
 *
 *  Distributed under the Boost Software License, Version 1.0.
 *  (See accompanying file LICENSE_1_0.txt or copy at
 *  http://www.boost.org/LICENSE_1_0.txt)
 **************************************************************************/

#ifndef FOXXLL_IO_IOSTATS_HEADER
#define FOXXLL_IO_IOSTATS_HEADER

#include <algorithm>
#include <iostream>
#include <limits>
#include <list>
#include <mutex>
#include <string>
#include <utility>
#include <vector>

#include <tlx/logger/core.hpp>
#include <tlx/string.hpp>
#include <tlx/unused.hpp>

#include <foxxll/common/error_handling.hpp>
#include <foxxll/common/timer.hpp>
#include <foxxll/common/types.hpp>
#include <foxxll/common/utils.hpp>
#include <foxxll/singleton.hpp>

namespace foxxll {

//! \addtogroup foxxll_iolayer
//!
//! \{

class file_stats
{
    //! associated device id
    const unsigned device_id_;

    //! number of operations: read/write
    unsigned read_count_, write_count_;
    //! number of bytes read/written
    external_size_type read_bytes_, write_bytes_;
    //! seconds spent in operations
    double read_time_, write_time_;
    //! start time of parallel operation
    double p_begin_read_, p_begin_write_;

    //! number of requests, participating in parallel operation
    int acc_reads_, acc_writes_;

    std::mutex read_mutex_, write_mutex_;

public:
    //! construct zero initialized
    explicit file_stats(unsigned int device_id);

    class scoped_read_write_timer
    {
        using size_type = size_t;
        file_stats& file_stats_;

        bool is_write_;
        bool running_ = false;

    public:
        explicit scoped_read_write_timer(
            file_stats* file_stats, size_type size, bool is_write = false)
            : file_stats_(*file_stats), is_write_(is_write)
        {
            start(size);
        }

        ~scoped_read_write_timer()
        {
            stop();
        }

        void start(size_type size)
        {
            if (!running_) {
                running_ = true;
                if (is_write_)
                    file_stats_.write_started(size);
                else
                    file_stats_.read_started(size);
            }
        }

        void stop()
        {
            if (running_) {
                if (is_write_)
                    file_stats_.write_finished();
                else
                    file_stats_.read_finished();
                running_ = false;
            }
        }
    };

    class scoped_write_timer
    {
        using size_type = size_t;
        file_stats& file_stats_;

        bool running_ = false;

    public:
        explicit scoped_write_timer(file_stats* file_stats, size_type size)
            : file_stats_(*file_stats)
        {
            start(size);
        }

        ~scoped_write_timer()
        {
            stop();
        }

        void start(size_type size)
        {
            if (!running_) {
                running_ = true;
                file_stats_.write_started(size);
            }
        }

        void stop()
        {
            if (running_) {
                file_stats_.write_finished();
                running_ = false;
            }
        }
    };

    class scoped_read_timer
    {
        using size_type = size_t;
        file_stats& file_stats_;

        bool running_ = false;

    public:
        explicit scoped_read_timer(file_stats* file_stats, size_type size)
            : file_stats_(*file_stats)
        {
            start(size);
        }

        ~scoped_read_timer()
        {
            stop();
        }

        void start(size_type size)
        {
            if (!running_) {
                running_ = true;
                file_stats_.read_started(size);
            }
        }

        void stop()
        {
            if (running_) {
                file_stats_.read_finished();
                running_ = false;
            }
        }
    };

public:
    //! Returns the device id.
    //! \return device id
    unsigned get_device_id() const
    {
        return device_id_;
    }

    //! Returns total number of read_count_.
    //! \return total number of read_count_
    unsigned get_read_count() const
    {
        return read_count_;
    }

    //! Returns total number of write_count_.
    //! \return total number of write_count_
    unsigned get_write_count() const
    {
        return write_count_;
    }

    //! Returns number of bytes read from disks.
    //! \return number of bytes read
    external_size_type get_read_bytes() const
    {
        return read_bytes_;
    }

    //! Returns number of bytes written to the disks.
    //! \return number of bytes written
    external_size_type get_write_bytes() const
    {
        return write_bytes_;
    }

    //! Time that would be spent in read syscalls if all parallel read_count_
    //! were serialized.
    //! \return seconds spent in reading
    double get_read_time() const
    {
        return read_time_;
    }

    //! Time that would be spent in write syscalls if all parallel write_count_
    //! were serialized.
    //! \return seconds spent in writing
    double get_write_time() const
    {
        return write_time_;
    }

    // for library use
    void write_started(const size_t size_, double now = 0.0);
    void write_canceled(const size_t size_);
    void write_finished();
    void write_op_finished(const size_t size_, double duration);

    void read_started(const size_t size_, double now = 0.0);
    void read_canceled(const size_t size_);
    void read_finished();
    void read_op_finished(const size_t size_, double duration);
};

class file_stats_data
{
    //! device id
    unsigned device_id_;
    //! number of operations
    unsigned read_count_, write_count_;
    //! number of bytes read/written
    external_size_type read_bytes_, write_bytes_;
    //! seconds spent in operations
    double read_time_, write_time_;

public:
    file_stats_data()
        : device_id_(std::numeric_limits<unsigned>::max()),
          read_count_(0), write_count_(0),
          read_bytes_(0), write_bytes_(0),
          read_time_(0.0), write_time_(0.0)
    { }

    //! construct file_stats_data by taking current values from file_stats
    explicit file_stats_data(const file_stats& fs)
        : device_id_(fs.get_device_id()),
          read_count_(fs.get_read_count()),
          write_count_(fs.get_write_count()),
          read_bytes_(fs.get_read_bytes()),
          write_bytes_(fs.get_write_bytes()),
          read_time_(fs.get_read_time()),
          write_time_(fs.get_write_time())
    { }

    file_stats_data operator + (const file_stats_data& a) const;
    file_stats_data operator - (const file_stats_data& a) const;

    unsigned get_device_id() const
    {
        return device_id_;
    }

    unsigned get_read_count() const
    {
        return read_count_;
    }

    unsigned get_write_count() const
    {
        return write_count_;
    }

    external_size_type get_read_bytes() const
    {
        return read_bytes_;
    }

    external_size_type get_write_bytes() const
    {
        return write_bytes_;
    }

    double get_read_time() const
    {
        return read_time_;
    }

    double get_write_time() const
    {
        return write_time_;
    }
};

//! Collects various I/O statistics.
//! \remarks is a singleton
class stats : public singleton<stats>
{
    friend class singleton<stats>;
    friend class file_stats;

    const double creation_time_;

    //! need std::list here, because the io::file objects keep a pointer to the
    //! enclosed file_stats objects and this list may grow.
    std::list<file_stats> file_stats_list_;

    mutable std::mutex list_mutex_;

    // *** parallel times have to be counted globally ***

    //! seconds spent in parallel operations
    double p_reads_, p_writes_;
    //! start time of parallel operation
    double p_begin_read_, p_begin_write_;
    // seconds spent in all parallel I/O operations (read and write)
    double p_ios_;
    double p_begin_io_;

    // number of requests, participating in parallel operation
    int acc_reads_, acc_writes_;
    int acc_ios_;

    // *** waits are measured globally ***

    // seconds spent waiting for completion of I/O operations
    double t_waits_, p_waits_;
    double p_begin_wait_;
    double t_wait_read_, p_wait_read_;
    double p_begin_wait_read_;
    double t_wait_write_, p_wait_write_;
    double p_begin_wait_write_;
    int acc_waits_;
    int acc_wait_read_, acc_wait_write_;

    std::mutex wait_mutex_, read_mutex_, write_mutex_, io_mutex_;

    //! private construction from singleton
    stats();

public:
    enum wait_op_type {
        WAIT_OP_ANY,
        WAIT_OP_READ,
        WAIT_OP_WRITE
    };

    class scoped_wait_timer
    {
#ifndef FOXXLL_DO_NOT_COUNT_WAIT_TIME
        bool running_ = false;
        wait_op_type wait_op_;
#endif

    public:
        explicit scoped_wait_timer(wait_op_type wait_op, bool measure_time = true)
#ifndef FOXXLL_DO_NOT_COUNT_WAIT_TIME
            : wait_op_(wait_op)
#endif
        {
            if (measure_time)
                start();
        }

        ~scoped_wait_timer()
        {
            stop();
        }

        void start()
        {
#ifndef FOXXLL_DO_NOT_COUNT_WAIT_TIME
            if (!running_) {
                running_ = true;
                stats::get_instance()->wait_started(wait_op_);
            }
#endif
        }

        void stop()
        {
#ifndef FOXXLL_DO_NOT_COUNT_WAIT_TIME
            if (running_) {
                stats::get_instance()->wait_finished(wait_op_);
                running_ = false;
            }
#endif
        }
    };

public:
    //! return list of file's stats data (deeply copied from each file_stats)
    std::vector<file_stats_data> deepcopy_file_stats_data_list() const;

    double get_creation_time() const
    {
        return creation_time_;
    }

    //! create new instance of a file_stats for an io::file to collect
    //! statistics. (for internal library use.)
    file_stats * create_file_stats(unsigned device_id);

    //! I/O wait time counter.
    //! \return number of seconds spent in I/O waiting functions \link
    //! request::wait request::wait \endlink, \c wait_any and \c wait_all
    double get_io_wait_time() const
    {
        return t_waits_;
    }

    double get_wait_read_time() const
    {
        return t_wait_read_;
    }

    double get_wait_write_time() const
    {
        return t_wait_write_;
    }

    //! Period of time when at least one I/O thread was executing a read.
    //! \return seconds spent in reading
    double get_pread_time() const
    {
        return p_reads_;
    }

    //! Period of time when at least one I/O thread was executing a write.
    //! \return seconds spent in writing
    double get_pwrite_time() const
    {
        return p_writes_;
    }

    //! Period of time when at least one I/O thread was executing a read or a write.
    //! \return seconds spent in I/O
    double get_pio_time() const
    {
        return p_ios_;
    }

    friend std::ostream& operator << (std::ostream& o, const stats& s);

    // for library use

private:
    // only called from file_stats
    void p_write_started(double now);
    void p_write_finished(double now);
    void p_read_started(double now);
    void p_read_finished(double now);

public:
    void wait_started(wait_op_type wait_op_);
    void wait_finished(wait_op_type wait_op_);
};

#ifdef FOXXLL_DO_NOT_COUNT_WAIT_TIME
inline void stats::wait_started(wait_op_type) { }
inline void stats::wait_finished(wait_op_type) { }
#endif

class stats_data
{
    //! seconds spent in parallel io
    double p_reads_, p_writes_, p_ios_;

    //! seconds spent waiting for completion of I/O operations
    double t_wait;
    double t_wait_read_, t_wait_write_;

    double elapsed_;

    //! list of individual file statistics.
    std::vector<file_stats_data> file_stats_data_list_;

    //! aggregator
    template <typename T, typename Functor>
    T fetch_sum(const Functor& get_value) const;

public:
    template <typename T>
    struct summary
    {
        T total, min, max;
        double average, median;
        std::vector<std::pair<T, unsigned> > values_per_device;

        template <typename Functor>
        summary(const std::vector<file_stats_data>& fs,
                const Functor& get_value);
    };

public:
    stats_data()
        : p_reads_(0.0), p_writes_(0.0),
          p_ios_(0.0),
          t_wait(0.0),
          t_wait_read_(0.0), t_wait_write_(0.0),
          elapsed_(0.0)
    { }

    stats_data(const stats& s) // implicit conversion -- NOLINT
        : p_reads_(s.get_pread_time()),
          p_writes_(s.get_pwrite_time()),
          p_ios_(s.get_pio_time()),
          t_wait(s.get_io_wait_time()),
          t_wait_read_(s.get_wait_read_time()),
          t_wait_write_(s.get_wait_write_time()),
          elapsed_(timestamp() - s.get_creation_time()),
          file_stats_data_list_(s.deepcopy_file_stats_data_list())
    { }

    stats_data operator + (const stats_data& a) const;
    stats_data operator - (const stats_data& a) const;

    //! Returns the number of file_stats_data objects
    size_t num_files() const;

    //! Returns the sum of all read_count_.
    //! \return the sum of all read_count_
    unsigned get_read_count() const;

    //! Retruns sum, min, max, avarage and median of all read_count_.
    //! \return a summary of the read measurements
    stats_data::summary<unsigned> get_read_count_summary() const;

    //! Returns the sum of all write_count_.
    //! \return the sum of all write_count_
    unsigned get_write_count() const;

    //! Returns sum, min, max, avarage and median of all write_count_.
    //! \returns a summary of the write measurements
    stats_data::summary<unsigned> get_write_count_summary() const;

    //! Returns number of bytes read from disks in total.
    //! \return number of bytes read
    external_size_type get_read_bytes() const;

    //! Returns sum, min, max, avarage and median of all read bytes.
    //! \returns a summary of the write measurements
    stats_data::summary<external_size_type> get_read_bytes_summary() const;

    //! Returns number of bytes written to the disks in total.
    //! \return number of bytes written
    external_size_type get_write_bytes() const;

    //! Returns sum, min, max, avarage and median of all written bytes.
    //! \return a summary of the written bytes
    stats_data::summary<external_size_type> get_write_bytes_summary() const;

    //! Time that would be spent in read syscalls if all parallel read_count_
    //! were serialized.
    //! \return seconds spent in reading
    double get_read_time() const;

    //! Returns sum, min, max, avarage and median of all read times
    //! \return a summary of the read times
    stats_data::summary<double> get_read_time_summary() const;

    //! Time that would be spent in write syscalls if all parallel write_count_
    //! were serialized.
    //! \return the sum of the write times of all files
    double get_write_time() const;

    //! Returns sum, min, max, avarage and median of all write times
    //! \return a summary of the write times
    stats_data::summary<double> get_write_time_summary() const;

    //! Period of time when at least one I/O thread was executing a read.
    //! \return seconds spent in reading
    double get_pread_time() const;

    //! Period of time when at least one I/O thread was executing a write.
    //! \return seconds spent in writing
    double get_pwrite_time() const;

    //! Period of time when at least one I/O thread was executing a read or a write.
    //! \return seconds spent in I/O
    double get_pio_time() const;

    stats_data::summary<double> get_read_speed_summary() const;

    stats_data::summary<double> get_pread_speed_summary() const;

    stats_data::summary<double> get_write_speed_summary() const;

    stats_data::summary<double> get_pwrite_speed_summary() const;

    stats_data::summary<double> get_pio_speed_summary() const;

    //! Retruns elapsed_ time
    //! \remark If stats_data is not the difference between two other stats_data
    //! objects, then this value is measures the time since the first file object
    //! was initialized.
    //! \return elapsed_ time
    double get_elapsed_time() const
    {
        return elapsed_;
    }

    //! I/O wait time counter.
    //! \return number of seconds spent in I/O waiting functions
    double get_io_wait_time() const;

    double get_wait_read_time() const;

    double get_wait_write_time() const;

    void to_ostream(std::ostream& o, const std::string line_prefix = "") const;

    friend std::ostream& operator << (std::ostream& o, const stats_data& s)
    {
        s.to_ostream(o);
        return o;
    }
};

static inline
std::string add_IEC_binary_multiplier(
    const external_size_type number, const std::string& unit = "")
{
    return tlx::format_iec_units(number) + unit;
}

static inline
std::string add_SI_multiplier(
    external_size_type number, const std::string& unit = "")
{
    return tlx::format_si_units(number) + unit;
}

/*!
 * Simple scoped iostats reporter which takes a message and reports the relative
 * IO performance on destruction
 */
class scoped_print_iostats
{
protected:
    //! message
    std::string message_;
    std::string key_;

    //! initial io-stats
    foxxll::stats_data begin_;

    //! bytes processed
    uint64_t bytes_;

    //! report on destruction
    bool report_on_destruction_;

public:
    /*!
     * Start time and configure report-style
     *
     * \param message  Description displayed on the first line of the report
     * \param key      Line prefix displayed at the beginning of every line but the first
     * \param bytes    Used to compute MB/s as an initial overview
     */
    scoped_print_iostats(const std::string& message, const std::string key, uint64_t bytes)
        : message_(message),
          key_(key),
          begin_(*foxxll::stats::get_instance()),
          bytes_(bytes),
          report_on_destruction_(true)
    {
        TLX_LOG1 << "Starting " << message;
    }

    explicit scoped_print_iostats(const std::string& message, uint64_t bytes = 0)
        : scoped_print_iostats(message, "", bytes)
    { }

    explicit scoped_print_iostats(uint64_t bytes = 0)
        : scoped_print_iostats("", bytes)
    { }

    //! stats at initialization
    const foxxll::stats_data & initial_stats() const
    {
        return begin_;
    }

    //! print out relative stats via LOG
    void report() const;

    //! Same as report() but disables reporting on destruction
    void final_report()
    {
        report_on_destruction_ = false;
        report();
    }

    //! on destruction: report stats
    ~scoped_print_iostats()
    {
        if (report_on_destruction_)
            report();
    }
};

//! \}

} // namespace foxxll

#endif // !FOXXLL_IO_IOSTATS_HEADER

/**************************************************************************/
