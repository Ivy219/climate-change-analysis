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
        cleaned_tokens = [word for word in post.lower().split() 
                          if word not in stop_words and word not in string.punctuation]
        tokens.extend(cleaned_tokens)
    word_freq = Counter(tokens)
    return word_freq

# Function to filter posts by sentiment score
def filter_posts_by_sentiment(sentiment):
    filtered_posts = df[df['sentiment'] == sentiment]['message']
    return filtered_posts

# Function to highlight a word in text
def highlight_word_in_text(text, word):
    return text.replace(word, f"<span style='color:red'>{word}</span>")

# Generate word cloud
def generate_wordcloud(frequencies):
    wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(frequencies)
    return wc

# Calculate word frequencies from the 'message' column
word_freq = calculate_word_frequencies(df['message'])
wordcloud = generate_wordcloud(word_freq)

# Streamlit App
st.title("Semantic Analysis of Twitter Posts on Climate Change")

# Display word cloud
st.write("### Click on a word in the word cloud to see its context:")
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
st.pyplot(plt)

# Word Input
selected_word = st.text_input("Enter a word to see its context:")

# Display word frequency
if selected_word:
    word_frequency = word_freq.get(selected_word.lower(), 0)
    st.write(f"Word Frequency of '{selected_word}': {word_frequency}")

# Add filtering buttons for sentiments (-1, 0, 1, 2)
if selected_word:
    st.write("Filter posts by sentiment score:")
    col1, col2, col3, col4 = st.columns(4)
    if col1.button('-1'):
        filtered_posts = filter_posts_by_sentiment(-1)
        st.write("#### Filtered Posts with Sentiment -1:")
        for post in filtered_posts:
            st.write(f"- {highlight_word_in_text(post, selected_word)}", unsafe_allow_html=True)

    if col2.button('0'):
        filtered_posts = filter_posts_by_sentiment(0)
        st.write("#### Filtered Posts with Sentiment 0:")
        for post in filtered_posts:
            st.write(f"- {highlight_word_in_text(post, selected_word)}", unsafe_allow_html=True)

    if col3.button('1'):
        filtered_posts = filter_posts_by_sentiment(1)
        st.write("#### Filtered Posts with Sentiment 1:")
        for post in filtered_posts:
            st.write(f"- {highlight_word_in_text(post, selected_word)}", unsafe_allow_html=True)

    if col4.button('2'):
        filtered_posts = filter_posts_by_sentiment(2)
        st.write("#### Filtered Posts with Sentiment 2:")
        for post in filtered_posts:
            st.write(f"- {highlight_word_in_text(post, selected_word)}", unsafe_allow_html=True)

# Error message if buttons pressed without entering a word
else:
    st.write("Please enter a word to see the filtered results.")

# Context display
if selected_word:
    context_sentences = [post for post in df['message'] if selected_word.lower() in post.lower()]
    if context_sentences:
        st.write("#### Context Sentences:")
        for sentence in context_sentences:
            st.write(f"- {highlight_word_in_text(sentence, selected_word)}", unsafe_allow_html=True)
    else:
        st.write("No context found for this word.")
