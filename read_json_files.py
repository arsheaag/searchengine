import os
import json
from extract_text import extract_text_from_html
from tokenizer import tokenize

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(BASE_DIR, "data", "developer", "DEV")
OUTPUT_FILE = os.path.join(BASE_DIR, "processed_documents.json")


def read_json_files():
    document_list = []
    file_count = 0
    skipped_count = 0  # Counter for skipped documents
    total_json_files = 0  # Counter for total files read

    for folder_name, subfolder_names, file_names in os.walk(DATA_FOLDER):
        for file in file_names:
            if file.endswith(".json"):
                file_path = os.path.join(folder_name, file)
                total_json_files += 1  # Count every file

                with open(file_path, "r", encoding="utf-8") as json_file:
                    try:
                        data = json.load(json_file)
                        url = data.get("url", "No URL Found")
                        content = data.get("content", "No Content Found")

                        try:
                            processed_text = extract_text_from_html(content)
                        except Exception as e:
                            print(f"ERROR: Failed to process HTML for {url}: {str(e)}")
                            continue

                        regular_tokens = tokenize(processed_text["regular"])
                        important_tokens = tokenize(processed_text["important"])

                        if not regular_tokens and not important_tokens:
                            print(f"Skipping empty document: {url}")
                            skipped_count += 1
                            continue  # Skip this document

                        document_list.append({
                            "url": url,
                            "regular_tokens": regular_tokens,
                            "important_tokens": important_tokens
                        })
                        file_count += 1

                        if file_count % 100 == 0:
                            print(f"Processed {file_count} files...")

                        if file_count % 1000 == 0:
                            with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                                json.dump(document_list, f)
                                f.write("\n")
                            #document_list = []  # Clear memory

                    except json.JSONDecodeError:
                        print(f"Skipped invalid JSON file: {file_path}")

    if document_list:
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            json.dump(document_list, f, indent=4)
#            f.write("\n")

    # Print the final statistics
    print(f"\nTotal JSON files read: {total_json_files}")
    print(f"Skipped empty documents: {skipped_count}")
    print(f"Final total documents sent for indexing: {file_count}\n")

    print(f"Final check before returning: {len(document_list)} documents being returned.")  # Debugging line

    return document_list, total_json_files