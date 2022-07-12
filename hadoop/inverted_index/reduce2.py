#!/usr/bin/env python3
"""Word count reducer."""
from cmath import log
import sys
import itertools
from math import log10


def reduce_one_group(key, group, n):
    """Reduce one group."""
    # for key, group in itertools.groupby(sys.stdin, keyfunc):
    #     reduce_one_group(key, group)
    term_doc_freq = {}

    # get n_k below
    for line in group:
        line_info = line.split()
        doc_id = line_info[1]
        term_tfik = line_info[2]
        if key in term_doc_freq:
            term_doc_freq[key].append([key, doc_id, term_tfik])
        else:
            term_doc_freq[key] = [[key, doc_id, term_tfik]]

    # calculate idf_k below.
    for term in term_doc_freq.keys():
        n_k = len(term_doc_freq[term])
        for term_doc in term_doc_freq[term]:
            # print(f"term {term}", file=sys.stderr)
            # print(f"term_doc {term_doc}", file=sys.stderr)
            doc_id = term_doc[1]
            term_tfik = term_doc[2]
            # print(f"n: {n}, n_k {n_k}, n/n_k {float(n)/float(n_k)}",
            #       file=sys.stderr)
            idf_k = log10(float(n)/float(n_k))
            # print(f"idf_k: {idf_k}", file=sys.stderr)
            print(f"{term}\t{doc_id} {term_tfik} {idf_k}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    # read in N (total document count) below
    n = 0
    with open('total_document_count.txt', 'r') as n_file:
        line = n_file.readline()
        # print(f"line: {line}", file=sys.stderr)
        n = int(line)
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group, n)


if __name__ == "__main__":
    main()
