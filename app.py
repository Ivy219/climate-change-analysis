"""COSC480 Program: Semantic Analysis APP for Twitter Posts on Climate Change 
Author: Ivy
Date: 09/10/2024
"""
# import streamlit library to produce a web app for the whole data visualization 
# and interactive function
import streamlit as st
# import pandas library to deal with both string (posts) and 
# numeric data (proportion of sentiment scores)
import pandas as pd
# import worldcould library for generating wordcloud
from wordcloud import WordCloud
# import matplotlib library to produce bar chart
import matplotlib.pyplot as plt
# import string function to remove punctuation in dataset. 
# GitHub has no built-in string function so need to import in the code
import string
# import scikit-learn library to clean dataset with ENGLISH_STOP_WORDS
# (i.e. words like "i", "was", "has", "before")
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stop_words
# import re module to cope with string pattern so that the keyword entered by
# the user could be highlighted in the post. But failed to fullfill due to the 
# conclict with streamlit markdown
# import re


#Part I Create a word cloud based on word frequency of the whole dataset 
#Step 1: Load the data of twitter posts on climate change

# cache the result to avoid program lag, which happened during testing
@st.cache_data 
def load_data():
    """Load twitter_sentiment_data with pandas library"""
    return pd.read_csv('twitter_sentiment_data.csv')


#Step 2: Clean data and calculate word frequency in preparation of the word cloud.
# Since the word cloud is generated according to word frequency, meaningless word
# and message the audience has already known (i.e. "climate change") will affect
# information quality, so need to remove them.
@st.cache_data 
def calculate_word_frequencies(posts):
    """Filter out meaningless words with ENGLISH_STOP_WORD and default string 
    function of punctuation, URL links start with "https://" and topic word 
    "climate change" and calculate word frequency. 
    """
    tokens = []
    for post in posts:
        # Don't care if it's upper or lower cases so make all the words lower case
        for word in post.lower().split():
            if word not in stop_words and word not in string.punctuation and \
               word != "climate" and word != "change" and \
               not word.startswith('https:'):
                tokens.append(word)
                
    word_freq = {}
    for word in tokens:
        word_freq[word] = word_freq.get(word, 0) + 1
    return word_freq


#Step 3: Generate word cloud for the whole dataset
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


#Part II Interactive funtion supporting user to explore each word displayed in 
# the word cloud with detailed information: word frequency of the keyword, sentiment
# distribution chart of posts containing the keyword, original posts under 
# each sentiment segmentation.

# Step 1: Ask user to prompt a keyword for exploration
def prompt_user_keyword(raw_posts):
    """Prompts a keyword from the user and calculate the keyword frequency to 
    display. If no input, show error message."""
    keyword = st.text_input("Enter a word to see its context:")
    if keyword:
        keyword_freq = calculate_word_frequencies(raw_posts).get(keyword.lower(), 0)
        st.markdown(f"""Word Frequency of <span style='color: red; \
        font-size:16px; font-style:italic;'>'{keyword}'</span>: <span 
        style='color: blue; font-size:16px; font-style:italic;'>{keyword_freq:,}
        """, unsafe_allow_html=True)        
    else:
        st.write("Please enter a word to see sentiment results.")
    return keyword


# Step 2: Create bar chart to showcase the sentiment distribution of 
# posts containing the keyword
def sentiment_segmentation_plot(keyword):
    """Calculate proportions of the posts(containing the keyword) of each 
    sentiment segmentation and display with a horizontal clustered bar chart."""
    
    # find the posts(i.e. the 'message'column of the csv file) containing 
    # keyword and count the total number
    total_keyword_posts = len(df[df['message'].str.contains(keyword, case=False)])
    
    # after fitler out posts containing keyword, select 'sentiment' column in
    # in the csv file and count the occurrence of each unique value of the 
    # sentiment score
    sentiment_filtered_counts = df[df['message'].str.contains(keyword, case=False)]\
        ['sentiment'].value_counts()
    
    sentiment_proportions = (sentiment_filtered_counts / total_keyword_posts) * 100
    
    # set a data frame to draw the plot, x= sentiment proportion, 
    # y=4 sentiment score as label
    sentiment_data = pd.DataFrame({
        # The sentiment score here acts as label so treat it as string
        'Sentiment': sentiment_proportions.index.astype(str),
        'Proportion': sentiment_proportions.values
    })
    
    # plot the bar chart
    st.markdown(f"<h3>Sentiment Distribution for Posts Containing\
    <span style='color: red; font-style:italic;'>'{keyword}'</span></h3>", \
                unsafe_allow_html=True)  
    fig, axes = plt.subplots() 
    axes.barh(sentiment_data['Sentiment'], sentiment_data['Proportion'], \
              color=['red', 'orange', 'yellow', 'green'])
    axes.set_xlabel("Proportion of Posts (%)")
    axes.set_ylabel("Sentiment (-1: Anti, 0: Neutral, 1: Pro, 2: News)")
    axes.set_title(f"Sentiment Distribution of Posts Containing '{keyword}'")
    for index, value in enumerate(sentiment_data['Proportion']):
        axes.text(value, index, f"{value:.2f}%", va='center')
    st.pyplot(fig)


# Step 3: Prepare filtered posts of each sentiment score
def filter_posts_by_sentiment(sentiment, keyword):
    """Prepare filtered posts of each sentiment segmentation. The posts contains 
    the keyword entered by the user. Drop duplicate posts."""
    filtered_posts = df[(df['sentiment'] == sentiment) & (\
        df['message'].str.contains(keyword, case=False))]['message'].drop_duplicates()
    return filtered_posts


# Step 4: Set 4 buttons corresponding to the 4 sentiment score and display filtered
# posts accordingly
def set_buttons(keyword):
    """Set 4 buttons for sentiment segmentation. Users could click on the button 
    to filter posts(containing keyword entered) of corresponding sentiment score.
    The filtered post will be displayed below the buttons."""
    
    st.write("#### Filter posts by sentiment score:")
    # display the buttons side by side
    col1, col2, col3, col4 = st.columns(4)
    
    # initialize button status to None to ensure the existence of unclicked buttons
    # (during the test, the rest buttons disappeared after one was clicked)
    if 'click' not in st.session_state:
        st.session_state.sentiment = None

    if col1.button('-1'):
        st.session_state.click = -1
    if col2.button('0'):
        st.session_state.click = 0
    if col3.button('1'):
        st.session_state.click = 1
    if col4.button('2'):
        st.session_state.click = 2

    if st.session_state.click is not None:
        filtered_posts = filter_posts_by_sentiment(st.session_state.click, keyword)
        scrollable_filtered_posts = "\n\n".join(filtered_posts)
        
        # display the filtered posts in a text area, if the content height 
        # exceeds 400, the text area is scrollable
        st.text_area(f"Filtered Posts for Sentiment {st.session_state.click}",\
                    scrollable_filtered_posts, height=400, key='filtered_posts')


# Step 5: Display all the information about the keyword by streamlit App
def create_streamlit_app(keyword):
    """Create Streamlit app with two sections: the left one for all the posts 
    containing the keyword and the right one for sentiment buttons with 
    filtered posts."""
    
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(f"<h3>Full List of Posts Containing <span style='color: red; \
        font-style:italic;'>'{keyword}'</span></h3>", unsafe_allow_html=True)
        # find the posts containing keyword, drop duplicate posts
        full_posts = df[df['message'].str.contains(keyword, case=False)]\
            ['message'].drop_duplicates()
        
        # display the full posts in a text area, if the content height 
        # exceeds 400, the text area is scrollable        
        scrollable_full_posts = "\n\n".join(full_posts)
        st.text_area(f"", scrollable_full_posts, height=400, key='full_posts')

    with col_right:
        st.write("#### Sentiment Segmentation:")
        # Explain the meaning of each sentiment score
        st.markdown("""<p style='font-size: 12px;'>
        <strong>*2 (News):</strong> \
        The tweet links to factual news about climate change<br>
        <strong>*1 (Pro):</strong> \
        The tweet supports the belief of man-made climate change<br>
        <strong>*0 (Neutral):</strong> \
        The tweet neither supports nor refutes the belief of man-made climate change<br>
        <strong>*-1 (Anti):\</strong> \
        The tweet does not believe in man-made climate change
        </p>
        """, unsafe_allow_html=True)
        # display functions in Step 2-4
        sentiment_segmentation_plot(keyword)
        set_buttons(keyword)
        
        
def main():
    """Main function to display the wordcloud and deal with user 
    interaction with Streamlit App."""
    # select raw posts from the 'message' column of the csv file
    raw_posts = df['message']
    # clean data and calculate word frequency with funtion in Part I -Step 2
    word_freq = calculate_word_frequencies(raw_posts)

    if word_freq:
        st.title("Semantic Analysis APP for Twitter Posts on Climate Change")
        
        # Count total word amount after data is cleaned
        total_word_count = sum(word_freq.values())
        
        st.markdown(f"""<h3>Total Word Count: <span style='color: red; \
        font-size:24px; font-style:italic;'>{total_word_count:,}</span></h3>
        """, unsafe_allow_html=True)
        st.markdown("<p style='font-size: 14px'>(Topic word 'climate change' \
        removed to display more informative vocabularies)</p>", unsafe_allow_html=True)
        
        # Generate wordcloud with function in Part I - Step 3
        word_cloud = generate_wordcloud(word_freq)
        # Get user prompt and display keyword count with function in Part II - Step 1
        keyword = prompt_user_keyword(raw_posts)
        if keyword:
            # If keyword is not empty, then deploy all the functions in Part II
            # - Step 2-5
            create_streamlit_app(keyword)


# load data in global view for all functions above to avoid program lag 
# (lagging happens during testings due to duplicate calls from one function to another)
df = load_data()
# call main functions
main()


# Failed function:
# Designed to highlight user keyword in red. But conflict with the streamlit
# mardown function such that html code <span style='color:red'>{keyword}</span>
# was displayed directly in the post instead of turning keyword into red.
#def highlight_keyword_in_post(post, keyword):
    #"""Highlight keyword entered by the user in red. """
    #pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    #return pattern.sub(f"<span style='color:red'>{keyword}</span>", post)

