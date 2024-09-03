import json
from typing import List, Dict

from fastapi import UploadFile, HTTPException, status
from PyPDF2 import PdfReader


class TextExtractor:

    async def extract_document_text(file: UploadFile) -> str:

        if file.filename.endswith('.pdf'):
            reader = PdfReader(file.file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid File, Context file should be of type PDF!"
            )

        return text

    async def extract_questions(file: UploadFile) -> List[Dict[str, str]]:
        if file.filename.endswith('.json'):
            content = await file.read()
            questions = json.loads(content.decode("utf-8"))
            return questions
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid File, Questions file should be of type Json!"
            )
