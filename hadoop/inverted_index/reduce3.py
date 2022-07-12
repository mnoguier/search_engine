#!/usr/bin/env python3
"""Word count reducer."""
import sys
import itertools

from isort import file
# In: Key, value pairs (key: doc_id, value:  term, tf_ik, idf_k)
#       "{term}\t{term} {doc_id} {term_tfik} {idf_k}"
# During: Calculate w_ik for each term in each document
# Out: term, doc_id, w_ik


def reduce_one_group(key, group):
    """Reduce one group."""
    for line in group:
        # print(f"line: {line}", file=sys.stderr)
        term_info = line.split('\t')[1].split()
        # print(f"key {key}", file=sys.stderr)
        # print(f"term_info {term_info}", file=sys.stderr)
        doc_id = str(term_info[0])
        term_tfik = str(term_info[1])
        idf_k = str(term_info[2])
        w_ik = str(float(term_tfik)*float(idf_k))
        print(f"{key}\t{doc_id} {term_tfik} {idf_k} {w_ik}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
