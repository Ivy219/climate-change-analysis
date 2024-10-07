import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stop_words
from collections import Counter

# Load the dataset
df = pd.read_csv('twitter_sentiment_data.csv')

# Function to clean text and generate word frequencies
def calculate_word_frequencies(posts):
    tokens = []
    for post in posts:
        cleaned_tokens = [word for word in post.lower().split() 
                          if word not in stop_words and word not in string.punctuation and word != "climate" and word != "change"]
        tokens.extend(cleaned_tokens)
    word_freq = Counter(tokens)
    return word_freq

# Function to filter posts by sentiment and word
def filter_posts_by_sentiment(sentiment, selected_word):
    filtered_posts = df[(df['sentiment'] == sentiment) & (df['message'].str.contains(selected_word, case=False))]['message'].drop_duplicates()
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

# Check if word_freq is not empty
if word_freq:
    wordcloud = generate_wordcloud(word_freq)

    # Streamlit App
    st.title("Word Dashboard of Twitter Posts on Climate Change")

    # Display word cloud
    st.write("### Total Word Count (Topic word 'climate change' removed to display more informative vocabularies):")
    total_word_count = sum(word_freq.values())
    st.write(f"Total valid token count: {total_word_count}")
    
    # Create figure for the word cloud
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

# Word Input
selected_word = st.text_input("Enter a word to see its context:")

# Display word frequency and original posts
if selected_word:
    word_frequency = word_freq.get(selected_word.lower(), 0)
    st.write(f"Word Frequency of '{selected_word}': {word_frequency}")

    # Add filtering buttons for sentiments (-1, 0, 1, 2) just beneath the word count
    st.write("Filter posts by sentiment score:")
    col1, col2, col3, col4 = st.columns(4)
    
    # Show original posts where the word is derived from (within a scrollable area)
    all_posts = df[df['message'].str.contains(selected_word, case=False)]['message'].drop_duplicates()
    
    # Check if a sentiment button has been clicked
    filtered_posts = None
    if col1.button('-1'):
        filtered_posts = filter_posts_by_sentiment(-1, selected_word)
    elif col2.button('0'):
        filtered_posts = filter_posts_by_sentiment(0, selected_word)
    elif col3.button('1'):
        filtered_posts = filter_posts_by_sentiment(1, selected_word)
    elif col4.button('2'):
        filtered_posts = filter_posts_by_sentiment(2, selected_word)
    
    # If a sentiment button was clicked, display filtered posts
    if filtered_posts is not None:
        st.write(f"#### Filtered Posts with Sentiment:")
        for post in filtered_posts:
            st.write(f"- {highlight_word_in_text(post, selected_word)}", unsafe_allow_html=True)
    else:
        # If no sentiment button clicked, display all posts in a scrollable section
        with st.expander("See all posts containing the word"):
            for post in all_posts:
                st.write(f"- {highlight_word_in_text(post, selected_word)}", unsafe_allow_html=True)

# Error message if buttons pressed without entering a word
else:
    st.write("Please enter a word to see the filtered results.")

# Add annotations for sentiment buttons
st.write("#### Sentiment Analysis Categories:")
st.markdown("""
**2 (News)**: The tweet links to factual news about climate change  
**1 (Pro)**: The tweet supports the belief of man-made climate change  
**0 (Neutral)**: The tweet neither supports nor refutes the belief of man-made climate change  
**-1 (Anti)**: The tweet does not believe in man-made climate change  
""")
