/*******************************************************************************
 * cobs/query/compact_index/search_file.cpp
 *
 * Copyright (c) 2018 Florian Gauger
 *
 * All rights reserved. Published under the MIT License in the LICENSE file.
 ******************************************************************************/

#include <cobs/query/compact_index/search_file.hpp>

#include <cobs/util/file.hpp>

#include <tlx/die.hpp>

namespace cobs {

CompactIndexSearchFile::CompactIndexSearchFile(const fs::path& path) {
    std::ifstream ifs;
    header_ = deserialize_header<CompactIndexHeader>(ifs, path);
    stream_pos_ = get_stream_pos(ifs);

    // todo assertions that all the data in the Header is correct
    row_size_ = header_.page_size() * header_.parameters().size();
    num_hashes_ = header_.parameters()[0].num_hashes;
    for (const auto& p : header_.parameters()) {
        die_unless(num_hashes_ == p.num_hashes);
    }
}

uint64_t CompactIndexSearchFile::counts_size() const {
    return 8 * header_.parameters().size() * header_.page_size();
}

} // namespace cobs

/******************************************************************************/
