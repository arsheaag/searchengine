# Run queries and measure performance
import time
from search import search

test_queries = [
    "cristina lopes",
    "machine learning",
    "ACM",
    "master of software engineering",
    "computer science faculty",
    "graduate admissions",
    "artificial intelligence research",
    "undergraduate internships",
    "data science",
    "software engineering program",
    "new student housing availability",
    "research lab openings 2024",
    "UCI campus parking regulations",
    "upcoming ICS networking events",
    "online graduate programs ICS",
    "scholarships for international students",
    "faculty sabbatical leave policies",
    "remote software engineering jobs",
    "latest cybersecurity workshops",
    "alumni career outcomes 2024"
]

for query in test_queries:
    start_time = time.time()
    results = search(query)
    elapsed_time = time.time() - start_time
    print(f"Query: '{query}' | Time: {elapsed_time:.4f}s | Results: {len(results)}")