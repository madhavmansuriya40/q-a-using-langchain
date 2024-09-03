# standard imports
import os
from typing import Dict

# third-party imports
from fastapi import UploadFile
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate

# local imports
from utils.constants import ACCESS_TOKEN, MODEL_NAME
from utils.prompts import CONTEXT_AND_QUESTIONS_PROMPT
from utils.text_extractor import TextExtractor


async def generate_answers(questions: list, document_text: str) -> Dict:
    """
        Input:
        -> questions: List => The list of questions that we want answer for
        -> document_text: str => The text extracted from the PDF or JSON

        This function talks with hugging face hosted models
        and reverts back with the answer from the given context.

        Return's: Dict of questions and answers.
    """

    # creating LLM object
    repo_id = os.environ.get('MODEL_NAME')
    token = os.environ.get('HUGGINGFACE_API_KEY')

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

    # getting answers from the questions
    question_and_answers = {}
    for question in questions:

        llm_chain = prompt | llm | StrOutputParser()
        answer = llm_chain.invoke(
            {"context": document_text, "question": question}
        )

        question_and_answers[question] = answer

    return question_and_answers


async def process(que_file: UploadFile, ref_doc: UploadFile) -> Dict:

    # Extract questions from JSON file
    questions = await TextExtractor.extract_questions(file=que_file)

    # Extract text from the document (PDF or JSON)
    document_text = await TextExtractor.extract_document_text(file=ref_doc)

    # Process questions and generate answers
    answers = await generate_answers(questions, document_text)

    return answers
