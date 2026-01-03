from tokenizer import tokenize


def preprocess_query(query):
    """
    Tokenize the query using the existing tokenize function,
    which also handles stemming.
    """
    return tokenize(query)


def boolean_and_query(query_tokens, inverted_index, max_results=100):
    """
    Retrieve a set of document IDs that contain all query terms (Boolean AND).
    Limit the number of results to speed up processing.
    """
    if not query_tokens:
        return set()

    doc_sets = []
    for term in query_tokens:
        if term in inverted_index:
            doc_sets.append(set(inverted_index[term]["documents"]))
        else:
            return set()  # If one term is missing, return empty result

    # Sort by the smallest set first (faster intersection)
    doc_sets.sort(key=len)

    result_docs = doc_sets[0]

    for doc_set in doc_sets[1:]:
        result_docs.intersection_update(doc_set)

        # Stop early if max results reached
        if not result_docs or len(result_docs) >= max_results:
            break

    return list(result_docs)[:max_results]  # Return only the top results
