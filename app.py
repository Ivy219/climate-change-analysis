import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stop_words
from collections import Counter
import re

# Load dataset
df = pd.read_csv('twitter_sentiment_data.csv')

# Function to calculate word frequencies
def calculate_word_frequencies(posts):
    tokens = []
    for post in posts:
        for word in post.lower().split():
            if word not in stop_words and word not in string.punctuation and \
               word != "climate" and word != "change" and \
               not word.startswith('https:'):
                tokens.append(word)
    word_freq = {}
    for word in tokens:
        word_freq[word] = word_freq.get(word, 0) + 1
    return word_freq

# Generate WordCloud
def generate_wordcloud(word_freq):
    word_cloud = WordCloud(width=1000, height=500, background_color="white").generate_from_frequencies(word_freq)
    
    fig, axes = plt.subplots(figsize=(10, 5))  # Changed 'ax' to 'axes'
    axes.imshow(word_cloud, interpolation='bilinear')
    axes.axis("off")
    st.pyplot(fig)

# Prompt for keyword input
def prompt_user_keyword(raw_posts):
    keyword = st.text_input("Enter a word to see its context:")
    if keyword:
        keyword_freq = calculate_word_frequencies(raw_posts).get(keyword.lower(), 0)
        st.write(f"Word Frequency of '{keyword}': {keyword_freq}")
    else:
        st.write("Please enter a word to see the filtered results.")
    return keyword

# Highlight keyword in posts
def highlight_keyword_in_post(post, keyword):
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return pattern.sub(f"<span style='color:red'>{keyword}</span>", post)

# Create the Streamlit app layout
def create_streamlit_app(keyword):
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(f"### Full List of Posts Containing '{keyword}':")
        full_posts = df[df['message'].str.contains(keyword, case=False)]['message'].drop_duplicates()
        with st.expander(f"See all posts containing {keyword}"):
            for post in full_posts:
                st.markdown(f"{highlight_keyword_in_post(post, keyword)}", unsafe_allow_html=True)

    with col_right:
        st.write("#### Sentiment Segmentation:")
        st.markdown("""
        <p style='font-size: 12px'>**2 (News)**: The tweet links to factual news about climate change<br>
        **1 (Pro)**: The tweet supports the belief of man-made climate change<br>
        **0 (Neutral)**: The tweet neither supports nor refutes the belief of man-made climate change<br>
        **-1 (Anti)**: The tweet does not believe in man-made climate change</p>
        """, unsafe_allow_html=True)
        sentiment_segmentation_plot(keyword)
        set_buttons(keyword)

# Sentiment distribution plot
def sentiment_segmentation_plot(keyword):
    total_keyword_posts = len(df[df['message'].str.contains(keyword, case=False)])
    sentiment_filtered_counts = df[df['message'].str.contains(keyword, case=False)]['sentiment'].value_counts()
    sentiment_proportions = (sentiment_filtered_counts / total_keyword_posts) * 100

    sentiment_data = pd.DataFrame({
        'Sentiment': sentiment_proportions.index.astype(str),
        'Proportion': sentiment_proportions.values
    })

    st.markdown(f"### Sentiment Distribution for Posts Containing '{keyword}'")
    fig, axes = plt.subplots()  # Define 'axes' here
    axes.barh(sentiment_data['Sentiment'], sentiment_data['Proportion'], color=['red', 'orange', 'yellow', 'green'])
    axes.set_xlabel("Proportion of Posts (%)")
    axes.set_ylabel("Sentiment (-1: Anti, 0: Neutral, 1: Pro, 2: News)")
    axes.set_title(f"Sentiment Distribution of Posts Containing '{keyword}'")
    for index, value in enumerate(sentiment_data['Proportion']):
        axes.text(value, index, f"{value:.2f}%", va='center')
    st.pyplot(fig)

# Filter posts by sentiment score
def filter_posts_by_sentiment(sentiment, keyword):
    filtered_posts = df[(df['sentiment'] == sentiment) & (df['message'].str.contains(keyword, case=False))]['message'].drop_duplicates()
    return filtered_posts

# Set sentiment buttons
def set_buttons(keyword):
    st.write("#### Filter posts by sentiment score:")
    col1, col2, col3, col4 = st.columns(4)

    if 'sentiment' not in st.session_state:
        st.session_state.sentiment = None

    if col1.button('-1'):
        st.session_state.sentiment = -1
    if col2.button('0'):
        st.session_state.sentiment = 0
    if col3.button('1'):
        st.session_state.sentiment = 1
    if col4.button('2'):
        st.session_state.sentiment = 2

    if st.session_state.sentiment is not None:
        filtered_posts = filter_posts_by_sentiment(st.session_state.sentiment, keyword)
        st.write(f"#### Filtered Posts for sentiment {st.session_state.sentiment}:")
        for post in filtered_posts:
            st.markdown(f"{highlight_keyword_in_post(post, keyword)}", unsafe_allow_html=True)

# Main WordCloud display function
def main_display_wordcloud():
    raw_posts = df['message']
    word_freq = calculate_word_frequencies(raw_posts)
    generate_wordcloud(word_freq)
    if word_freq:
        st.title("Word Dashboard of Twitter Posts on Climate Change")
        total_word_count = sum(word_freq.values())
        st.markdown(f"### Total Word Count: {total_word_count}")
        st.markdown("<p style='font-size: 14px'>(Topic word 'climate change' \
        removed to display more informative vocabularies)</p>", unsafe_allow_html=True)
    
    keyword = prompt_user_keyword(raw_posts)
    create_streamlit_app(keyword)

# Run the app
main_display_wordcloud()
