import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stop_words
from collections import Counter
import re


df = pd.read_csv('twitter_sentiment_data.csv')

#1. Rewritten
#def calculate_word_frequencies(posts):
    #tokens = []
    #for post in posts:
        #for word in post.lower().split():
            #if word not in stop_words and word not in string.punctuation and \
               #word != "climate" and word != "change" and \
               #not word.startswith('https://'):
                #tokens.append(word)
    #word_freq = {}
    #for word in tokens:
        #word_freq[word] = word_freq.get(word, 0) + 1
    #return word_freq   

#print(calculate_word_frequencies(df['message']))

#2. Not solved yet
#def sentiment_posts_with_keyword(sentiment, user_word):
    #filtered_posts = []
    #no_duplicate_posts = df['message'].drop_duplicates()
    #for post in no_duplicate_posts:
        #if user_word in post:
            #filtered_posts. append(df[df['sentiment'] == sentiment])
    ##if df['sentiment'] == sentiment) and df['message'].str.contains(user_word, case=False):
        ##filtered_posts = df[(df['sentiment'] == sentiment) & (df['message'].str.contains(user_word, case=False))]['message'].drop_duplicates()
    #return filtered_posts

#print (sentiment_posts_with_keyword('1', 'trump'))
#print (df['message'].drop_duplicates())

#test = pd.DataFrame({
    #'sentiment': [1, 0, -1, 2, 1],
    #'message': ['Climate change is real', 'I don\'t care', 'Climate change is a hoax', 'News about climate change', 'Real impact of climate change']
#})

#print(test[(test['sentiment']== -1)])
#   sentiment                   message
#2         -1  Climate change is a hoax
#no_duplicate_posts = df['message'].drop_duplicates()
#print(sentiment_posts_with_keyword('-1', 'trump'))

#3. Function to highlight a word in text (case-insensitive)
#def highlight_word_in_text(text, word):
    #pattern = re.compile(re.escape(word), re.IGNORECASE)  # Case-insensitive matching
    #return pattern.sub(f"<span style='color:red'>{word}</span>", text)


#pattern = re.compile(re.escape('%'))
#result = pattern.findall('a%b shighoerrioa&$%nshiji is a pattern')
#print(result) 

#4 Funtion to generate the wordcloud
#def generate_wordcloud(word_freq):
    #"""Generate word cloud with word frequency
    #"""
    #word_cloud = WordCloud(width=1000, height=500, background_color="white").generate_from_frequencies(word_freq)
    #return word_cloud


#import matplotlib.pyplot as plt
#from wordcloud import WordCloud
#import matplotlib
##print(matplotlib.rcsetup.all_backends)

#matplotlib.use('TkAgg')
## Sample word frequencies
#word_frequencies = {'climate': 50, 'change': 40, 'earth': 20, 'asf': 30, 'teste': 100}

## Function to generate word cloud
#def generate_wordcloud(frequencies):
    #wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(frequencies)
    #return wc

## Generate the word cloud
#wordcloud = generate_wordcloud(word_frequencies)

## Display the word cloud using matplotlib
#plt.figure(figsize=(10, 5))
#plt.imshow(wordcloud, interpolation='bicubic')
#plt.axis("off")
#plt.show()


#5.
import streamlit as st

# Check if 'click_count' exists in session_state, if not, initialize it to 0
if 'click_count' not in st.session_state:
    st.session_state.click_count = 0

# Create a button that increments the click count
if st.button('Click Me!'):
    st.session_state.click_count += 1

# Display the number of times the button has been clicked
st.write(f"Button clicked {st.session_state.click_count} times")