import calendar
import pandas as pd
import streamlit as st
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
from collections import Counter
from plotly.subplots import make_subplots


def show_avg_and_max_len(df):
    df['length'] = df['text'].apply(len)
    avg_length = df.groupby('from')['length'].mean().reset_index()
    max_length = df.groupby('from')['length'].max().reset_index()
    
    # Combine average and maximum lengths into a single table
    user_stats = avg_length.merge(max_length, on='from', suffixes=('_avg', '_max'))
    
    # Calculate message count per user
    msg_count = df['from'].value_counts().reset_index()
    msg_count.columns = ['from', 'message_count']
    
    # Merge with user stats
    user_stats = user_stats.merge(msg_count, on='from')
        
    # Create a container for each user's metrics
    for _, user in user_stats.iterrows():
        with st.container():
            st.markdown(f"### {user['from']}")
            
            # Create three metrics for each user
            col1, col2, col3 = st.columns(3)
            
            col1.metric(
                label="Average Length ⏳",
                value=f"{user['length_avg']:.1f}",
                delta=f"{user['length_avg'] - user_stats['length_avg'].mean():.1f}"
            )
            
            col2.metric(
                label="Max Length 📏",
                value=int(user['length_max']),
                delta=int(user['length_max'] - user_stats['length_max'].mean())
            )
            
            col3.metric(
                label="Message Count 💬",
                value=int(user['message_count']),
                delta=int(user['message_count'] - user_stats['message_count'].mean())
            )
            

def plot_emoji(df):
    df['reaction_count'] = df['reactions'].apply(
        lambda x: x[0]['count'] 
        if isinstance(x, list) and len(x) > 0 and 'count' in x[0] 
        else None
    )

    df['reaction_emoji'] = df['reactions'].apply(
        lambda x: x[0]['emoji'] 
        if isinstance(x, list) and len(x) > 0 and 'count' in x[0] 
        else None
    )
    emoji_df = df[['date', 'from', 'reaction_emoji', 'reaction_count']]

    emoji_df = emoji_df.dropna(subset=['reaction_emoji'])
    grouped = emoji_df.groupby(['from', 'reaction_emoji'])['reaction_count'].sum().reset_index()

    # Filter for two users
    users = grouped['from'].unique()
    filtered_df = grouped[grouped['from'].isin(users)]

    # Create a donut chart
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

    for i, user in enumerate(users):
        user_data = filtered_df[filtered_df['from'] == user]
        fig.add_trace(
            go.Pie(
                labels=user_data['reaction_emoji'],
                values=user_data['reaction_count'],
                name=user,
                hole=0.4,
                textinfo='label+value'  # Show label and count instead of percentage
            ),
            row=1, col=i + 1
        )

    fig.update_layout(
        title_text="Emoji Reactions",
        annotations=[
            dict(text=users[0], x=0.18, y=0.5, font_size=14, showarrow=False),
            dict(text=users[1], x=0.82, y=0.5, font_size=14, showarrow=False)
        ]
    )

    st.plotly_chart(fig)



def plot_heatmap(df):
    text_df = df[['date', 'from', 'text']].copy()
    text_df = text_df[text_df['text'] != '']     

    text_df['date'] = pd.to_datetime(text_df['date'])

    hour_day = text_df.groupby([text_df['date'].dt.dayofweek, text_df['date'].dt.hour]).size().unstack()
    hour_day.index = [calendar.day_name[day] for day in hour_day.index]

    fig = px.imshow(hour_day, color_continuous_scale='YlOrRd', labels={'x': 'Hour of Day', 'y': 'Day of Week'})
    fig.update_layout(title='When Conversations Happen', xaxis_title='Hour of Day', yaxis_title='Day of Week')
    
    st.plotly_chart(fig)

def plot_pie(df):
    message_counts = df['from'].value_counts().reset_index()
    labels = message_counts['from']
    sizes = message_counts['count']

    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, textinfo='percent', hole=.3)])
    fig.update_layout(title='Message Distribution by User')
    
    st.plotly_chart(fig)


def plot_bar(df):
    text_df = df[['date', 'from', 'text']].copy()
    text_df['length'] = text_df['text'].apply(len)

    avg_length = text_df.groupby('from')['length'].mean().reset_index()
    avg_length.rename(columns={'length': 'avg_length'}, inplace=True)

    max_length = text_df.groupby('from')['length'].max().reset_index()
    max_length.rename(columns={'length': 'max_length'}, inplace=True)


def plot_media_type(df):
    media_type = df[~df['media_type'].isnull()].copy()
    media_type = media_type[['from', 'media_type', 'date']]
    media_type_grouped = media_type.groupby(['from', 'media_type']).size().reset_index(name='count')

    # Get unique users
    users = media_type_grouped['from'].unique()
    
    # Calculate total counts per user for sizing
    user_totals = {}
    for user in users:
        user_totals[user] = media_type_grouped[media_type_grouped['from'] == user]['count'].sum()
    
    # Find max total for scaling
    max_total = max(user_totals.values())
    
    # Create a donut chart with multiple subplots (one for each user)
    fig = make_subplots(
        rows=1, 
        cols=len(users), 
        specs=[[{'type': 'domain'} for _ in range(len(users))]],
        subplot_titles=[f"{user} ({user_totals[user]} items)" for user in users]
    )
    
    # Add traces for each user
    for i, user in enumerate(users):
        user_data = media_type_grouped[media_type_grouped['from'] == user]
        
        # Calculate relative size factor (proportional to total count)
        size_factor = user_totals[user] / max_total
        
        fig.add_trace(
            go.Pie(
                labels=user_data['media_type'],
                values=user_data['count'],
                name=user,
                hole=0.4,
                textinfo='label+value',
                textposition='inside',
                marker=dict(line=dict(color='#000000', width=1)),
                domain={'x': [0.1, 0.9], 'y': [0.2, 0.2 + 0.6 * size_factor]}  # Adjust the size
            ),
            row=1, col=i+1
        )
    
    # Update layout for better presentation
    fig.update_layout(
        title_text="Media Type Distribution by User",
        height=500 if len(users) <= 2 else 700,
        width=300 * len(users),
        showlegend=True,
        legend=dict(orientation="h", y=-0.1)
    )
    
    st.plotly_chart(fig, use_container_width=True)