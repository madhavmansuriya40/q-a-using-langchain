# standard imports
import os
from typing import List

# third-party imports
from fastapi import UploadFile
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate

# local imports
from utils.prompts import CONTEXT_AND_QUESTIONS_PROMPT
from utils.text_extractor import TextExtractor
from utils.text_cleaner import TextCleaner
from schemas.schemas import AnswerSchema, AnswerResponse


class QAndAProcessor:
    async def generate_answers(questions: list, document_text: str) -> List[AnswerSchema]:
        """
            Generate answers for a list of questions based on document text.

            Args:
            - questions: List of questions.
            - document_text: The text extracted from the document.

            Returns:
            - Dictionary mapping questions to their answers.
        """

        # creating LLM object
        repo_id = os.environ.get('MODEL_NAME')
        token = os.environ.get('HUGGINGFACE_API_KEY')

        if not repo_id or not token:
            raise ValueError("Missing environment variables")

        llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            temperature=0.7,
            huggingfacehub_api_token=token,
            max_new_tokens=512
        )

        # creating prompt
        prompt = ChatPromptTemplate.from_template(
            CONTEXT_AND_QUESTIONS_PROMPT
        )

        llm_chain = prompt | llm | StrOutputParser()

        # getting answers from the questions
        question_and_answers = []
        for question in questions:
            try:
                answer = llm_chain.invoke(
                    {"context": document_text, "question": question}
                )
                answer = TextCleaner.clean_string(text=answer)
                question_and_answers.append(AnswerSchema(
                    question=question, answer=answer))
            # TODO: @madhav to add more strict Exceptions
            except Exception as ex:
                print(f"Exception invoking chain for Q:{question} Ex: {ex}")
                raise ex
        return question_and_answers

    async def process(que_file: UploadFile, ref_doc: UploadFile) -> AnswerResponse:
        """
            Process the files and generate answers.

            Args:
            - que_file: UploadFile containing questions.
            - ref_doc: UploadFile containing the reference document.

            Returns:
            - Dictionary of questions and their answers.
        """

        try:
            questions = await TextExtractor.extract_questions(file=que_file)
            document_text = await TextExtractor.extract_document_text(file=ref_doc)
            answers = await QAndAProcessor.generate_answers(questions, document_text)
            return AnswerResponse(answers=answers)
        # TODO: @madhav to add more strict Exceptions
        except Exception as ex:
            raise ex
