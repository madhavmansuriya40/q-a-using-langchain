from fastapi import FastAPI, UploadFile, File, status, HTTPException
from fastapi.responses import HTMLResponse
from processor.q_and_a_processor import QAndAProcessor

from schemas.schemas import AnswerResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def ready():
    return """
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Service Status</title>
    </head>
    <body style="width: 100%; text-align: center;">

        <h2>Service Up and Running! 😈</h2>

        <p>
            <a href="https://q-a-using-langchain.onrender.com/docs" style="text-decoration: none; color: blue;">Click here open docs</a>
        </p>

    </body>
    </html>
    """


@app.get("/ready", response_class=HTMLResponse)
def ready():
    return """Service is up and running ! 😈 <p>
            <a href="https://q-a-using-langchain.onrender.com/docs" style="text-decoration: none; color: blue;">Click here open docs</a>
        </p>"""


@app.post("/process", response_model=AnswerResponse, status_code=status.HTTP_200_OK)
async def process_files(questions_file: UploadFile = File(...), document_file: UploadFile = File(...)) -> AnswerResponse:

    try:
        return await QAndAProcessor.process(que_file=questions_file, ref_doc=document_file)
    except HTTPException as ex:
        raise ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Internal server error")
