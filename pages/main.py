import streamlit as st

from utils import *
from plot import *

st.set_page_config(layout="wide")

def show_main_page():
    # File uploader for JSON files
    file = st.sidebar.file_uploader("Add your JSON files", accept_multiple_files=False, type='json')

    if file is not None:
        df = read_json(file)
        
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
            
            # If no years selected, use all years
            if not selected_years:
                selected_years = unique_years
                
            # Filter data by selected years
            df = df[df['year'].isin(selected_years)]
        
        show_avg_and_max_len(df)

        
        one, two = st.columns(2)

        with one:
            plot_heatmap(df)
            plot_bar(df)


        with two:
            plot_pie(df)

        plot_emoji(df)
        plot_media_type(df)


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
