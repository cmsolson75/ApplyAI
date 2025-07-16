import os
import uuid
import re
from datetime import datetime
from typing import Dict
from app.services.resume_service import ResumeService
from app.services.cover_service import CoverLetterService
from app.embedding_utils import FAISSIndex


class WorkflowRunner:
    """
    Orchestrates resume and cover letter generation.

    Attributes:
        resume_service (ResumeService): Service used for resume generation.
        cover_service (CoverLetterService): Service used for cover letter generation.
        index (FAISSIndex): FAISS index for retrieving cover letter templates.
        resume_context_path (str): Path to base resume context file.
        output_dir (str): Directory to write generated artifacts.
    """

    def __init__(
        self,
        resume_service: ResumeService,
        cover_service: CoverLetterService,
        index: FAISSIndex,
        resume_context_path: str,
        output_dir: str = "outputs",
    ) -> None:
        """
        Initialize WorkflowRunner.

        Args:
            resume_service (ResumeService): Resume generation service instance.
            cover_service (CoverLetterService): Cover letter generation service instance.
            index (FAISSIndex): Index for retrieving context templates.
            resume_context_path (str): Path to the resume context file.
            output_dir (str): Directory where outputs will be stored.
        """
        self.resume_service: ResumeService = resume_service
        self.cover_service: CoverLetterService = cover_service
        self.index: FAISSIndex = index
        self.resume_context_path: str = resume_context_path
        self.output_dir: str = output_dir

    def _clean_name(self, name: str) -> str:
        """
        Normalize a string to a filesystem‑safe identifier.

        Args:
            name (str): Input string.

        Returns:
            str: Normalized lowercase string with non‑alphanumerics replaced by underscores.
        """
        return re.sub(r"[^a-z0-9]+", "_", name.strip().lower()).strip("_")

    def run(self, job_title: str, company: str, job_description: str) -> Dict[str, str]:
        """
        Execute the workflow to produce tailored resume and cover letter.

        Args:
            job_title (str): Target job title.
            company (str): Target company name.
            job_description (str): Full job description text.

        Returns:
            Dict[str, str]: Paths for generated outputs:
                {
                    "output_dir": str,
                    "resume_path": str,
                    "cover_path": str
                }
        """
        date_str: str = datetime.now().strftime("%m_%d_%Y")
        job_clean: str = self._clean_name(job_title)
        company_clean: str = self._clean_name(company)
        run_id: str = str(uuid.uuid4())[:8]

        run_dir: str = os.path.join(self.output_dir, f"{date_str}_{job_clean}_{run_id}")
        os.makedirs(run_dir, exist_ok=True)

        # Read base resume context
        with open(self.resume_context_path, "r", encoding="utf-8") as f:
            resume_full: str = f.read()

        # Generate tailored resume
        tailored_resume: str = self.resume_service.generate(
            job_title, company, job_description, resume_full
        )
        resume_filename: str = f"resume_{job_clean}_{company_clean}_{date_str}.md"
        resume_path: str = os.path.join(run_dir, resume_filename)
        with open(resume_path, "w", encoding="utf-8") as f:
            f.write(tailored_resume)

        # Generate tailored cover letter
        retrieved_contexts = self.index.query(job_description, top_k=3)
        combined_context: str = "\n\n".join(retrieved_contexts)
        tailored_cover: str = self.cover_service.generate(
            job_title, company, job_description, tailored_resume, combined_context
        )
        cover_filename: str = f"cover_letter_{job_clean}_{company_clean}_{date_str}.md"
        cover_path: str = os.path.join(run_dir, cover_filename)
        with open(cover_path, "w", encoding="utf-8") as f:
            f.write(tailored_cover)

        return {
            "output_dir": run_dir,
            "resume_path": resume_path,
            "cover_path": cover_path,
        }