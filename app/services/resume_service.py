from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


class ResumeService:
    """
    Service for generating tailored resumes using a prompt template and a language model.
    """

    def __init__(self, prompt_path: str) -> None:
        """
        Initialize the ResumeService.

        Args:
            prompt_path (str): Path to a prompt template file used for generation.
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
        resume_full: str,
    ) -> str:
        """
        Generate a tailored resume based on the provided job context.

        Args:
            job_title (str): Target job title.
            company (str): Target company name.
            job_description (str): Job description text.
            resume_full (str): Full base resume context.

        Returns:
            str: Generated resume content.
        """
        chain = self.prompt | self.llm
        result = chain.invoke(
            {
                "job_title": job_title,
                "company": company,
                "job_description": job_description,
                "resume_full": resume_full,
            }
        )
        return result.content