/*******************************************************************************
 * cobs/cortex_file.hpp
 *
 * Copyright (c) 2018 Florian Gauger
 * Copyright (c) 2018 Timo Bingmann
 *
 * All rights reserved. Published under the MIT License in the LICENSE file.
 ******************************************************************************/

#ifndef COBS_CORTEX_FILE_HEADER
#define COBS_CORTEX_FILE_HEADER

#include <string>
#include <vector>

#include <cobs/kmer_buffer.hpp>
#include <cobs/util/file.hpp>
#include <cobs/util/fs.hpp>
#include <cobs/util/string_view.hpp>
#include <cobs/util/timer.hpp>
#include <cstring>
#include <iomanip>
#include <sstream>

#include <tlx/die.hpp>
#include <tlx/unused.hpp>

namespace cobs {

class CortexFile
{
public:
    CortexFile(std::string path) {
        is_.open(path);
        die_unless(is_.good());
        read_header(is_, path);
    }

    template <typename Type>
    static inline Type cast_advance(std::istream& is) {
        Type t;
        is.read(reinterpret_cast<char*>(&t), sizeof(t));
        return t;
    }

    static void check_magic_number(std::istream& is, std::string path) {
        std::string magic_word = "CORTEX";
        for (size_t i = 0; i < magic_word.size(); i++) {
            if (is.get() != magic_word[i]) {
                throw std::invalid_argument(
                          "CortexFile: magic number not found @ " + path);
            }
        }
    }

    void read_header(std::istream& is, std::string path) {
        check_magic_number(is, path);
        version_ = cast_advance<uint32_t>(is);
        if (version_ != 6)
            die("Invalid .ctx file version (" << version_);

        kmer_size_ = cast_advance<uint32_t>(is);
        die_unequal(kmer_size_, 31u);
        num_words_per_kmer_ = cast_advance<uint32_t>(is);
        num_colors_ = cast_advance<uint32_t>(is);
        if (num_colors_ != 1)
            die("Invalid number of colors (" << num_colors_ << "), must be 1");

        for (size_t i = 0; i < num_colors_; i++) {
            uint32_t mean_read_length = cast_advance<uint32_t>(is);
            uint64_t total_length = cast_advance<uint64_t>(is);
            tlx::unused(mean_read_length, total_length);
        }
        for (size_t i = 0; i < num_colors_; i++) {
            auto document_name_length = cast_advance<uint32_t>(is);
            name_.resize(document_name_length);
            is.read(const_cast<char*>(name_.data()), document_name_length);
        }
        is.ignore(16 * num_colors_);
        for (size_t i = 0; i < num_colors_; i++) {
            is.ignore(12);
            auto length_graph_name = cast_advance<uint32_t>(is);
            is.ignore(length_graph_name);
        }
        check_magic_number(is, path);

        pos_data_begin_ = is.tellg();
        is.seekg(0, std::ios::end);
        pos_data_end_ = is.tellg();
    }

    size_t num_kmers() const {
        return (pos_data_end_ - pos_data_begin_)
               / (8 * num_words_per_kmer_ + 5 * num_colors_);
    }

    template <unsigned N, typename Callback>
    void process_kmers(size_t term_size, Callback callback) {
        std::string term(N, 0);
        KMer<N> kmer;
        auto kmer_data = reinterpret_cast<char*>(kmer.data());

        size_t num_uint8_ts_per_kmer = 8 * num_words_per_kmer_;
        die_unequal(num_uint8_ts_per_kmer, kmer.size);

        is_.clear();
        is_.seekg(pos_data_begin_);

        size_t r = num_kmers();
        while (r != 0) {
            --r;
            if (!is_.good())
                die("corrupted .ctx file");

            is_.read(kmer_data, num_uint8_ts_per_kmer);
            is_.ignore(5 * num_colors_);

            kmer.to_string(&term);
            for (size_t i = 0; i + term_size <= N; ++i) {
                callback(string_view(term.data() + i, term_size));
            }
        }
    }

    template <typename Callback>
    void process_terms(size_t term_size, Callback callback) {
        if (kmer_size_ == 31) {
            return process_kmers<31>(term_size, callback);
        }
        else {
            die("CortexFile: unsupported kmer_size_ " << kmer_size_);
        }
    }

    uint32_t version_;
    uint32_t kmer_size_;
    uint32_t num_words_per_kmer_;
    uint32_t num_colors_;
    std::string name_;

private:
    std::ifstream is_;
    std::istream::pos_type pos_data_begin_, pos_data_end_;
};

} // namespace cobs

#endif // !COBS_CORTEX_FILE_HEADER

/******************************************************************************/
