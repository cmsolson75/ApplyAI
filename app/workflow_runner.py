import os
import uuid
import re
from datetime import datetime


class WorkflowRunner:
    def __init__(
        self,
        resume_service,
        cover_service,
        index,
        resume_context_path: str,
        output_dir: str = "outputs",
    ):
        self.resume_service = resume_service
        self.cover_service = cover_service
        self.index = index
        self.resume_context_path = resume_context_path
        self.output_dir = output_dir

    def _clean_name(self, name: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", name.strip().lower()).strip("_")

    def run(self, job_title: str, company: str, job_description: str) -> dict:
        date_str = datetime.now().strftime("%m_%d_%Y")
        job_clean = self._clean_name(job_title)
        company_clean = self._clean_name(company)
        run_id = str(uuid.uuid4())[:8]

        run_dir = os.path.join(self.output_dir, f"{date_str}_{job_clean}_{run_id}")
        os.makedirs(run_dir, exist_ok=True)

        # Read full resume context
        with open(self.resume_context_path, "r", encoding="utf-8") as f:
            resume_full = f.read()

        # Generate tailored resume
        tailored_resume = self.resume_service.generate(
            job_title, company, job_description, resume_full
        )
        resume_filename = f"resume_{job_clean}_{company_clean}_{date_str}.md"
        resume_path = os.path.join(run_dir, resume_filename)
        with open(resume_path, "w", encoding="utf-8") as f:
            f.write(tailored_resume)

        # Generate tailored cover letter
        retrieved_contexts = self.index.query(job_description, top_k=3)
        combined_context = "\n\n".join(retrieved_contexts)
        tailored_cover = self.cover_service.generate(
            job_title, company, job_description, tailored_resume, combined_context
        )
        cover_filename = f"cover_letter_{job_clean}_{company_clean}_{date_str}.md"
        cover_path = os.path.join(run_dir, cover_filename)
        with open(cover_path, "w", encoding="utf-8") as f:
            f.write(tailored_cover)

        return {
            "output_dir": run_dir,
            "resume_path": resume_path,
            "cover_path": cover_path,
        }
