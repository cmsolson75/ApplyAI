from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


class CoverLetterService:
    """
    Service for generating tailored cover letters using a prompt template and a language model.
    """

    def __init__(self, prompt_path: str) -> None:
        """
        Initialize the CoverLetterService.

        Args:
            prompt_path (str): Path to the prompt template file used for generation.
        """
        with open(prompt_path, "r", encoding="utf-8") as f:
            template_str: str = f.read()
        self.prompt: PromptTemplate = PromptTemplate.from_template(template_str)
        self.llm: ChatOpenAI = ChatOpenAI(model="gpt-4.1", temperature=0)

    def generate(
        self,
        job_title: str,
        company: str,
        job_description: str,
        tailored_resume: str,
        retrieved_templates: str,
    ) -> str:
        """
        Generate a tailored cover letter given job details and contextual templates.

        Args:
            job_title (str): Target job title.
            company (str): Target company name.
            job_description (str): Full job description text.
            tailored_resume (str): Resume content generated for this job.
            retrieved_templates (str): Retrieved cover letter templates as context.

        Returns:
            str: Generated cover letter content.
        """
        chain = self.prompt | self.llm
        result = chain.invoke(
            {
                "job_title": job_title,
                "company": company,
                "job_description": job_description,
                "tailored_resume": tailored_resume,
                "retrieved_templates": retrieved_templates,
            }
        )
        return result.content