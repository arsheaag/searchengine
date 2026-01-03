import os
import json

# from summarizer import generate_summary

def build_inverted_index(documents):
    """
    Builds an inverted index from the given tokenized documents.
    Now also generates and stores summaries.
    """
    print(f"Debug: Received {len(documents)} documents for indexing.")  # Debugging line
    inverted_index = {}
    document_lookup = {}
    document_summaries = {}  # ✅ Store summaries

    for doc_id, document in enumerate(documents):
        url = document["url"]
        regular_tokens = document["regular_tokens"]
        important_tokens = document["important_tokens"]

        document_lookup[doc_id] = url

        term_frequencies = {}

        for token in regular_tokens:
            term_frequencies[token] = term_frequencies.get(token, 0) + 1

        for token in important_tokens:
            term_frequencies[token] = term_frequencies.get(token, 0) + 2  # Boost important words

        for token, freq in term_frequencies.items():
            if token not in inverted_index:
                inverted_index[token] = {"documents": [], "frequency": []}
            inverted_index[token]["documents"].append(doc_id)
            inverted_index[token]["frequency"].append(freq)

        # ✅ Generate and store summary
        full_text = " ".join(regular_tokens[:200])  # Use first 200 tokens for summary
        #summary = generate_summary(full_text)
        #document_summaries[doc_id] = summary

    print(f"Debug: Indexed {len(document_lookup)} documents.")  # Debugging line

    return inverted_index, document_lookup, document_summaries  # ✅ Return summaries


def save_index(index, doc_lookup, summaries, pagerank_scores, total_files_read, filename="../index/inverted_index.json"):
    """
    Saves the inverted index, document lookup, summaries, and PageRank scores to a JSON file.
    """
    index_folder = os.path.dirname(filename)

    if not os.path.exists(index_folder):
        os.makedirs(index_folder)

    full_index = {
        "total_files_read": total_files_read,
        "total_documents": len(doc_lookup),
        "unique_words": len(index),
        "index_size_kb": os.path.getsize(filename) // 1024 if os.path.exists(filename) else 0,
        "pagerank_scores": pagerank_scores,  # ✅ Save PageRank scores
        "index": index,
        "document_lookup": doc_lookup,
        #"document_summaries": summaries  # ✅ Save summaries
    }

    class SingleLineJSONEncoder(json.JSONEncoder):
        def encode(self, obj):
            if isinstance(obj, list):
                return "[" + ", ".join(map(str, obj)) + "]"
            return super().encode(obj)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(full_index, file, indent=4, separators=(",", ": "), cls=SingleLineJSONEncoder)

    print(f"Inverted index saved to {filename}")
