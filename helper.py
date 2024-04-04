from urlextract import URLExtract
from PIL import Image
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from collections import Counter

import emoji as em 


import re

from collections import Counter


f= open('stop_hinglish.txt','r')
stopwords= f.read()
        

def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df = df[df['User'] == selected_user]


    # fetching num of message-------------------------------------------!   
    num_message = df.shape[0]

    # fetching num of words---------------------------------------------!
    word_len = []
    for msg in df['Message_']:
        word_len.extend(msg.split(' '))

    # fetching number of media---------------------------------------------!
    
    num_media_msg = df[df['Message_'] == "<Media omitted>\n"].shape[0]

    # fetching number of links in messages-----------------------------!

    extract = URLExtract()
    num_links = []
    for i in df['Message_']:
        num_links.extend(extract.find_urls(i))
    
    return num_message, len(word_len), num_media_msg, len(num_links)






def most_busy_users(df):
    # this code is for bar chart------------------------!
    temp = df[df['User'] !='Notification']

    x = temp['User'].value_counts().head()
    x.reset_index().rename(columns = {'index':'Users', 'User':'Value'})

    # this code is for percentage dataframe
    percentage_df = round(temp['User'].value_counts()/df.shape[0]*100, 2).reset_index().rename(columns = {'User': 'User Name', 'count':'Percentage'})
    
    
    return x, percentage_df


def create_wordcloud(selected_user, df):

    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    temp = df[df['Message_'] != "<Media omitted>\n"]
    temp = temp[temp['Message_'] != "Notification"]
    temp = temp[temp['Message_'] != "Missed voice call\n"]
    temp = temp[temp['Message_'] != "You deleted this message\n"]
     
     # creating nested function to remove stop words
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)
    
    # picking color for word cloud image randomly
    color = np.random.choice(['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Blues', 'Greens', 'Oranges', 'Reds','coolwarm', 'bwr', 'RdBu', 'RdYlBu', 'PiYG', 'twilight', 'hsv', 'twilight_shifted', 'hsv_r','tab10', 'tab20', 'tab20b', 'tab20c', 'Pastel1', 'Pastel2', 'Set1', 'Set2', 'Set3','flag', 'prism', 'nipy_spectral', 'terrain', 'cubehelix'])

    
    wc = WordCloud(width=1000, height =500, min_font_size=10 , colormap = color)

    temp['Message_'] = temp['Message_'].apply(remove_stop_words) # calling nested function through apply function

    df_wc = wc.generate(temp['Message_'].str.cat(sep =" "))
    # converting word cloud object in pil.image object, so that streamlit.image() can display image!
    pil_image = Image.fromarray(df_wc.to_array())

    return pil_image


def most_common_words(selected_user, df):

        if selected_user != "Overall":
            df = df[df['User'] == selected_user]

        temp = df[df['Message_'] != "<Media omitted>\n"]
        temp = temp[temp['Message_'] != "Notification"]
        temp = temp[temp['Message_'] != "Missed voice call\n"]
        temp = temp[temp['Message_'] != "You deleted this message\n"]

        words= []
        for msg in temp['Message_']:
         for word in msg.lower().split():
          if word not in stopwords:
            words.append(word)
        
        most_common_words_df = pd.DataFrame(Counter(words).most_common(20), columns=['Message', 'Occurrence'])
        return  most_common_words_df


def emoji_helper(selected_user,df):
  
    if selected_user != "Overall":
            df = df[df['User'] == selected_user]

    emojis = []
    for message in df['Message_']:
      emojis.extend([c for c in message if c in em.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))),  columns=['Emojis', 'Occurrence'])

    return emoji_df

def to_get_timeline(selected_user, df):
    if selected_user != "Overall":
      df = df[df['User'] == selected_user]
    
    df['Month_Num'] = df['Dates'].dt.month

    timeline_df= df.groupby(['Year','Month','Month_Num'])['Message_'].count().reset_index()
    

    time = []
    for i in range(timeline_df.shape[0]):
      time.append(timeline_df['Month'][i] + '-' + str(timeline_df['Year'][i]))
    
    timeline_df['Time'] = time
    return timeline_df


def daily_timeline(selected_user, df):
        if selected_user != "Overall":
          df = df[df['User'] == selected_user]

        df['dates'] = df['Dates'].dt.day
        daily_timeline = df.groupby('dates')['Message_'].count().reset_index()

        return daily_timeline

def weely_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    weekly_map_df = df['Day Name'].value_counts().reset_index()

    

    return weekly_map_df


def monthly_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    monthly_map_df = df['Month'].value_counts().reset_index()

    

    return monthly_map_df


def activity_heatmap(selected_user, df):
        if selected_user != "Overall":
          df = df[df['User'] == selected_user]

        activity_heatmap = df.pivot_table(index = 'Day Name', columns = 'Period', values = 'Message_', aggfunc = 'count').fillna(0)
        return activity_heatmap



def sentiment_analysis(selected_user, df):
        if selected_user != "Overall":
          df = df[df['User'] == selected_user]

        df['sentiment'] = df['Message_'].apply(lambda x: TextBlob(x).sentiment.polarity)
        
        # Categorize the sentiment
        df['sentiment_category'] = df['sentiment'].apply(lambda x: 'Positive' if x > 0 else 'Negative' if x < 0 else 'Neutral')

        return df



        

 





