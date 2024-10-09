import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stop_words
import re

# Cache dataset loading to avoid slow running of the app
@st.cache_data
def load_data():
    """Load twitter_sentiment_data and cache the result."""
    return pd.read_csv('twitter_sentiment_data.csv')


# Cache word frequency calculation to avoid slow running of the app
@st.cache_data 
def calculate_word_frequencies(posts):
    """filter out meaningless word with ENGLISH_STOP_WORD, url links start 
    with "https://" and topic word "climate change" and calculate word frequency
    """
    tokens = []
    climate_change_pattern = re.compile(r'\b#?climatechange\b', re.IGNORECASE)
    
    for post in posts:
        for word in post.lower().split():
            if word not in stop_words and word not in string.punctuation and \
               not word.startswith('https:') and \
               not climate_change_pattern.match(word):
                tokens.append(word)
                
    word_freq = {}
    for word in tokens:
        word_freq[word] = word_freq.get(word, 0) + 1
    return word_freq


# Cache word cloud generation to avoid slow running of the app
@st.cache_resource
def generate_wordcloud(word_freq):
    """Generate word cloud with word frequency and display the figure"""
    word_cloud = WordCloud(width=800, height=400, background_color="white", \
                           max_words=200).generate_from_frequencies(word_freq)
    
    fig, axes = plt.subplots(figsize=(10, 5))
    axes.imshow(word_cloud, interpolation='bilinear')
    axes.axis("off")
    st.pyplot(fig)
    
    return word_cloud


def prompt_user_keyword(raw_posts):
    """Prompts a keyword from the user and calculate the keyword frequency. 
    If no input, show error message"""
    keyword = st.text_input("Enter a word to see its context:")
    if keyword:
        keyword_freq = calculate_word_frequencies(raw_posts).get(keyword.lower(), 0)
        st.write(f"Word Frequency of '{keyword}': {keyword_freq}")
    else:
        st.write("Please enter a word to see the filtered results.")
    return keyword


def highlight_keyword_in_post(post, keyword):
    """highlight keyword entered by the user in red"""
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return pattern.sub(f"<span style='color:red'>{keyword}</span>", post)


def create_streamlit_app(keyword):
    """create streamlit app with two columns, the left one will be used to 
    display the full posts of the keyword prompted and the right coloumn will 
    show sentiment buttons and the filtered posts after the user clicks on the 
    buttons.The left coloum is displayed in a scrollable section for a better 
    user experience"""
    
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(f"### Full List of Posts Containing '{keyword}':")
        full_posts = df[df['message'].str.contains(keyword, case=False)]\
            ['message'].drop_duplicates()
        with st.expander(f"See all posts containing {keyword}"):
            for post in full_posts:
                st.markdown(f"{highlight_keyword_in_post(post, keyword)}", \
                            unsafe_allow_html=True)

    with col_right:
        st.write("#### Sentiment Segmentation:")
        st.markdown("""
        <p style='font-size: 12px'>**2 (News)**: \
        The tweet links to factual news about climate change<br>
        **1 (Pro)**: The tweet supports the belief of man-made climate change<br>
        **0 (Neutral)**: The tweet neither supports nor refutes the belief of \
        man-made climate change<br>
        **-1 (Anti)**: The tweet does not believe in man-made climate change</p>
        """, unsafe_allow_html=True)
        sentiment_segmentation_plot(keyword)
        set_buttons(keyword)


def sentiment_segmentation_plot(keyword):
    """Calculate proportions of the posts(containing the keyword) of each 
    sentiment segmentation and display with a horizontal clustered bar chart"""
    total_keyword_posts = len(df[df['message'].str.contains(keyword, case=False)])
    sentiment_filtered_counts = df[df['message'].str.contains(keyword, case=False)]\
        ['sentiment'].value_counts()
    sentiment_proportions = (sentiment_filtered_counts / total_keyword_posts) * 100
    
    sentiment_data = pd.DataFrame({
        'Sentiment': sentiment_proportions.index.astype(str),
        'Proportion': sentiment_proportions.values
    })


    st.markdown(f"### Sentiment Distribution for Posts Containing '{keyword}'")
    fig, axes = plt.subplots() 
    axes.barh(sentiment_data['Sentiment'], sentiment_data['Proportion'], \
              color=['red', 'orange', 'yellow', 'green'])
    axes.set_xlabel("Proportion of Posts (%)")
    axes.set_ylabel("Sentiment (-1: Anti, 0: Neutral, 1: Pro, 2: News)")
    axes.set_title(f"Sentiment Distribution of Posts Containing '{keyword}'")
    for index, value in enumerate(sentiment_data['Proportion']):
        axes.text(value, index, f"{value:.2f}%", va='center')
    st.pyplot(fig)


def filter_posts_by_sentiment(sentiment, keyword):
    """filter posts with the sentiment buttons the user clicked on if the user 
    wants to explore the sentiment segmentation of posts containing the keyword 
    he entered. Drop duplicate posts"""
    filtered_posts = df[(df['sentiment'] == sentiment) & (df['message'].\
                str.contains(keyword, case=False))]['message'].drop_duplicates()
    return filtered_posts


def set_buttons(keyword):
    """set 4 buttons for sentiment segmentation. users could click on the button 
    to filter posts(containing keyword entered) of corresponding sentiment score.
    the filtered post will be displayed below the buttons"""
    
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
        filtered_posts = filter_posts_by_sentiment\
            (st.session_state.sentiment, keyword)
        st.write(f"#### Filtered Posts for sentiment \
        \{st.session_state.sentiment}:")
        for post in filtered_posts:
            st.markdown(f"{highlight_keyword_in_post(post, keyword)}", \
                        unsafe_allow_html=True)


def main():
    """Main function to display the wordcloud and deal with user 
    interaction with streamlit App"""
    raw_posts = df['message']
    word_freq = calculate_word_frequencies(raw_posts)

    if word_freq:
        st.title("Word Dashboard of Twitter Posts on Climate Change")
        total_word_count = sum(word_freq.values())
        st.markdown(f"### Total Word Count: {total_word_count}")
        st.markdown("<p style='font-size: 14px'>(Topic word 'climate change' \
        removed to display more informative vocabularies)</p>", unsafe_allow_html=True)
        
        word_cloud = generate_wordcloud(word_freq)
        keyword = prompt_user_keyword(raw_posts)
        if keyword:
            create_streamlit_app(keyword)


df = load_data()
main()
