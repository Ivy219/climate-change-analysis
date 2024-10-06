#1. Test on library

#import dash
#from dash import dcc, html
#from dash.dependencies import Input, Output
#import plotly.express as px
#import pandas as pd

## Sample data
#df = pd.DataFrame({
    #"Fruit": ["Apples", "Oranges", "Bananas", "Berries"],
    #"Amount": [4, 2, 3, 5]
#})

## Create a Dash app
#app = dash.Dash(__name__)

## Layout for the dashboard
#app.layout = html.Div([
    #html.H1("Fruit Sales Dashboard"),
    #dcc.Graph(id='bar-graph'),
    #dcc.Dropdown(
        #id='dropdown',
        #options=[{'label': fruit, 'value': fruit} for fruit in df["Fruit"]],
        #value='Apples'
    #),
    #html.Div(id='output-container')
#])

## Callback to update the graph based on dropdown input
#@app.callback(
    #Output('bar-graph', 'figure'),
    #[Input('dropdown', 'value')]
#)
#def update_graph(selected_fruit):
    #filtered_df = df[df['Fruit'] == selected_fruit]
    #fig = px.bar(filtered_df, x='Fruit', y='Amount', title=f'Sales of {selected_fruit}')
    #return fig

## Run the app
#if __name__ == '__main__':
    #app.run_server(debug=True)



#2. Test wiz matplotlib 
#import matplotlib.pyplot as plt

## Data
#x = [1, 2, 3, 4, 5]
#y = [1, 4, 9, 16, 25]

## Create a simple line plot
#plt.plot(x, y)

## Add title and labels
#plt.title("Simple Line Plot")
#plt.xlabel("X axis")
#plt.ylabel("Y axis")

## Show the plot
#plt.show()

#3. Test wiz word cloud
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import base64
from io import BytesIO

# Sample data (replace with your actual word frequency data and documents)
documents = {
    "twitter_sentiment_data.csv"
}

# Example word frequencies (replace with actual word counts from your corpus)
word_frequencies = {
    'data': 10,
    'science': 8,
    'machine': 7,
    'learning': 6,
    'AI': 5,
    'Python': 5,
    'development': 4,
    # Add more words with their frequencies...
}

# Create a Pandas DataFrame from the word frequencies
df = pd.DataFrame(list(word_frequencies.items()), columns=['Word', 'Frequency'])
df = df.sort_values(by='Frequency', ascending=False).head(100)  # Get Top 100 words

# Function to create the word cloud
def generate_wordcloud():
    wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_frequencies)
    return wc

# Function to encode the word cloud image in base64 format
def wordcloud_image():
    wc = generate_wordcloud()
    image_stream = BytesIO()
    wc.to_image().save(image_stream, format='PNG')
    image_stream.seek(0)
    return base64.b64encode(image_stream.read()).decode()

# Create the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Interactive Word Cloud"),
    
    # Word cloud image
    html.Img(id='wordcloud', src='data:image/png;base64,{}'.format(wordcloud_image()), style={'width': '100%', 'height': 'auto'}),
    
    # Table to display words and frequencies
    html.H2("Word Frequency Table"),
    dcc.Graph(id='table-graph'),
    
    # Display article text on word click
    html.Div(id='article-text', style={'whiteSpace': 'pre-line', 'marginTop': '20px'})
])

# Callback for the word cloud hover effect
@app.callback(
    Output('table-graph', 'figure'),
    Input('wordcloud', 'src')
)
def update_table(_):
    # Plotly table of words and frequencies
    fig = px.bar(df, x='Word', y='Frequency', text='Frequency', hover_data={'Word': True, 'Frequency': True})
    fig.update_layout(title="Word Frequencies", xaxis_title="Word", yaxis_title="Frequency")
    return fig

# Callback for displaying the article text when clicking on a word
@app.callback(
    Output('article-text', 'children'),
    [Input('wordcloud', 'src')]
)
def display_article_text(_):
    # Example: Display text for a clicked word (you can extend this for actual article links)
    return "Clicking on the word will display the corresponding article text here."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
