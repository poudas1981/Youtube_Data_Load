# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 15:38:55 2021

@author: merlin mpoudeu
Creating the first app to display youtube video statistics
"""

import streamlit as st
import requests
import json
import pandas as pd
from apiclient.discovery import  build
from youtube_transcript_api import YouTubeTranscriptApi
import googletrans
from googletrans import Translator
import time
import base64

# pip install pipreqs
# pipreqs /home/project/location

api_key = "AIzaSyCThqVv2000rW8LTPH80_5_i9AhqJAsM70"
@st.cache  # 👈 Added this
def comment_comb(api_key, video_id):
    """
    Get all comments from a video
    """
    youtube = build('youtube', 'v3', developerKey= api_key)
    comments = youtube.commentThreads().list(
            part = 'snippet, replies',
            videoId = video_id).execute()
    n = comments['pageInfo']['totalResults']
    if n > 0:
        for i in range(0, n):
            videoID = video_id
            text = comments['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal']
            if i == 0:
                try:
                    dat_dict = {'Video_ID': videoID,
                                    'Comment': text}
                    dat = pd.DataFrame([dat_dict])
                except:
                    print('There is no comment ')
                    dat = pd.DataFrame(columns=['Video_ID', 'Comment'])
            else:
                try:
                    dat_dict = {'Video_ID': videoID,
                        'Comment': text}
                    dat2 = pd.DataFrame([dat_dict])
                    dat = dat.append(dat2)
                except:
                    print('Another error')
                    dat2 = pd.DataFrame(columns=['Video_ID', 'Comment'])
                    dat = dat.append(dat2)
    else:
        print('The dataset is empty')
        dat = pd.DataFrame(columns=['Video_ID', 'Comment'])
    return dat

@st.cache  # 👈 Added this
def convert_english_to_french(text):

    translator = Translator()
    output = translator.translate(text, dest ='fr').text
    return output

@st.cache  # 👈 Added this
def filedownload(df):
    # path = str(Name) + str('comments.csv')
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download= "commentaires.csv"> Download CSV File</a>'
    href2 = f'<a href="data:file/txt;base64,{b64}" download= "commentaires.txt"> Download txt File</a>'
    return href2, href

path = 'https://github.com/poudas1981/Youtube_Data_Load/blob/main/dataset_analysis_raw.csv'
path2 = 'https://github.com/poudas1981/Youtube_Data_Load/blob/main/dataset_analysis_raw.csv?raw=true'
dataset = pd.read_csv(path2)
st.sidebar.header('User Input Features')
option = st.sidebar.selectbox(
    'What do you want to do?',
     ['Download comment', 'Translate English into French', 'Classify comments?'])
st.sidebar.header('Select your name')
if option == 'Download comment':
    st.title('Download Comments')
    video_id = st.text_input('Input a new video ID', value='kQDxmjfkIKY', max_chars=None, key=None, type='default')
    if st.checkbox('show the first 5 rows of the comment'):
        comment_data = comment_comb(api_key, video_id)
        # comment_data2 = comment_data[['ID', 'Video_ID', 'comment_fr', 'Name', 'Target']]
        st.write(comment_data.head())
        dead = comment_data.head()
        st.markdown(filedownload(comment_data),  unsafe_allow_html=True)
elif option == 'Classify comments?':
    st.title('Sentiment Analysis')
    Name = st.sidebar.selectbox('Select your name',
                            ['Maxime Pouokam', 'Charles Ndonzeu', 'Ben Hassan',
                             'International Tchatcho', 'Tchango International',
                             'Cedric Sougang', 'Thierry Aubin Moukam', 'Serge Ewane',
                             'Cyrille Nzouda','Merlin Mpoudeu'])
    Text = """Thank you VAR for participating in this study. Our goal is to develop a tool \
                 that can be used to predict a comment from a video as Positive, \
                     Negative, or Neutral.
                    Your job is to read the comments and make the classification.
                    After you are done, you will send your results to the following\
                        email: ***merlinmpoudeu@gmail.com***."""
    st.write(Text.replace('VAR', Name))
    st.write("""
    The column that you should translate is named Comment_fr. After reading each comment,\
        you should classify it as either Positive, Negative, or Neutral.\
    A positive comment is a comment that after reading it, the underline meaning is good.
    Another way around for the negative comment. Neutral when you cannot classify as either negative or positive.\
        The column that you should field is named Target.
        
             """)
    st.write("""
             Bear with me, it could happen that the comment is still written in English,\
                 in that case, follow these steps:
                     1. Copy the comment
                     2. Come back to this webApp, on the left pannel under User Input Features\
                         select **Translate English into French**.
                    3. Paste your comment
                    4. Copy the translated comment and paste it in your excel sheet.
                    5. Perform your classification.
             """)
    dat = dataset[dataset['Name'] == Name]
    dat['Target'] = ''
    dat2 = dat[['ID', 'Video_ID', 'comment_fr', 'Name', 'Target']]
    if st.checkbox('The first five comments of your dataset is'):
        # st.write(dat.head())
        st.dataframe(dat2.head())
    st.markdown(filedownload(dat2), unsafe_allow_html=True)
    
else:
    st.write("""
     # Translate English to French        
     """)
    text = st.text_input('Input the Englist sentence', value='My name is Merlin', max_chars=None, key=None, type='default')
    Text = convert_english_to_french(text)
    st.write(Text)

st.balloons()
