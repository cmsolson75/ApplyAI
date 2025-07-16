from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


class CoverLetterService:
    def __init__(self, prompt_path: str):
        with open(prompt_path, "r", encoding="utf-8") as f:
            template_str = f.read()
        self.prompt = PromptTemplate.from_template(template_str)
        self.llm = ChatOpenAI(model="gpt-4.1", temperature=0)

    def generate(
        self,
        job_title: str,
        company: str,
        job_description: str,
        tailored_resume: str,
        retrieved_templates: str,
    ) -> str:
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
