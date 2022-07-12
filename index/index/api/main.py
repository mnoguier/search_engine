"""
This is required.

Description.
"""
# import json
import pathlib
import re
import math
from copy import deepcopy
import sys
import flask
import index


class Words():
    """Style Req."""

    def __init__(self):
        """Style Req."""
        self.stop_words = {}
        self.page_rank = {}
        self.inverted_index = {}

    def read_stopwords(self, index_dir):
        """Style Req."""
        with open(str(index_dir) + "/stopwords.txt", 'r', encoding="utf8"
                  ) as stop_file:
            for line in stop_file.readlines():
                self.stop_words[line.strip()] = True

    def read_pagerank(self, index_dir):
        """Style Req."""
        with open(str(index_dir) + "/pagerank.out", encoding="utf8"
                  ) as page_rank_file:
            # comma seperated terms, where 2 values per line
            # doc_id,page_rank
            for line in page_rank_file.readlines():
                doc_id = line.split(',')[0]
                page_rank = line.split(',')[1]
                self.page_rank[doc_id] = page_rank

    def read_inverted_index(self, index_dir):
        """Style Req."""
        # term\tval
        #
        file = index.app.config["INDEX_PATH"]
        print("inverted_index file: ", file, '\n\n', file=sys.stderr)
        with open(str(index_dir) +
                  f"/inverted_index/{file}", 'r', encoding="utf8"
                  ) as inverted_index:
            for line in inverted_index.readlines():
                term = line.split('\t')[0]
                val = line.split('\t')[1]
                self.inverted_index[term] = val

    def clean_line(self, line: str) -> str:
        """Pylint req."""
        terms = re.sub(r"[^a-zA-Z0-9 ]+", "", line)
        # Convert upper case characters to lower case using casefold()
        terms = terms.casefold()
        terms = terms.split()
        # print(f"terms {terms}", file=sys.stderr)
        # Split the text into whitespace-delimited terms.
        terms_return = []
        for word in terms:
            # print(f"word: {word}", file=sys.stderr)
            if word not in self.stop_words:
                # print(f"in with word {word}", file=sys.stderr)
                terms_return.append(word)
        # print(f"terms: {terms_return}", file=sys.stderr)
        return terms_return


words = Words()


@index.app.before_first_request
def startup():
    """Load inverted index, pagerank, and stopwords into memory."""
    # how do we access these now
    index_dir = pathlib.Path(__file__).parent.parent
    words.read_stopwords(index_dir)
    words.read_pagerank(index_dir)
    words.read_inverted_index(index_dir)


def get_good_doc_ids(query, new_query):
    """Style Req."""
    doc_id_term = {}
    print("new_query", new_query)
    for word in new_query:
        # print("word", word)
        # Split the value so we can extract the doc_ids
        term_value = ''
        if word in words.inverted_index:
            term_value = words.inverted_index[word]
        # print("term_value before", term_value)
        # print("term_value", term_value)
        # get all of the doc_ids from term_value
        # print("term_value before 1", term_value)
        term_value = term_value.split()[1:][::3]
        # print("term_value after", term_value)
        for doc_id in term_value:
            if doc_id not in doc_id_term:
                doc_id_term[doc_id] = 1
            else:
                doc_id_term[doc_id] += 1
    good_docs = {}
    print("doc_id_term", doc_id_term)
    for doc in doc_id_term.items():
        doc_id = doc[0]
        if doc_id_term[doc_id] == len(query):
            good_docs[doc_id] = 0
    print("good_docs 1", good_docs)
    return good_docs


def create_doc_vecs(query, good_docs):
    """Style Req."""
    print("entering create_doc_vecs")
    doc_vecs = {}
    print("good_docs 2", good_docs)
    print("query 2", query)
    for word in query:
        print("\n word", word)
        # idf = float(words.inverted_index[word].split('\t')[1].split()[0])
        # Split the value so we can extract the doc_ids and tf
        term_value = ''
        idf_k = 0.0
        print("word in ii", word in words.inverted_index)
        if word in words.inverted_index:
            # print("in ii")
            term_value = deepcopy(words.inverted_index[word])
            # print("term_value", term_value)
            term_value = term_value.split()
            idf_k = float(term_value[0])
            term_value.pop(0)
        print("term_value", term_value)
        # get all of the doc_ids from term_value
        # we have idf. Now we need to increment by 3. Need doc_id,
        # tf, d_i during each interation.
        # idf
        # 0001	 3.0371607931407154 5234576 2 27383.875993769438
        # 5702 2 126918.90181137579
        # print("len(term_value)", len(term_value), "\n\n")
        while len(term_value) > 0:
            doc_id = term_value[0]
            term_freq = float(term_value[1])
            d_i = term_value[2]
            # print("doc_id", doc_id, "term_freq", term_freq, "d_i", d_i)
            # weird issues, try pop 3 times
            term_value = term_value[3:]
            # print("term_value", term_value)
            if doc_id in good_docs:
                if doc_id not in doc_vecs:
                    doc_vecs[doc_id] = [d_i, term_freq * idf_k]
                else:
                    doc_vecs[doc_id].append(term_freq * idf_k)
        # print("doc_vecs", doc_vecs)
    return doc_vecs


def tf_idf_calc(query_vec, doc_vecs, weight):
    """Style Req."""
    # get dot product (Mathieu Definitely)

    # normalized query vec value

    norm_q = 0.0
    dot_prod = 0
    for term in query_vec.keys():
        norm_q += query_vec[term]**2
    norm_q = math.sqrt(norm_q)

    # Compute the normalization factor for the document,
    # which is the square root of the normalization factor
    # read from the inverted Index.
    score_vec = {}
    print("doc_vecs", doc_vecs)
    for doc in doc_vecs.keys():
        print("doc", doc)
        # Calulate norm_d
        doc_v = doc_vecs[doc]
        norm_d = math.sqrt(float(doc_v[0]))
        doc_v = doc_v[1:]
        # doc_v and query_vec
        dot_prod = sum(float(x) * float(y) for x, y in zip(doc_v,
                                                           query_vec.values()))
        # while len(doc_vec) > 0:
        # print("dot_prod", dot_prod, "norm_q", norm_q, "norm_d", norm_d)
        tfidf = dot_prod / (norm_q * norm_d)
        score = float(weight) * float(words.page_rank[doc]) \
            + (1 - float(weight)) * tfidf
        score_vec[score] = doc
    hits = {"hits": []}
    # sort the score_vec by score. format it and return
    print("score_vec", score_vec)
    for score in sorted(score_vec.keys(), reverse=True):
        doc_id = score_vec[score]
        print("doc_id", doc_id, "score", score)
        hits["hits"].append(
            {
                "docid": int(doc_id),
                "score": score
            })
    return hits


@index.app.route('/api/v1/', methods=['GET'])
def get_basic():
    """Style Req."""
    msg = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    msg = flask.jsonify(**msg)
    msg.status_code = 200
    return msg


@index.app.route('/api/v1/hits/', methods=['GET'])
def get_hits():
    """Style Req."""
    # args
    # querry: from user, diff every time
    # weight: optional from user, 0.5 default val
    query = flask.request.args.get("q", default="", type=str)
    weight = flask.request.args.get("w", default=0.5)
    # clean the query: same as for inverted index
    query = words.clean_line(query)
    print("QUERY: ", query, '\n\n')
    # {key: term, value {docid:tf}}
    # term_info = words.inverted_index[term in query]
    #
    # {docid: term_count}
    # Go through all the documents and find the docs that contain
    # all terms in the query.
    # Suggestion: loop though cleaned query term by term and get
    # the values from the inverted_index
    # Then extract all of the doc_ids from the value as well as
    # their term frequence
    # Maybe store in a dict (key: term, value: [doc_id, tf])
    # Create good_doc_id dict, with (key: doc_id, value:
    # (tf of each term in the query))
    # Generate query vector: See Appendix A (Easy)
    # Generate document vector: See Appendix A (Hard)
    #   Suggestion 1: Have a dict of doc_ids, where the value is the
    # doc_vector for the document
    #               Loop though dict of doc_vectors
    #                   Calculate tf-idf -> calculate the score -> store
    # in dict with doc_id and score as key,value pair
    #                   Order can be changed depending on how we want to
    # handle sorting

    # Go though all terms in query and find the document/s that contain
    # all of the terms (in the querry)
    # # Find docs with all query args
    query_vec = {}
    new_query = []
    for word in query:
        # print("word", word)
        if word not in query_vec:
            query_vec[word] = 1
            new_query.append(word)
        else:
            query_vec[word] += 1
    # calculate query vec values
    print("query_vec", query_vec)
    for word in query_vec.items():
        if word[0] in words.inverted_index:
            idf = float(words.inverted_index[word[0]].split()[0])
            query_vec[word[0]] = query_vec[word[0]] * idf
    print("query_vec", query_vec)
    # get good doc_ids
    good_docs = get_good_doc_ids(query, new_query)
    # print("good_docs", good_docs)
    # # get PageRank for ___ docs. Unecessary
    # for doc_id in good_docs:
    #     good_docs[doc_id] = words.pagerank[doc_id]
    # loop though query terms
    # get the values in the inverted_index for each term,
    # if doc_id is in good_doc:
    # add the tf to a dict where the doc_id is they key and a list of tf
    # values is the key
    # doc_vecs = {key: doc_id, value: [tf, tf]}
    # Create a dictionary of all of the document vectors
    print("before create_doc_vecs")
    doc_vecs = create_doc_vecs(query, good_docs)
    print("after create_doc_vecs")
    # tf-idf calculation
    hits = tf_idf_calc(query_vec, doc_vecs, weight)
    print("hits", hits)
    return flask.jsonify(hits)
