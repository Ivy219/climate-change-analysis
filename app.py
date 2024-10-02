import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# Load the dataset (replace with your actual file path if needed)
df = pd.read_csv('twitter_sentiment_data.csv')

# Ensure that the 'text' column exists
if 'message' not in df.columns:
    st.error("Missing data")
    st.stop()

# Tokenize and calculate word frequencies
def calculate_word_frequencies(posts):
    tokens = []
    for post in posts:
        tokens.extend(post.lower().split())  
    word_freq = Counter(tokens)
    return word_freq

# Generate word cloud
def generate_wordcloud(frequencies):
    wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(frequencies)
    return wc

# Prepare data (using the 'text' column from your dataset)
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
        st.write("#### Original Twitter Post:")
        for sentence in context_sentences:
            st.write(f"- {sentence}")
    else:
        st.write("No post found for this word.")
