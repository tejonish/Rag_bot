import streamlit as st
import tempfile
import os
import shutil
import re

from modules.resume import resume_feedback_tool, extract_github_from_resume
from modules.verification import verify_resume_with_github
from modules.jd_analysis import analyze_job_fit
from modules.ats import ats_score
from modules.interview import generate_questions, evaluate_answer
from rag_core import extract_full_text, build_rag_chain
from modules.report import generate_pdf_report
from streamlit_mic_recorder import mic_recorder
from modules.speech import transcribe_audio
from modules.fillers import count_fillers
from modules.assistant import candidate_assistant

st.set_page_config(page_title="AI Hiring Copilot", page_icon="🤖")
st.title("🚀 AI Hiring Copilot")
show_info = st.toggle("📌 Show Project Information")
if show_info:

    info_tab = st.radio(
        "Select",
        [
            "Architecture",
            "Tech Stack",
            "About"
        ],
        horizontal=True
    )

    if info_tab == "Architecture":

        st.image(
            "assets/architecture.png",
            use_container_width=True
        )

    elif info_tab == "Tech Stack":

        st.code("""
LangGraph
LangChain
FAISS
Groq
Llama 3.1
Whisper
Streamlit
GitHub API
PyPDFLoader
""")

    elif info_tab == "About":

        st.info("""
AI Hiring Copilot is an Agentic AI recruitment platform
built using LangGraph, LangChain, Groq LLMs, FAISS,
and Whisper.

Features:
• ATS Analysis
• Job Fit Scoring
• Mock Interviews
• Resume Verification
• Conversational AI Assistant
• Learning Roadmap Generation
""")
st.info("💻 Best viewed on laptop/desktop. Mobile upload may be unstable.")


def reset_vectordb():
    if os.path.exists("faiss_index"):
        shutil.rmtree("faiss_index")


if st.button("🔁 Reset Vector DB"):
    reset_vectordb()
    st.success("Reset Done ✅")


pdf_file = st.file_uploader("Upload Resume", type=["pdf"])

mode = st.radio(
    "Select Mode", ["🧑‍🎓 Candidate", "🧑‍💼 HR", "🎙 Candidate Assistant"], horizontal=True
)

if not pdf_file:
    st.info("Upload resume to continue")
    st.stop()

if pdf_file:

    if "temp_path" not in st.session_state:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_file.read())
            st.session_state["temp_path"] = tmp.name

    temp_path = st.session_state["temp_path"]

    if "resume_text" not in st.session_state:
        st.session_state["resume_text"] = extract_full_text(temp_path)

    resume_text = st.session_state["resume_text"]

    # GitHub
    if "github_user" not in st.session_state:
        st.session_state["github_user"] = extract_github_from_resume(temp_path)

    github = st.session_state["github_user"]

    if github:
        st.success(f"GitHub: {github}")
        st.markdown(f"[🔗 Open](https://github.com/{github})")
    else:
        github = st.text_input("Enter GitHub Username")

    # =========================
    # 🧑‍🎓 CANDIDATE
    # =========================
    if mode == "🧑‍🎓 Candidate":

        jd = st.text_area("Paste Job Description")

        if st.button("📊 Analyze Profile"):
            # fit = analyze_job_fit(resume_text, jd)
            # ats = ats_score(resume_text, jd)

            # st.markdown("### 📊 Job Fit")
            # st.code(fit)

            # st.markdown("### 📄 ATS Score")
            # st.code(ats)

            if not jd.strip():
                st.warning("Please paste Job Description ⚠️")
                st.stop()

            from agents.controller import run_pipeline

            result, steps = run_pipeline(resume_text, jd)
            st.markdown("### 🧠 Agent Decision")
            st.write(" → ".join(steps))

            st.markdown("### 📊 Job Fit")
            st.text(result)

            st.session_state["fit"] = result
            st.session_state["jd"] = jd

        if st.button("🎤 Start Mock Interview"):

            questions = generate_questions(resume_text, st.session_state["jd"])

            st.session_state["questions"] = questions
            st.session_state["question_index"] = 0
            st.session_state["interview_mode"] = True

            # st.session_state["ats"] = ats

        if st.button("📌 Resume Feedback"):
            fb = resume_feedback_tool(temp_path)
            st.code(fb)
            st.session_state["feedback"] = fb

        if st.button("📥 Generate Candidate Report"):
            if "fit" not in st.session_state:
                st.warning("Please run analysis first ⚠️")
                st.stop()

            report_text = st.session_state["fit"]

            if "feedback" in st.session_state:
                report_text += (
                    "\n\n📌 Resume Feedback\n\n" + st.session_state["feedback"]
                )
                file_path = generate_pdf_report(report_text, mode="candidate")

                with open(file_path, "rb") as f:
                    st.download_button(
                        label="Download Candidate PDF",
                        data=f,
                        file_name="Candidate_Report.pdf",
                        mime="application/pdf",
                    )

            st.success("Report ready ✅")

        if st.session_state.get("interview_mode"):

            st.subheader("🎤 Mock Interview")

            st.markdown("### 😂 Interview Mood")
            st.write("🎙 Waiting for answer...")

            idx = st.session_state["question_index"]

            questions = st.session_state["questions"]

            if idx < len(questions):

                st.markdown(f"### Question {idx + 1}")

                st.info(questions[idx])

                # answer = st.text_area("Your Answer", key=f"answer_{idx}")
                audio = mic_recorder(
                    start_prompt="🎙 Record Answer",
                    stop_prompt="⏹ Stop Recording",
                    key=f"mic_{idx}",
                )

                if st.button("📤 Submit Answer"):

                    if not audio:

                        st.warning("Please record your answer first 🎙")

                    else:

                        transcript = transcribe_audio(audio)

                        filler_count, filler_words = count_fillers(transcript)

                        st.session_state["filler_count"] = filler_count
                        st.session_state["filler_words"] = filler_words

                        st.session_state["transcript"] = transcript

                        feedback = evaluate_answer(questions[idx], transcript)

                        st.session_state["feedback"] = feedback

                if "transcript" in st.session_state:

                    st.markdown("### 📝 Transcript")
                    st.code(st.session_state["transcript"])

                if "filler_count" in st.session_state:

                    st.markdown("### 🎙 Speech Analysis")

                    st.metric("Fillers", st.session_state["filler_count"])

                    st.write(f"Detected: {', '.join(st.session_state['filler_words'])}")

                if st.session_state.get("filler_count", 0) >= 3:

                    st.image("assets/dumb monkey.jpg", width=250)

                    st.warning("🐒 Brain buffering detected...")
                    
                if "feedback" in st.session_state:

                    st.markdown("### 🤖 Feedback")
                    st.code(st.session_state["feedback"])

                    import re

                    score_match = re.search(
                        r"Score:\s*(\d+)",
                        st.session_state["feedback"]
                    )

                    score = int(score_match.group(1)) if score_match else 5

                    st.markdown("### 😂 Interview Mood")

                    if score >= 9:

                        st.image("assets/gigachad.jpg", width=250)

                    elif score >= 7:

                        st.image("assets/doge pic.jpg", width=250)

                    elif score >= 5:

                        st.image("assets/cat man idk.jpg", width=250)

                    else:

                        st.image("assets/pikachu.jpg", width=250)

                    if st.button("➡️ Next Question"):

                        st.session_state["question_index"] += 1

                        st.session_state.pop("feedback", None)
                        st.session_state.pop("transcript", None)
                        st.session_state.pop("filler_count", None)
                        st.session_state.pop("filler_words", None)

                        st.rerun()

                    

            else:

                st.success("🎉 Mock Interview Completed!")
                st.balloons()

    # =========================
    # HR
    # =========================
    elif mode == "🧑‍💼 HR":

        jd = st.text_area("Paste JD")

        if st.button("Evaluate"):
            if not jd.strip():
                st.warning("Please paste Job Description ⚠️")
                st.stop()
            fit = analyze_job_fit(resume_text, jd)
            verification = verify_resume_with_github(resume_text, github)

            # st.code(fit)
            # st.code(verification)

            st.session_state["hr_fit"] = fit
            st.session_state["verification"] = verification

            #  DISPLAY
            #
            st.markdown("### 📊 Job Fit")
            st.text(fit)

            st.markdown("### 🔍 Verification Report")
            st.text(verification)

        if st.button("📥 Generate HR Report"):

            if not jd.strip():
                st.warning("Paste Job Description first ⚠️")
                st.stop()

            if "hr_fit" not in st.session_state:
                st.warning("Run evaluation first ⚠️")
                st.stop()

            report_text = ""

            # Job Fit
            report_text += "📊 Job Fit\n\n"
            report_text += st.session_state["hr_fit"] + "\n\n"

            # Verification (if exists)
            if "verification" in st.session_state:
                report_text += "🔍 Verification Report\n\n"
                report_text += st.session_state["verification"]

            # Generate PDF
            file_path = generate_pdf_report(report_text, mode="hr")

            # Show download button separately
            with open(file_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download HR PDF",
                    data=f,
                    file_name="HR_Report.pdf",
                    mime="application/pdf",
                )

            st.success("HR Report Ready ✅")

    # # =========================
    # # 🤖 CHAT
    # # =========================
    # elif mode == "🤖 Chat":

    #     if "rag_chain" not in st.session_state:
    #         st.session_state["rag_chain"] = build_rag_chain(temp_path)

    #     q = st.text_input("Ask")

    #     if st.button("Ask"):
    #         res = st.session_state["rag_chain"].invoke({"input": q})
    #         st.write(res["answer"])
            
            
    elif mode == "🎙 Candidate Assistant":

        st.subheader("🎙 Candidate Assistant")

        if "fit" not in st.session_state:

            st.warning(
                "Run Candidate Analysis first"
            )

        else:

            if "assistant_messages" not in st.session_state:
                st.session_state["assistant_messages"] = []

            for msg in st.session_state["assistant_messages"]:

                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
                    
            if "last_intent" in st.session_state:
                st.success(
                    f"🎯 Detected Intent: {st.session_state['last_intent']}"
                )
                
            query = None    
                
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                improve = st.button("📈 Improve Score")

            with col2:
                missing = st.button("🧠 Missing Skills")

            with col3:
                roles = st.button("☁️ Google Roles")

            with col4:
                interview = st.button("🎤 Interview Prep")
            
            if query is None:

                if improve:
                    query = "how do i reach 90+ fit score"

                elif missing:
                    query = "what skills am i missing"

                elif roles:
                    query = "which google roles fit me"

                elif interview:
                    query = "how should i prepare for this role interview"

                else:
                    query = st.chat_input(
                        "Ask about your profile"
                    )
            
            # query = st.chat_input(
            #     "Ask about your profile"
            # )

            if query:

                st.session_state["assistant_messages"].append(
                    {
                        "role": "user",
                        "content": query
                    }
                )

                intent, answer = candidate_assistant(
                    query,
                    resume_text,
                    st.session_state["fit"],
                    st.session_state["assistant_messages"]
                )
                
                st.session_state["last_intent"] = intent

                st.session_state["assistant_messages"].append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )
                
                st.rerun()