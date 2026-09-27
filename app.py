import streamlit as st
import pandas as pd
from resume_parser import extract_text_from_pdf
from ai_analyzer import analyze_resume
from database import save_application, get_applications

st.set_page_config(
    page_title="AI Job Application & Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Job Application & Resume Analyzer")
st.caption("Python • Gemini AI • SQL • NLP • Streamlit")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Resume Analyzer", "Application History"])

if page == "Resume Analyzer":
    st.header("🔍 Resume Analysis")

    col1, col2 = st.columns(2)
    with col1:
        candidate_name = st.text_input("Candidate Name")
    with col2:
        company_name = st.text_input("Company Name")

    job_title = st.text_input("Job Title")
    resume_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
    job_description = st.text_area("Paste Job Description", height=250)

    if st.button("🚀 Analyze Resume", type="primary"):
        if resume_file is None:
            st.error("Please upload your resume PDF.")
            st.stop()

        if not job_description.strip():
            st.error("Please enter the job description.")
            st.stop()

        with st.spinner("Extracting resume and analyzing with Gemini AI..."):
            resume_text = extract_text_from_pdf(resume_file)

            if not resume_text:
                st.error("Could not extract text from the PDF.")
                st.stop()

            result = analyze_resume(resume_text, job_description)

        if "error" in result:
            st.error(result["error"])
            st.stop()

        score = float(result.get("match_score", 0))
        score = max(0, min(100, score))

        st.success("Analysis completed successfully!")
        st.divider()

        st.subheader("📊 Resume Match Score")
        st.metric("ATS-Style Match", f"{score:.0f}%")
        st.progress(int(score))

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Matching Skills")
            skills = result.get("matching_skills", [])
            if skills:
                for skill in skills:
                    st.write(f"✓ {skill}")
            else:
                st.info("No matching skills identified.")

        with col2:
            st.subheader("❌ Missing Skills")
            skills = result.get("missing_skills", [])
            if skills:
                for skill in skills:
                    st.write(f"• {skill}")
            else:
                st.info("No major missing skills identified.")

        st.divider()

        st.subheader("🔑 Recommended Keywords")
        keywords = result.get("recommended_keywords", [])
        st.write(" • ".join(keywords) if keywords else "No additional keywords.")

        st.subheader("💡 Resume Improvement Suggestions")
        suggestions = result.get("suggestions", [])
        for i, suggestion in enumerate(suggestions, 1):
            st.write(f"{i}. {suggestion}")

        if candidate_name and company_name and job_title:
            if save_application(
                candidate_name,
                company_name,
                job_title,
                score,
                skills if 'skills' in locals() else [],
                result.get("missing_skills", []),
                keywords,
                suggestions
            ):
                st.success("Analysis saved to MySQL database.")
            else:
                st.warning("Analysis completed, but database save failed.")
        else:
            st.info("Enter candidate name, company name, and job title to save this analysis.")

elif page == "Application History":
    st.header("📋 Application History")
    applications = get_applications()

    if applications:
        df = pd.DataFrame(applications)
        st.dataframe(df, use_container_width=True)

        st.subheader("📈 Match Score Overview")
        chart_df = df[["company_name", "job_title", "match_score"]].copy()
        chart_df["label"] = chart_df["company_name"] + " - " + chart_df["job_title"]
        st.bar_chart(chart_df.set_index("label")["match_score"])
    else:
        st.info("No application history found.")
