
"""
AI Meeting Intelligence
Smart Meeting Summarizer & Action Item Generator

Powered by:
Streamlit, Gemini API, Python and ReportLab
"""

import streamlit as st
import os
import io
from datetime import datetime
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Import Gemini service
from services.gemini_service import analyze_meeting_audio


# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="AI Meeting Intelligence",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()


# -------------------------------
# CUSTOM CSS
# -------------------------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
}

.header-box {
    background: linear-gradient(120deg, #312e81, #6366f1);
    padding: 30px;
    border-radius: 15px;
    color: white;
    margin-bottom: 25px;
}

.header-box h1 {
    color: white;
    font-size: 35px;
}

.header-box p {
    color: #e0e7ff;
    font-size: 16px;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}

.stButton button {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    color: white;
    border-radius: 8px;
    border: none;
    height: 45px;
    font-weight: bold;
}

.stButton button:hover {
    background: #4338ca;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------
# SESSION STATE
# -------------------------------

if "meeting_result" not in st.session_state:
    st.session_state.meeting_result = None

if "meeting_filename" not in st.session_state:
    st.session_state.meeting_filename = None


# -------------------------------
# PDF GENERATOR
# -------------------------------

def generate_pdf(result):

    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    y = height - 50

    def write_text(text, heading=False):

        nonlocal y

        if y < 70:
            pdf.showPage()
            y = height - 50

        if heading:
            pdf.setFont("Helvetica-Bold", 13)
        else:
            pdf.setFont("Helvetica", 10)

        text = str(text).replace("\n", " ")

        words = text.split()
        line = ""

        for word in words:

            test_line = line + " " + word if line else word

            if pdf.stringWidth(test_line, "Helvetica", 10) > width - 100:
                pdf.drawString(50, y, line)
                y -= 16
                line = word
            else:
                line = test_line

        if line:
            pdf.drawString(50, y, line)
            y -= 20

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, y, "AI Meeting Intelligence")

    y -= 35

    write_text(
        "Generated on: " + datetime.now().strftime("%d-%m-%Y %H:%M")
    )

    y -= 10

    write_text("MEETING SUMMARY", True)
    write_text(result.get("summary", "No summary available"))

    y -= 15

    write_text("KEY POINTS", True)

    for item in result.get("key_points", []):
        write_text("- " + str(item))

    y -= 15

    write_text("ACTION ITEMS", True)

    for item in result.get("action_items", []):
        if isinstance(item, dict):
            write_text(
                "- Task: " + str(item.get("task", item.get("title", "")))
            )
            write_text(
                "  Assigned to: " + str(item.get("assigned_to", "Not specified"))
            )
            write_text(
                "  Deadline: " + str(item.get("deadline", "Not specified"))
            )
        else:
            write_text("- " + str(item))

    y -= 15

    write_text("TRANSCRIPT", True)
    write_text(result.get("transcript", "No transcript available"))

    pdf.save()

    buffer.seek(0)

    return buffer.getvalue()


# -------------------------------
# HEADER
# -------------------------------

st.markdown("""
<div class="header-box">

<h1>🎙️ AI Meeting Intelligence</h1>

<p>
Smart Meeting Summarizer & Action Item Generator
</p>

<p>
Transform your meeting recordings into meaningful insights
using Artificial Intelligence.
</p>

</div>
""", unsafe_allow_html=True)


# -------------------------------
# SIDEBAR
# -------------------------------

with st.sidebar:

    st.title("⚙️ Settings")

    st.markdown("---")

    language = st.selectbox(
        "Meeting Language",
        [
            "English",
            "Tamil",
            "Hindi",
            "Malayalam",
            "Telugu"
        ]
    )

    detail = st.selectbox(
        "Summary Detail",
        [
            "Short",
            "Medium",
            "Detailed"
        ]
    )

    st.markdown("---")

    st.subheader("Supported Formats")

    st.write("🎵 MP3")
    st.write("🎵 WAV")
    st.write("🎵 M4A")

    st.markdown("---")

    st.info(
        "Upload your meeting recording "
        "and let Gemini AI analyze it."
    )


# -------------------------------
# AUDIO UPLOAD
# -------------------------------

st.subheader("📁 Upload Meeting Recording")

uploaded_file = st.file_uploader(
    "Choose your meeting audio file",
    type=["mp3", "wav", "m4a"]
)

if uploaded_file:

    audio_bytes = uploaded_file.getvalue()

    st.success(
        f"Uploaded successfully: {uploaded_file.name}"
    )

    st.audio(audio_bytes)

    st.write(
        f"File Size: {len(audio_bytes) / (1024 * 1024):.2f} MB"
    )

    analyze_button = st.button(
        "🚀 Analyze Meeting",
        use_container_width=True
    )

    if analyze_button:

        if not os.getenv("GEMINI_API_KEY"):

            st.error(
                "GEMINI_API_KEY not found. "
                "Please configure your .env file."
            )

        elif not audio_bytes:

            st.warning("Please upload a valid audio file.")

        elif len(audio_bytes) > 20 * 1024 * 1024:

            st.error(
                "File is too large. Please upload an audio "
                "file smaller than 20 MB."
            )

        else:

            try:

                with st.spinner(
                    "🤖 Gemini AI is analyzing your meeting... "
                    "Please wait."
                ):

                    result = analyze_meeting_audio(
                        audio_bytes,
                        uploaded_file.name,
                        language,
                        detail
                    )

                    if not isinstance(result, dict):
                        raise ValueError(
                            "Gemini service must return a dictionary."
                        )

                    st.session_state.meeting_result = result

                    st.session_state.meeting_filename = (
                        uploaded_file.name
                    )

                st.success(
                    "Meeting analysis completed successfully!"
                )

            except Exception as e:

                st.error(
                    f"Meeting analysis failed: {str(e)}"
                )

                st.info(
                    "Check your Gemini API key, internet connection "
                    "and gemini_service.py file."
                )


# -------------------------------
# DISPLAY RESULTS
# -------------------------------

result = st.session_state.meeting_result

if result:

    st.markdown("---")

    st.title("📊 Meeting Analysis Dashboard")

    st.caption(
        f"File: {st.session_state.meeting_filename}"
    )

    # METRICS

    key_points = result.get("key_points", [])
    action_items = result.get("action_items", [])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Key Points",
            len(key_points)
        )

    with col2:
        st.metric(
            "Action Items",
            len(action_items)
        )

    with col3:
        st.metric(
            "Analysis Status",
            "Completed"
        )

    st.markdown("---")

    # TABS

    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Summary",
        "💡 Key Points",
        "✅ Action Items",
        "📄 Transcript"
    ])

    # SUMMARY TAB

    with tab1:

        st.subheader("Meeting Summary")

        st.write(
            result.get(
                "summary",
                "No summary available."
            )
        )

    # KEY POINTS TAB

    with tab2:

        st.subheader("Important Key Points")

        if key_points:

            for index, point in enumerate(
                key_points, start=1
            ):

                st.markdown(
                    f"**{index}.** {point}"
                )

        else:

            st.info("No key points available.")

    # ACTION ITEMS TAB

    with tab3:

        st.subheader("Meeting Action Items")

        if action_items:

            for index, item in enumerate(
                action_items, start=1
            ):

                if isinstance(item, dict):

                    task = item.get(
                        "task",
                        item.get("title", "Not specified")
                    )

                    assigned_to = item.get(
                        "assigned_to",
                        "Not specified"
                    )

                    deadline = item.get(
                        "deadline",
                        "Not specified"
                    )

                    with st.expander(
                        f"Task {index}: {task}"
                    ):

                        st.write(
                            f"**Task:** {task}"
                        )

                        st.write(
                            f"**Assigned To:** {assigned_to}"
                        )

                        st.write(
                            f"**Deadline:** {deadline}"
                        )

                else:

                    st.write(f"✅ {item}")

        else:

            st.info("No action items available.")

    # TRANSCRIPT TAB

    with tab4:

        st.subheader("Meeting Transcript")

        transcript = result.get(
            "transcript",
            "No transcript available."
        )

        st.text_area(
            "Full Transcript",
            value=transcript,
            height=350
        )

    # PDF DOWNLOAD

    st.markdown("---")

    st.subheader("📥 Download Meeting Report")

    try:

        pdf_data = generate_pdf(result)

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_data,
            file_name="meeting_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"PDF generation failed: {str(e)}"
        )


# -------------------------------
# FOOTER
# -------------------------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:gray;">

    <p>AI Meeting Intelligence</p>

    <p>Powered by Python | Streamlit | Gemini AI</p>

    </div>
    """,
    unsafe_allow_html=True
)
