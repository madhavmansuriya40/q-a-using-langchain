from fastapi import FastAPI, UploadFile, File, status, HTTPException
from processor.q_and_a_processor import QAndAProcessor

from schemas.schemas import AnswerResponse

app = FastAPI()


@app.get("/ready")
def ready():
    return 'Service Up and Running! 😈'


@app.post("/process", response_model=AnswerResponse, status_code=status.HTTP_200_OK)
async def process_files(questions_file: UploadFile = File(...), document_file: UploadFile = File(...)) -> AnswerResponse:

    try:
        return await QAndAProcessor.process(que_file=questions_file, ref_doc=document_file)
    except HTTPException as ex:
        raise ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Internal server error")
