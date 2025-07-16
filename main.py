import streamlit as st
from app.config_loader import load_config
from app.embedding_utils import build_faiss_index
from app.services.resume_service import ResumeService
from app.services.cover_service import CoverLetterService
from app.workflow_runner import WorkflowRunner

cfg = load_config()

resume_service = ResumeService(cfg["resume_prompt"])
cover_service = CoverLetterService(cfg["coverletter_prompt"])
index = build_faiss_index(cfg["cover_letter_context_folder"])

workflow = WorkflowRunner(
    resume_service=resume_service,
    cover_service=cover_service,
    index=index,
    resume_context_path=cfg["resume_context"],
)

st.title("ApplyAI")

job_title = st.text_input("Job Title")
company = st.text_input("Company")
job_description = st.text_area("Job Description", height=300)

if st.button("Generate"):
    if not all([job_title, company, job_description]):
        st.error("All fields are required.")
    else:
        with st.spinner("📝 Generating tailored documents..."):
            result = workflow.run(job_title, company, job_description)

        st.success(f"✅ Generation complete! Files saved in `{result['output_dir']}`")

        st.download_button(
            f"⬇️ Download Tailored Resume ({job_title})",
            data=open(result["resume_path"], "rb").read(),
            file_name=result["resume_path"].split("/")[-1],
        )
        st.download_button(
            f"⬇️ Download Tailored Cover Letter ({job_title})",
            data=open(result["cover_path"], "rb").read(),
            file_name=result["cover_path"].split("/")[-1],
        )
