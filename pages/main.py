import streamlit as st

from utils import *
from plot import *


def show_main_page():
    # Initialize session state for dataframe
    if 'df' not in st.session_state:
        st.session_state.df = None
    
    # File uploader for JSON files
    file = st.sidebar.file_uploader("Add your JSON files", accept_multiple_files=False, type='json')
    btn = st.sidebar.button("Використати приклад")
    
    # Handle file loading
    if file is not None:
        # New file uploaded
        if isinstance(file, str):  # Handle the case where file is a string
            df = read_json(open(file, 'r', encoding='utf-8'))
        else:
            df = read_json(file)
        st.session_state.df = df  # Store in session state
    elif btn:
        # Example button clicked
        df = read_json(open('result.json', 'r', encoding='utf-8'))
        st.session_state.df = df  # Store in session state
    
    # Process data if available
    if st.session_state.df is not None:
        df = st.session_state.df
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        
        # Get unique years for multiselect
        unique_years = sorted(df['year'].unique())
        if len(unique_years) > 0:
            selected_years = st.sidebar.multiselect(
            "Select Years", 
            unique_years,
            default=unique_years  # Default to all years selected
            )
            
            # Add global chart scaling checkbox to sidebar
            scale_charts = st.sidebar.checkbox(
                "Масштабувати діаграми відносно даних", 
                value=True
            )
            
            # If no years selected, use all years
            if not selected_years:
                selected_years = unique_years
                
            # Filter data by selected years
            filtered_df = df[df['year'].isin(selected_years)]
            
            show_avg_and_max_len(filtered_df)
            
            one, two = st.columns(2)
            
            with one:
                plot_heatmap(filtered_df)
            
            with two:
                plot_pie(filtered_df)
            
            plot_emoji(filtered_df, scale_charts)
            plot_media_type(filtered_df, scale_charts)
            plot_stacked_bar_chart(filtered_df)
    else:
        st.header("Вітаємо у Telegram Chat Analyzer! 🎉")
        st.write("Цей інструмент допоможе вам дослідити ваші чати у Telegram.")
        st.write("Завантажте JSON-файл, щоб почати аналіз ваших розмов.")
        st.markdown("### Що ви можете зробити тут?")
        st.write("- Аналізувати активність у чатах за роками.")
        st.write("- Досліджувати найпопулярніші емодзі, медіа та повідомлення.")
        st.write("- Візуалізувати дані за допомогою графіків та діаграм.")
        st.markdown("### Як почати?")
        st.write("Просто завантажте JSON-файл з вашими чатами у боковій панелі, і ми зробимо все інше!")
        st.write("🚀 Готові? Почнемо!")
