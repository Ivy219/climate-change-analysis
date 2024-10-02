import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stop_words
from collections import Counter

# Load the dataset
df = pd.read_csv('twitter_sentiment_data.csv')

# Ensure the 'message' column exists
if 'message' not in df.columns:
    st.error("The CSV file must contain a 'message' column with the Twitter posts.")
    st.stop()

# Function to clean text and generate word frequencies
def calculate_word_frequencies(posts):
    tokens = []
    for post in posts:
        # Tokenize the text and remove stop words and punctuation
        cleaned_tokens = [word for word in post.lower().split() 
                          if word not in stop_words and word not in string.punctuation]
        tokens.extend(cleaned_tokens)  # Add cleaned tokens to the list
    word_freq = Counter(tokens)  # Count frequencies of each token
    return word_freq

# Generate word cloud
def generate_wordcloud(frequencies):
    wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(frequencies)
    return wc

# Calculate word frequencies from the 'message' column
word_freq = calculate_word_frequencies(df['message'])
wordcloud = generate_wordcloud(word_freq)

# Streamlit App
st.title("Semantic Analysis of Twitter Posts on Climate Change")
st.write("### Click on a word in the word cloud to see its context:")

# Display word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
st.pyplot(plt)

# Context display
selected_word = st.text_input("Enter a word to see its context:")
if selected_word:
    context_sentences = [post for post in df['message'] if selected_word in post.lower()]
    if context_sentences:
        st.write("#### Context Sentences:")
        for sentence in context_sentences:
            st.write(f"- {sentence}")
    else:
        st.write("No context found for this word.")