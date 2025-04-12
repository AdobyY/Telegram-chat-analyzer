# Telegram Chat Analyzer

An interactive web application to analyze and visualize your Telegram chat data.

## Features

- **Message Stats**: View metrics for each user including average message length and message count
- **Activity Heatmap**: See when conversations happen throughout the week
- **Message Distribution**: View the share of messages per participant
- **Media Analysis**: Analyze the types of media shared (photos, videos, stickers, etc.)
- **Emoji Usage**: See which emojis are used most frequently
- **Year Filter**: Filter your chat data by year using multi-select

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/Telegram-chat-analyzer.git
cd Telegram-chat-analyzer
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Export your Telegram chat data:
   - Open Telegram (desktop app)
   - Select the chat you want to analyze
   - Click on the three dots (⋮) in the top right
   - Select "Export chat history"
   - Choose JSON format
   - Download the file

2. Run the application:
```bash
streamlit run app.py
```

3. Upload your JSON file and explore your chat data!

## Dependencies

- Python 3.7+
- streamlit
- pandas
- plotly
- wordcloud
- numpy
- seaborn

## Privacy

This application runs locally on your machine. Your chat data is not uploaded to any server or shared with anyone.

## License

Apache License 2.0
