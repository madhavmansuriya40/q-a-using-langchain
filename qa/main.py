from fastapi import FastAPI, UploadFile, File, status
from processor import q_and_a_processor

from schemas.schemas import AnswerResponse

app = FastAPI()


@app.get("/ready")
def ready():
    return 'Service Up and Running! 😈'


@app.post("/process", status_code=status.HTTP_200_OK)
async def process_files(questions_file: UploadFile = File(...), document_file: UploadFile = File(...)):

    try:
        return await q_and_a_processor.process(que_file=questions_file, ref_doc=document_file)
    except Exception as ex:
        raise ex
