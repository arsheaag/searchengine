import json
from query_processor import preprocess_query, boolean_and_query
from scoring import compute_combined_score

def load_inverted_index(file_path):
    """Load the inverted index, document lookup, PageRank scores, summaries, and total document count."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    inverted_index = data["index"]
    doc_lookup = data["document_lookup"]
    pagerank_scores = data.get("pagerank_scores", {})
    document_summaries = data.get("document_summaries", {})  # Load summaries
    total_docs = data["total_documents"]

    return inverted_index, doc_lookup, pagerank_scores, document_summaries, total_docs  # Return summaries

def search(query, inverted_index, doc_lookup, pagerank_scores, document_summaries, total_docs):
    """Process the query, retrieve matching documents via Boolean AND, and return TF-IDF + PageRank scores."""
    query_tokens = preprocess_query(query)
    matching_docs = boolean_and_query(query_tokens, inverted_index)

    if not matching_docs:
        print("\nNo results found.")
        return []

    doc_scores = []
    for doc_id in matching_docs:
        score = compute_combined_score(str(doc_id), query_tokens, inverted_index, total_docs,
                                       pagerank_scores)
        url = doc_lookup.get(str(doc_id), "URL Not Found")
        #summary = document_summaries.get(str(doc_id), "Summary not available.")  # Retrieve saved summary
        summary = "Summarization disabled."
        doc_scores.append((doc_id, score, url, summary))  # Now includes summaries

    doc_scores.sort(key=lambda x: x[1], reverse=True)
    return doc_scores[:5]  # Return top 5 results

