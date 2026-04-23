import streamlit as st
import tempfile
import os
import shutil
import re

from modules.resume import resume_feedback_tool, extract_github_from_resume
from modules.verification import verify_resume_with_github
from modules.jd_analysis import analyze_job_fit
from modules.ats import ats_score
from modules.interview import generate_question, evaluate_answer
from rag_core import extract_full_text, build_rag_chain
from modules.report import generate_pdf_report


st.set_page_config(page_title="AI Hiring Copilot", page_icon="🤖")
st.title("🚀 AI Hiring Copilot")


def reset_vectordb():
    if os.path.exists("faiss_index"):
        shutil.rmtree("faiss_index")


if st.button("🔁 Reset Vector DB"):
    reset_vectordb()
    st.success("Reset Done ✅")


pdf_file = st.file_uploader("Upload Resume", type=["pdf"])

mode = st.radio(
    "Select Mode", ["🧑‍🎓 Candidate", "🧑‍💼 HR", "🤖 Chat"], horizontal=True
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

    # =========================
    # 🧑‍💼 HR
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

            # 🔥 DISPLAY
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

    # =========================
    # 🤖 CHAT
    # =========================
    else:

        if "rag_chain" not in st.session_state:
            st.session_state["rag_chain"] = build_rag_chain(temp_path)

        q = st.text_input("Ask")

        if st.button("Ask"):
            res = st.session_state["rag_chain"].invoke({"input": q})
            st.write(res["answer"])
