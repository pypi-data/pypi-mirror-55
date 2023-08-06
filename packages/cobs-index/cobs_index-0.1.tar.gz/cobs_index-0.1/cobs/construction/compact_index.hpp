/*******************************************************************************
 * cobs/construction/compact_index.hpp
 *
 * Copyright (c) 2018 Florian Gauger
 *
 * All rights reserved. Published under the MIT License in the LICENSE file.
 ******************************************************************************/

#ifndef COBS_CONSTRUCTION_COMPACT_INDEX_HEADER
#define COBS_CONSTRUCTION_COMPACT_INDEX_HEADER

#include <cobs/util/fs.hpp>
#include <cobs/util/misc.hpp>

/*!
 * The compact Inverted Signature Index with the space-saving improvements.
 * This namespace provides methods for creation of this index. It can either be
 * constructed from existing documents or with random dummy data for performance
 * testing purposes. The index uses different signature sizes to minimize space
 * wastage.
 */
namespace cobs {

struct CompactIndexParameters {
    //! length of terms / k-mers
    unsigned term_size = 31;
    //! canonicalization flag for base pairs
    uint8_t canonicalize = 0;
    //! number of hash functions, provided by user
    unsigned num_hashes = 1;
    //! false positive rate, provided by user
    double false_positive_rate = 0.3;
    //! page or block size of filters with common fpr
    uint64_t page_size = 0;
    //! memory to use bytes to create index
    uint64_t mem_bytes = get_memory_size(80);
    //! number of threads to use
    size_t num_threads = gopt_threads;
    //! clobber erase output directory if it exists, default: false
    bool clobber = false;
    //! continue in existing output directory, default: false
    bool continue_ = false;
    //! keep temporary files during construction, default: false
    bool keep_temporary = false;
};

/*!
 * Constructs the folders used by the cobs::compact_index::construct.  Sorts the
 * documents by file size and then splits them into several directories.
 */
void compact_construct(
    DocumentList doc_list, const fs::path& index_dir,
    fs::path tmp_path, CompactIndexParameters index_params);

void compact_combine_into_compact(
    const fs::path& in_dir, const fs::path& out_file,
    uint64_t page_size = get_page_size(),
    uint64_t memory = get_memory_size(80),
    bool keep_temporary = false);

} // namespace cobs

#endif // !COBS_CONSTRUCTION_COMPACT_INDEX_HEADER

/******************************************************************************/
