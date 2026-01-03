import math
import numpy as np

def compute_tf_idf_score(doc_id, query_tokens, inverted_index, total_docs):
    """
    Compute the TF-IDF score for a given document (doc_id)
    and a set of query tokens.
    """
    score = 0.0
    doc_id = str(doc_id)  # Ensure doc_id is a string for correct matching
    doc_length = sum(inverted_index.get(doc_id, {}).get("frequency", []))  # Normalize by doc length

    for term in query_tokens:
        if term in inverted_index:
            postings = inverted_index[term]
            doc_list = list(map(str, postings["documents"]))  # Convert doc IDs to strings
            freq_list = postings["frequency"]

            if doc_id in doc_list:
                index = doc_list.index(doc_id)
                tf = freq_list[index] / (doc_length + 1)  # Normalize TF
                df = len(doc_list)
                idf = math.log((total_docs + 1) / (df + 1)) + 1
                score += tf * idf  # Now weighted properly
    return score



def compute_pagerank(document_graph, num_iterations=20, damping_factor=0.85):
    """
    Compute PageRank scores using the power iteration method.
    """
    print("🔄 Starting PageRank computation...")  # Log start of PR

    urls = list(document_graph.keys())
    num_docs = len(urls)
    if num_docs == 0:
        print("⚠️ PageRank skipped: No documents found in the graph.")
        return {}

    url_to_index = {url: i for i, url in enumerate(urls)}
    index_to_url = {i: url for url, i in url_to_index.items()}

    # Initialize adjacency matrix
    link_matrix = np.zeros((num_docs, num_docs))

    for url, outgoing_links in document_graph.items():
        if outgoing_links:
            for link in outgoing_links:
                if link in url_to_index:
                    link_matrix[url_to_index[url], url_to_index[link]] = 1

    # Normalize rows (handle dangling nodes)
    for i in range(num_docs):
        if np.sum(link_matrix[i]) > 0:
            link_matrix[i] /= np.sum(link_matrix[i])
        else:
            link_matrix[i] = np.ones(num_docs) / num_docs  # Handle dangling nodes

    # PageRank initialization
    pr_values = np.ones(num_docs) / num_docs

    for iteration in range(num_iterations):
        pr_values = (1 - damping_factor) / num_docs + damping_factor * link_matrix.T @ pr_values
        if iteration % 5 == 0:  # Log every 5 iterations
            print(f"PageRank Iteration {iteration + 1}/{num_iterations} completed.")

    print("PageRank computation finished!")  # Log completion

    return {index_to_url[i]: pr_values[i] for i in range(num_docs)}


def compute_combined_score(doc_id, query_tokens, inverted_index, total_docs, pagerank_scores):
    """
    Compute a combined score using TF-IDF and PageRank.
    """
    doc_id = str(doc_id)  # Ensure doc_id is a string

    tf_idf_score = compute_tf_idf_score(doc_id, query_tokens, inverted_index, total_docs)
    pagerank_score = pagerank_scores.get(doc_id, 0)  # Get PageRank

    # Scale PageRank dynamically to be comparable to TF-IDF
    if pagerank_score > 0:
        pagerank_weight = max(tf_idf_score) / max(pagerank_scores.values())  # Normalize PR
        pagerank_score *= pagerank_weight  # Scale PageRank appropriately

    return tf_idf_score + pagerank_score  # PageRank now properly influences ranking

