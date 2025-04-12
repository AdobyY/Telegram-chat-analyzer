# Telegram Chat Analyzer

https://github.com/user-attachments/assets/30cf5d51-5125-48d5-91c3-c1fd549dfb30

## 🌐 Live Demo

[Try the Telegram Chat Analyzer online](https://telegram-chat-analyzer.streamlit.app/)

---

Telegram Chat Analyzer is an advanced and interactive web application designed to help you dive deep into your Telegram chat data. Whether you're analyzing group chats, personal conversations, or professional discussions, this tool provides a comprehensive suite of visualizations and metrics to uncover patterns, trends, and insights.

## 🌟 Key Features

- **📊 Message Statistics**: Analyze average message length, maximum message length, and message counts for each participant.
- **🔥 Activity Heatmap**: Discover when conversations are most active during the week and day.
- **📈 Message Distribution**: Visualize the share of messages contributed by each participant.
- **🎥 Media Analysis**: Explore the types of media shared, including photos, videos, stickers, and more.
- **😂 Emoji Insights**: Identify the most frequently used emojis and their distribution among participants.
- **📅 Yearly Filters**: Focus on specific time periods with year-based filtering.
- **📄 Exportable Reports**: Generate and download PDF reports of your visualizations for sharing or offline analysis.

## 🚀 Installation

Follow these steps to set up Telegram Chat Analyzer on your local machine:

1. Clone this repository:

```bash
git clone https://github.com/yourusername/Telegram-chat-analyzer.git
cd Telegram-chat-analyzer
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## 🛠️ Usage

1. **Export Your Telegram Chat Data**:

   - Open Telegram (desktop app).
   - Select the chat you want to analyze.
   - Click on the three dots (⋮) in the top right corner.
   - Select "Export chat history."
   - Choose JSON format and download the file.
2. **Run the Application**:

```bash
streamlit run index.py
```

3. **Upload and Explore**:
   - Upload your exported JSON file.
   - Use the interactive interface to explore your chat data through various visualizations and metrics.

## 📚 Dependencies

Telegram Chat Analyzer relies on the following Python libraries:

- **Streamlit**: For building the interactive web application.
- **Pandas**: For data manipulation and analysis.
- **Plotly**: For creating interactive visualizations.

## 🔒 Privacy and Security

Your privacy is our top priority. Telegram Chat Analyzer:

- Runs entirely on your local machine or browser
- Never uploads your chat data to any server
- Never shares your information with third parties
- Provides optional data anonymization features
- Allows you to delete all imported data with one click

## 🤝 ContributingWe welcome contributions to improve Telegram Chat Analyzer! Feel free to submit issues, feature requests, or pull requests to the repository.

## 📜 License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

---

### 💡 Pro Tip

Want to customize the visualizations or add new features? Dive into the `plot.py` and `main.py` files to tweak the code and make it your own!
