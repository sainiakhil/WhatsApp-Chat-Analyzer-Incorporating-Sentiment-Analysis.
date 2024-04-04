

import streamlit as st 
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.graph_objects as go

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode(encoding="utf-8")
    df = preprocessor.preprocess(data)

# fetching unique users
    user_list = df['User'].unique().tolist()
    user_list.remove("Notification")
    user_list.sort()
    user_list.insert(0,"Overall")

    st.sidebar.divider()

    selected_user = st.sidebar.selectbox("Show Analysis with Respect to", user_list)


    if st.sidebar.button("Show Analysis"):

        # fetching stats----------------------------------!
        num_msg, num_words, num_media, num_link = helper.fetch_stats(selected_user, df)

        st.title('Top Statistics') 
        st.divider()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header(':blue[Total Messages]')
            st.header(num_msg)

        with col2:
            st.header(":blue[Total Words]")
            st.header(num_words)

        with col3:
            st.header(":blue[Media Shared]")
            st.header(num_media)
        
        with col4:
            st.header(":blue[Links Shared]")
            st.header(num_link)
        
        # timeline-------------------------------------!
        st.divider()
        st.subheader('Monthy Timeline of the User')
        timeline_df = helper.to_get_timeline(selected_user, df)
        st.line_chart(data = timeline_df, x = 'Time', y= 'Message_')

        # daily timeline-------------------------------!
        st.subheader('Daily Timeline of the User')
        daily_timeline_df = helper.daily_timeline(selected_user,df)
        st.line_chart(data = daily_timeline_df, x = 'dates', y= 'Message_')

        # weekly map --------------------!
        st.header('Activity Map', divider = True)
        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Most Busy Day')
            weekly_map = helper.weely_map(selected_user,df)
            st.bar_chart(weekly_map, x = 'Day Name', y = 'count')

        with col2:
            st.subheader('Most Busy Month')
            monthly_map = helper.monthly_map(selected_user,df)
            st.bar_chart(monthly_map, x = 'Month', y = 'count')


        # activity heatmap
        st.subheader("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)

            # picking color for word cloud image randomly
        color = np.random.choice(['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Blues', 'Greens', 'Oranges', 'Reds','coolwarm', 'bwr', 'RdBu', 'RdYlBu', 'PiYG', 'twilight', 'hsv', 'twilight_shifted', 'hsv_r','tab10', 'tab20', 'tab20b', 'tab20c', 'Pastel1', 'Pastel2', 'Set1', 'Set2', 'Set3','flag', 'prism', 'nipy_spectral', 'terrain', 'cubehelix'])

        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap, cmap = color, annot=True)

        st.pyplot(fig)

            


        # finding the busiest users in the group(only group level)-------------------------------!
        
        if selected_user == 'Overall':
            
            st.subheader("Most Busy Users", divider = True)

            x_df, per_df = helper.most_busy_users(df) 

            col1, col2 = st.columns(2)

            with col1:
                st.bar_chart(x_df)

            with col2:
                st.dataframe(per_df)

        # displaying wordcloud from df['message_'] column from dataframe-----------------------------------!
                
        
        st.subheader("Word Cloud Featuring Frequently Utilized Words")
        pil_wc_image = helper.create_wordcloud(selected_user,df)
        st.image(pil_wc_image, caption='Word Cloud')
        

        # displaying most common words used in chats--------------------!
        most_common_words_df = helper.most_common_words(selected_user,df)

        st.subheader("Most Commonly Used Words")
        st.bar_chart(most_common_words_df, x = 'Message', y ='Occurrence')
        
        # emoji analysis------------------------------!
        emoji_df = helper.emoji_helper(selected_user,df)
        st.subheader("Emoji Analysis", divider=True)

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        
        with col2:

            st.bar_chart(data = emoji_df.head(50), x= 'Emojis', y ='Occurrence')

        # displaying sentiment analysis---------------------------------------------------!
        
        sentiment_df = helper.sentiment_analysis(selected_user, df)
        st.subheader("Chat Sentiment Analysis", divider=True)

        st.bar_chart(sentiment_df['sentiment_category'].value_counts())

        st.divider()

        # Create an interactive pie chart
        labels = sentiment_df['sentiment_category'].unique()
        values = sentiment_df['sentiment_category'].value_counts()

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        st.plotly_chart(fig)
        st.divider()




        
        

  
        
             


            
