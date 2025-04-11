import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

import calendar
import seaborn as sns

from utils import *


st.set_page_config(layout="wide")

def show_main_page():
    # File uploader for JSON files
    file = st.sidebar.file_uploader("Add your JSON files", accept_multiple_files=False, type='json')

    if file is not None:
        df = read_json(file)

        text_df = df[['date', 'from', 'text']].copy()
        text_df = text_df[text_df['text'] != '']     

        text_df['date'] = pd.to_datetime(text_df['date'])

        hour_day = text_df.groupby([text_df['date'].dt.dayofweek, text_df['date'].dt.hour]).size().unstack()
        hour_day.index = [calendar.day_name[day] for day in hour_day.index]

        fig = px.imshow(hour_day, color_continuous_scale='YlOrRd', labels={'x': 'Hour of Day', 'y': 'Day of Week'})
        fig.update_layout(title='When Conversations Happen', xaxis_title='Hour of Day', yaxis_title='Day of Week')

        one, two = st.columns(2)
        with one:
            st.plotly_chart(fig)

        message_counts = df['from'].value_counts().reset_index()
        labels = message_counts['from']
        sizes = message_counts['count']

        fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, textinfo='percent', hole=.3)])
        fig.update_layout(title='Message Distribution by User')
        with two:
            st.plotly_chart(fig)

        text_df['length'] = text_df['text'].apply(len)

        avg_length = text_df.groupby('from')['length'].mean().reset_index()
        avg_length.rename(columns={'length': 'avg_length'}, inplace=True)

        max_length = text_df.groupby('from')['length'].max().reset_index()
        max_length.rename(columns={'length': 'max_length'}, inplace=True)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=avg_length['from'],
            y=avg_length['avg_length'],
            name='Average Length',
            marker_color='indianred'
        ))
        fig.add_trace(go.Bar(
            x=max_length['from'],
            y=max_length['max_length'],
            name='Max Length',
            marker_color='lightsalmon'
        ))
        fig.update_layout(
            title='Message Length Statistics per User',
            barmode='group',
            xaxis_title='User',
            yaxis_title='Length'
        )
        st.plotly_chart(fig)

    else:
        st.header("Main Page")
        st.write("Upload a JSON file to analyze your conversations.")
        st.write("No files uploaded yet.")
