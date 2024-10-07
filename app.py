import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string
import seaborn as sns
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stop_words
from collections import Counter
import re

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

# Function to highlight a word in text (case-insensitive)
def highlight_word_in_text(text, word):
    pattern = re.compile(re.escape(word), re.IGNORECASE)  # Case-insensitive matching
    return pattern.sub(f"<span style='color:red'>{word}</span>", text)

# Generate word cloud
def generate_wordcloud(frequencies):
    wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(frequencies)
    return wc

# Set up session state to track which button was pressed
if 'sentiment' not in st.session_state:
    st.session_state.sentiment = None

# Calculate word frequencies from the 'message' column
word_freq = calculate_word_frequencies(df['message'])

# Check if word_freq is not empty
if word_freq:
    wordcloud = generate_wordcloud(word_freq)

    # Streamlit App
    st.title("Word Dashboard of Twitter Posts on Climate Change")

    # Display total word count
    total_word_count = sum(word_freq.values())
    st.markdown(f"### Total Word Count: {total_word_count}")
    st.markdown("<p style='font-size: 12px'>(Topic word 'climate change' removed to display more informative vocabularies)</p>", unsafe_allow_html=True)
    
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

    # Create two columns: Left for the full list, Right for sentiment buttons and filtered list
    col_left, col_right = st.columns([2, 1])

    # Left side: Full list of posts (scrollable section)
    with col_left:
        st.write("### Full List of Posts Containing the Word:")
        all_posts = df[df['message'].str.contains(selected_word, case=False)]['message'].drop_duplicates()
        with st.expander("See all posts containing the word"):
            for post in all_posts:
                st.write(f"- {highlight_word_in_text(post, selected_word)}", unsafe_allow_html=True)

    # Right side: Sentiment buttons and filtered posts
    with col_right:
        # Annotations for sentiment buttons
        st.write("#### Sentiment Analysis Categories:")
        st.markdown("""
        <p style='font-size: 12px'>**2 (News)**: The tweet links to factual news about climate change  
        **1 (Pro)**: The tweet supports the belief of man-made climate change  
        **0 (Neutral)**: The tweet neither supports nor refutes the belief of man-made climate change  
        **-1 (Anti)**: The tweet does not believe in man-made climate change</p>
        """, unsafe_allow_html=True)

        # Calculate sentiment proportions for the word
        total_posts = len(df[df['message'].str.contains(selected_word, case=False)])
        sentiment_counts = df[df['message'].str.contains(selected_word, case=False)]['sentiment'].value_counts()

        # Calculate proportions as percentages
        sentiment_proportions = (sentiment_counts / total_posts) * 100  # Convert to percentage

        # Prepare data for plotting
        sentiment_data = pd.DataFrame({
            'Sentiment': sentiment_proportions.index.astype(str),  # Ensure Sentiment is treated as a string
            'Proportion': sentiment_proportions.values
        })

        # Display Clustered bar chart for sentiment distribution
        st.write("### Sentiment Distribution for Posts Containing the Word")
        fig, ax = plt.subplots()
        sns.barplot(x='Proportion', y='Sentiment', data=sentiment_data, palette='coolwarm', ax=ax)
        ax.set_xlabel("Proportion of Posts (%)")
        ax.set_ylabel("Sentiment (-1: Anti, 0: Neutral, 1: Pro, 2: News)")
        ax.set_xticklabels(ax.get_xticks(), rotation=45)  # Rotate x labels for better visibility
        st.pyplot(fig)

        # Sentiment buttons
        st.write("#### Filter posts by sentiment score:")
        col1, col2, col3, col4 = st.columns(4)

        # Check which sentiment button was pressed and update session state
        if col1.button('-1'):
            st.session_state.sentiment = -1
        if col2.button('0'):
            st.session_state.sentiment = 0
        if col3.button('1'):
            st.session_state.sentiment = 1
        if col4.button('2'):
            st.session_state.sentiment = 2

        # Display filtered posts below the buttons based on session state
        if st.session_state.sentiment is not None:
            filtered_posts = filter_posts_by_sentiment(st.session_state.sentiment, selected_word)
            st.write(f"#### Filtered Posts for sentiment {st.session_state.sentiment}:")
            for post in filtered_posts:
                st.write(f"- {highlight_word_in_text(post, selected_word)}", unsafe_allow_html=True)

# Error message if buttons pressed without entering a word
else:
    st.write("Please enter a word to see the filtered results.")
