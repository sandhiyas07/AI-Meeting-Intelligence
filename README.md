# 🎙️ AI Meeting Intelligence

### Smart Meeting Summarizer & Action Item Generator

AI Meeting Intelligence is an AI-powered application that analyzes meeting recordings and automatically generates meeting summaries, important discussion points, action items, and complete transcripts using Google Gemini AI.

It helps users save time, understand meeting discussions, and organize important tasks efficiently.

---

## 🚀 Features

- 🎵 **Audio Upload:** Upload meeting recordings in MP3, WAV, and M4A formats.
- 🤖 **AI Meeting Analysis:** Analyze audio recordings using Google Gemini AI.
- 📝 **Meeting Summary:** Automatically generate concise or detailed meeting summaries.
- 💡 **Key Point Extraction:** Identify important discussions and decisions.
- ✅ **Action Item Generator:** Extract tasks, assigned persons, and deadlines.
- 📄 **Meeting Transcript:** Generate a text transcript of the meeting.
- 📥 **PDF Report:** Download meeting analysis as a PDF report.
- 🌐 **Multiple Languages:** Select the preferred meeting language.
- 🎨 **Modern Dashboard:** Simple and user-friendly Streamlit interface.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Streamlit | Web application interface |
| Google Gemini AI | AI meeting analysis |
| Google Gen AI SDK | Gemini API integration |
| ReportLab | PDF report generation |
| Python-dotenv | Environment variable management |

---

## 📂 Project Structure

```text
AI-Meeting-Intelligence/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── services/
    ├── __init__.py
    └── gemini_service.py
```

---

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/AI-Meeting-Intelligence.git
```

### Step 2: Open Project Folder

```bash
cd AI-Meeting-Intelligence
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Gemini API Key

Create a `.env` file in the project root directory.

```env
GEMINI_API_KEY=your_actual_gemini_api_key
```

Get your API key from:

https://aistudio.google.com/apikey

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📖 How to Use

1. Open the AI Meeting Intelligence application.
2. Upload a meeting recording.
3. Select the preferred meeting language.
4. Choose the summary detail level.
5. Click the **Analyze Meeting** button.
6. Wait for Gemini AI to process the recording.
7. View the generated meeting summary.
8. Explore key points and action items.
9. Read the complete meeting transcript.
10. Download the meeting report as a PDF.

---

## 📊 Application Output

The application generates:

- Meeting Summary
- Important Key Points
- Action Items
- Assigned Persons
- Task Deadlines
- Complete Meeting Transcript
- Downloadable PDF Report

---

## 🔐 Security

- Store your Gemini API key in the `.env` file.
- Never upload your `.env` file to GitHub.
- Add `.env` to `.gitignore`.
- Do not expose API credentials in public repositories.
- Use meeting recordings only with appropriate permission.

---

## 🔮 Future Enhancements

- Real-time meeting transcription.
- Speaker identification.
- Meeting sentiment analysis.
- Automatic email notifications.
- Google Calendar integration.
- Meeting history dashboard.
- Multi-meeting analytics.

---

## 🎯 Project Objective

The main objective of AI Meeting Intelligence is to automate meeting documentation using Artificial Intelligence. It converts audio recordings into structured and meaningful information, making meeting management easier and more productive.

---

## 👩‍💻 Developed By

**Sri Nithya**

AI Meeting Intelligence  
Python | Streamlit | Google Gemini AI

---

## ⭐ Support

If you find this project useful, consider giving this repository a star!

**Built with Python and Google Gemini AI.**
