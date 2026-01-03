from summarizer import generate_summary

# Sample long text to summarize
test_text = """
Artificial intelligence (AI) is a branch of computer science that aims to create intelligent machines 
that can perform tasks that typically require human intelligence. AI systems use various techniques, 
including machine learning, deep learning, and natural language processing, to analyze data, recognize 
patterns, and make decisions. AI has applications in numerous fields such as healthcare, finance, 
automotive, and entertainment. Modern AI models like OpenAI’s ChatGPT and Google’s Gemini can generate 
human-like text, assist with coding, and answer complex queries. AI continues to evolve, transforming 
industries and society at a rapid pace.
"""

# Run the summarizer
summary = generate_summary(test_text)

# Print the generated summary
print("\n Original Text:\n", test_text)
print("\n AI-Generated Summary:\n", summary)
