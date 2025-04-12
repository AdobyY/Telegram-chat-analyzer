import calendar
import pandas as pd
import streamlit as st

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def show_avg_and_max_len(df):
    df['length'] = df['text'].apply(len)
    avg_length = df.groupby('from')['length'].mean().reset_index()
    max_length = df.groupby('from')['length'].max().reset_index()
    
    # Об'єднання середньої та максимальної довжини в одну таблицю
    user_stats = avg_length.merge(max_length, on='from', suffixes=('_avg', '_max'))
    
    # Підрахунок кількості повідомлень для кожного користувача
    msg_count = df['from'].value_counts().reset_index()
    msg_count.columns = ['from', 'message_count']
    
    # Об'єднання зі статистикою користувачів
    user_stats = user_stats.merge(msg_count, on='from')
        
    # Створення контейнера для метрик кожного користувача
    for _, user in user_stats.iterrows():
        with st.container():
            st.markdown(f"### {user['from']}")
            
            # Створення трьох метрик для кожного користувача
            col1, col2, col3 = st.columns(3)
            
            col1.metric(
                label="Середня довжина повідомлення ⏳",
                value=f"{user['length_avg']:.1f}",
                delta=f"{user['length_avg'] - user_stats['length_avg'].mean():.1f}"
            )
            
            col2.metric(
                label="Максимальна довжина повідомлення 📏",
                value=int(user['length_max']),
                delta=int(user['length_max'] - user_stats['length_max'].mean())
            )
            
            col3.metric(
                label="Кількість повідомлень 💬",
                value=int(user['message_count']),
                delta=int(user['message_count'] - user_stats['message_count'].mean())
            )

def plot_heatmap(df):
    text_df = df[['date', 'from', 'text']].copy()
    text_df = text_df[text_df['text'] != '']     

    text_df['date'] = pd.to_datetime(text_df['date'])

    hour_day = text_df.groupby([text_df['date'].dt.dayofweek, text_df['date'].dt.hour]).size().unstack()
    hour_day.index = [calendar.day_name[day] for day in hour_day.index]

    fig = px.imshow(hour_day, color_continuous_scale='YlOrRd', labels={'x': 'Година доби', 'y': 'День тижня'})
    fig.update_layout(title='Коли відбуваються розмови', xaxis_title='Година доби', yaxis_title='День тижня')
    
    st.plotly_chart(fig)

def plot_pie(df):
    message_counts = df['from'].value_counts().reset_index()
    labels = message_counts['from']
    sizes = message_counts['count']

    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, textinfo='percent', hole=.3)])
    fig.update_layout(title='Розподіл повідомлень за користувачами')
    
    st.plotly_chart(fig)
            

def plot_emoji(df, scale_charts=True):
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
    emoji_grouped = emoji_df.groupby(['from', 'reaction_emoji'])['reaction_count'].sum().reset_index()

    # Get unique users
    users = emoji_grouped['from'].unique()
    
    # Calculate total counts for each user for display in titles
    user_totals = {}
    for user in users:
        user_totals[user] = emoji_grouped[emoji_grouped['from'] == user]['reaction_count'].sum()
    
    # Calculate grid dimensions (max 4 columns)
    num_users = len(users)
    cols = min(num_users, 4)  # Maximum 4 columns
    rows = (num_users + cols - 1) // cols  # Ceiling division
    
    # Create pie charts with grid layout
    fig = make_subplots(
        rows=rows,
        cols=cols,
        specs=[[{'type': 'domain'} for _ in range(cols)] for _ in range(rows)],
        subplot_titles=[f"{user} ({int(user_totals[user])} реакцій)" for user in users]
    )
    
    # Add data for each user
    for i, user in enumerate(users):
        user_data = emoji_grouped[emoji_grouped['from'] == user]
        
        # Calculate row and column for this user
        row_idx = i // cols + 1  # 1-indexed for plotly
        col_idx = i % cols + 1   # 1-indexed for plotly
        
        fig.add_trace(
            go.Pie(
                labels=user_data['reaction_emoji'],
                values=user_data['reaction_count'],
                name=user,
                hole=0.4,
                textinfo='label+value',
                textposition='inside',
                marker=dict(line=dict(color='#000000', width=1)),
                scalegroup='one' if scale_charts else None  # Use passed parameter
            ),
            row=row_idx, col=col_idx
        )
    
    # Update layout for better appearance
    fig.update_layout(
        title_text="Реакції емодзі за користувачами",
        height=400 * rows,  # Adjust height based on number of rows
        showlegend=True,
        legend=dict(orientation="h", y=-0.1)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_media_type(df, scale_charts=True):
    media_type = df[~df['media_type'].isnull()].copy()
    media_type = media_type[['from', 'media_type', 'date']]
    media_type_grouped = media_type.groupby(['from', 'media_type']).size().reset_index(name='count')

    # Отримання унікальних користувачів
    users = media_type_grouped['from'].unique()
    
    # Підрахунок загальної кількості для кожного користувача для відображення у заголовках
    user_totals = {}
    for user in users:
        user_totals[user] = media_type_grouped[media_type_grouped['from'] == user]['count'].sum()
    
    # Розрахунок розмірності сітки (максимум 4 колонки)
    num_users = len(users)
    cols = min(num_users, 4)  # Максимум 4 колонки
    rows = (num_users + cols - 1) // cols  # Ділення з округленням вгору
    
    # Створення кругової діаграми з сітковим розташуванням
    fig = make_subplots(
        rows=rows,
        cols=cols,
        specs=[[{'type': 'domain'} for _ in range(cols)] for _ in range(rows)],
        subplot_titles=[f"{user} ({user_totals[user]} елементів)" for user in users]
    )
    
    # Додавання даних для кожного користувача
    for i, user in enumerate(users):
        user_data = media_type_grouped[media_type_grouped['from'] == user]
        
        # Розрахунок рядка та колонки для цього користувача
        row_idx = i // cols + 1  # 1-індексація для plotly
        col_idx = i % cols + 1   # 1-індексація для plotly
        
        fig.add_trace(
            go.Pie(
                labels=user_data['media_type'],
                values=user_data['count'],
                name=user,
                hole=0.4,
                textinfo='label+value',
                textposition='inside',
                marker=dict(line=dict(color='#000000', width=1)),
                scalegroup='one' if scale_charts else None  # Use passed parameter
            ),
            row=row_idx, col=col_idx
        )
    
    # Оновлення макету для кращого вигляду
    fig.update_layout(
        title_text="Розподіл типів медіа за користувачами",
        height=400 * rows,  # Налаштування висоти в залежності від кількості рядків
        showlegend=True,
        legend=dict(orientation="h", y=-0.1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_stacked_bar_chart(df):
    df.loc[:, 'year_month'] = df['date'].dt.to_period('M').astype(str)
    date_grouped = df.groupby(['from', 'year_month'])['date'].count().reset_index()
    date_grouped = date_grouped.pivot(index='year_month', columns='from', values='date').fillna(0).reset_index()

    # Create a stacked bar chart
    fig = go.Figure()
    for user in date_grouped.columns[1:]:  # Skip the 'year_month' column
        fig.add_trace(
            go.Bar(
                x=date_grouped['year_month'],
                y=date_grouped[user],
                name=user
            )
        )

    # Add total labels above each bar
    date_grouped['total'] = date_grouped.iloc[:, 1:].sum(axis=1)
    fig.add_trace(
        go.Scatter(
            x=date_grouped['year_month'],
            y=date_grouped['total'],
            mode='text',
            text=date_grouped['total'],
            textposition='top center',
            showlegend=False
        )
    )

    # Update layout for better appearance
    fig.update_layout(
        barmode='stack',
        title='Кількість повідомлень за місяцями',
        xaxis_title='Місяць',
        yaxis_title='Кількість повідомлень',
        legend_title='Користувачі',
        xaxis=dict(tickangle=-45),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)