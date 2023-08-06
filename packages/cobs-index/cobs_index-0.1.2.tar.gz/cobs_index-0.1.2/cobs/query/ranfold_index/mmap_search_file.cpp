/*******************************************************************************
 * cobs/query/ranfold_index/mmap_search_file.cpp
 *
 * Copyright (c) 2018 Florian Gauger
 *
 * All rights reserved. Published under the MIT License in the LICENSE file.
 ******************************************************************************/

#include <cobs/query/ranfold_index/mmap_search_file.hpp>
#include <cobs/util/file.hpp>
#include <cobs/util/fs.hpp>
#include <cobs/util/query.hpp>
#include <cstring>

namespace cobs {

RanfoldIndexMMapSearchFile::RanfoldIndexMMapSearchFile(const fs::path& path)
    : RanfoldIndexSearchFile(path)
{
    handle_ = initialize_mmap(path);
    data_ = handle_.data;
}

RanfoldIndexMMapSearchFile::~RanfoldIndexMMapSearchFile() {
    destroy_mmap(handle_);
}

void RanfoldIndexMMapSearchFile::read_from_disk(
    const std::vector<size_t>& /* hashes */, char* /* rows */) {
// #pragma omp parallel for
//     for (size_t i = 0; i < hashes.size(); i++) {
//         auto data_8 = m_data + hashes[i] % m_header.signature_size() * m_header.row_size();
//         auto rows_8 = rows + i * m_header.row_size();
//         std::memcpy(rows_8, data_8, m_header.row_size());
//     }
}

} // namespace cobs

/******************************************************************************/
