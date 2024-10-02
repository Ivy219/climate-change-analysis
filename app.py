import nltk
nltk.data.path.append('./nltk_data')
import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64
from collections import Counter

# Sample dataset: semantic Twitter posts on climate change
data = {
    'posts': [
        "Climate change is real and happening now.",
        "We must take action against climate change.",
        "The effects of global warming are evident.",
        "Climate change denial is dangerous.",
        "Renewable energy is key to fighting climate change."
    ]
}

# Tokenize and calculate word frequencies
def calculate_word_frequencies(posts):
    tokens = []
    for post in posts:
        tokens.extend(nltk.word_tokenize(post.lower()))
    word_freq = Counter(tokens)
    return word_freq

# Generate word cloud
def generate_wordcloud(frequencies):
    wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(frequencies)
    return wc

# Prepare data
df = pd.DataFrame(data)
word_freq = calculate_word_frequencies(df['posts'])
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
    context_sentences = [post for post in data['posts'] if selected_word in post.lower()]
    if context_sentences:
        st.write("#### Context Sentences:")
        for sentence in context_sentences:
            st.write(f"- {sentence}")
    else:
        st.write("No context found for this word.")
        
