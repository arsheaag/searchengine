from transformers import pipeline

# Load a small, fast summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(text):
    """Summarizes text into two concise sentences."""
    try:
        summary = summarizer(text, max_length=50, min_length=20, do_sample=False)
        summarized_text = summary[0]['summary_text']
        
        # Ensure only 2 sentences are returned
        sentences = summarized_text.split(". ")  # Split into sentences
        if len(sentences) > 2:
            return ". ".join(sentences[:2]) + "."  # Return only first 2 sentences
        
        return summarized_text  # If already short, return full summary

    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Summary unavailable."
