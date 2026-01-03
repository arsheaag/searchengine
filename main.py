import sys
import os
import time
import json
import tkinter as tk
from tkinter import scrolledtext
from search import load_inverted_index, search
from read_json_files import read_json_files
from build_index import build_inverted_index, save_index
from scoring import compute_pagerank

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVERTED_INDEX_PATH = os.path.join(BASE_DIR, "index", "inverted_index.json")

def run_indexing():
    """Builds the inverted index only if it's missing."""
    if os.path.exists(INVERTED_INDEX_PATH):
        print("Inverted index found. Skipping indexing.")
        return

    choice = input("No index found. Do you want to build it now? (y/n): ").strip().lower()
    if choice != 'y':
        print("Cannot proceed without an index. Exiting.")
        sys.exit(0)

    print("Starting search engine indexing...")

    documents, total_files_read = read_json_files()
    if len(documents) == 0:
        print("Error: No documents were found. Check your dataset path!")
        sys.exit(1)

    print(f"Processed {len(documents)} documents.")

    # Fix: Unpack 3 values instead of 2
    inverted_index, document_lookup, document_contents = build_inverted_index(documents)

    # Extract document graph for PageRank
    document_graph = {doc["url"]: [] for doc in documents}
    for doc in documents:
        if "links" in doc:
            document_graph[doc["url"]] = doc["links"]

    # Compute PageRank
    pagerank_scores = compute_pagerank(document_graph)
    # Save everything, including document_contents
    save_index(inverted_index, document_lookup, document_contents, pagerank_scores, total_files_read, INVERTED_INDEX_PATH)

    print("Indexing complete. Inverted index saved.")




def run_search():
    """Loads the inverted index and runs the search process."""
    inverted_index, doc_lookup, pagerank_scores, document_summaries, total_docs = load_inverted_index(INVERTED_INDEX_PATH)

    if inverted_index is None:
        print("Failed to load the index. Exiting.")
        sys.exit(1)

    while True:
        query = input("Enter your query (or type 'exit' to quit): ").strip()
        if query.lower() == 'exit':
            print("Exiting search.")
            break

        if not query:
            print("Error: Empty query provided.")
            continue

        # Run search
        top_results = search(query, inverted_index, doc_lookup, pagerank_scores, document_summaries, total_docs)

        print("\nTop 5 Results:")
        if not top_results:
            print("No relevant results found.")
        else:
            for doc_id, score, url, summary in top_results:
                print(f"\nDocID: {doc_id}, Score: {score:.4f}")
                print(f"URL: {url}")
                print(f"Summary: {summary}")  #Display pre-generated summary


def run_gui_search():
    """Launches a GUI-based search interface using Tkinter."""
    inverted_index, doc_lookup, pagerank_scores, document_summaries, total_docs = load_inverted_index(
        INVERTED_INDEX_PATH)

    if inverted_index is None:
        print("Failed to load the index. Exiting.")
        sys.exit(1)

    def perform_search():
        """Runs when the user clicks the Search button. Fetches results and displays them with timing."""
        query = query_entry.get().strip()
        if not query:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Please enter a search query.")
            return

        # Measure search execution time
        start_time = time.time()
        results = search(query, inverted_index, doc_lookup, pagerank_scores, document_summaries, total_docs)
        end_time = time.time()

        execution_time = (end_time - start_time) * 1000  # Convert seconds to milliseconds

        formatted_results = [
            f"DocID: {doc_id}\nScore: {score:.4f}\nURL: {url}\nSummary: {summary}\n\n"
            for doc_id, score, url, summary in results
        ]

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Search completed in {execution_time:.2f} ms\n\n")
        result_text.insert(tk.END, "\n".join(formatted_results) if formatted_results else "No relevant results found.")

    root = tk.Tk()
    root.title("Search Engine")
    root.geometry("600x400")

    tk.Label(root, text="Enter your query:", font=("Arial", 12)).pack(pady=5)
    query_entry = tk.Entry(root, width=50, font=("Arial", 12))
    query_entry.pack(pady=5)

    search_button = tk.Button(root, text="Search", command=perform_search, font=("Arial", 12), bg="lightblue")
    search_button.pack(pady=5)

    result_text = scrolledtext.ScrolledText(root, width=70, height=15, font=("Arial", 10))
    result_text.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    run_indexing()

    print("\nChoose your search method:")
    print("1 - Command Line Search")
    print("2 - GUI Search")

    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        run_search()
    elif choice == "2":
        run_gui_search()
    else:
        print("Invalid choice. Running command-line search by default.")
        run_search()
