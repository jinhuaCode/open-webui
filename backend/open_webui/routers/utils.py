import black
import markdown

from open_webui.models.chats import ChatTitleMessagesForm
from open_webui.config import DATA_DIR, ENABLE_ADMIN_EXPORT
from open_webui.constants import ERROR_MESSAGES
<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel
from starlette.responses import FileResponse


from open_webui.utils.misc import get_gravatar_url
from open_webui.utils.pdf_generator import PDFGenerator
from open_webui.utils.auth import get_admin_user, get_verified_user
from open_webui.utils.code_interpreter import execute_code_jupyter

=======
from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel
from starlette.responses import FileResponse
from open_webui.utils.misc import get_gravatar_url
from open_webui.utils.pdf_generator import PDFGenerator
from open_webui.utils.auth import get_admin_user
>>>>>>> dfef03c8e (同步远程)

router = APIRouter()


@router.get("/gravatar")
<<<<<<< HEAD
async def get_gravatar(email: str, user=Depends(get_verified_user)):
    return get_gravatar_url(email)


class CodeForm(BaseModel):
=======
async def get_gravatar(
    email: str,
):
    return get_gravatar_url(email)


class CodeFormatRequest(BaseModel):
>>>>>>> dfef03c8e (同步远程)
    code: str


@router.post("/code/format")
<<<<<<< HEAD
async def format_code(form_data: CodeForm, user=Depends(get_verified_user)):
    try:
        formatted_code = black.format_str(form_data.code, mode=black.Mode())
        return {"code": formatted_code}
    except black.NothingChanged:
        return {"code": form_data.code}
=======
async def format_code(request: CodeFormatRequest):
    try:
        formatted_code = black.format_str(request.code, mode=black.Mode())
        return {"code": formatted_code}
    except black.NothingChanged:
        return {"code": request.code}
>>>>>>> dfef03c8e (同步远程)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


<<<<<<< HEAD
@router.post("/code/execute")
async def execute_code(
    request: Request, form_data: CodeForm, user=Depends(get_verified_user)
):
    if request.app.state.config.CODE_EXECUTION_ENGINE == "jupyter":
        output = await execute_code_jupyter(
            request.app.state.config.CODE_EXECUTION_JUPYTER_URL,
            form_data.code,
            (
                request.app.state.config.CODE_EXECUTION_JUPYTER_AUTH_TOKEN
                if request.app.state.config.CODE_EXECUTION_JUPYTER_AUTH == "token"
                else None
            ),
            (
                request.app.state.config.CODE_EXECUTION_JUPYTER_AUTH_PASSWORD
                if request.app.state.config.CODE_EXECUTION_JUPYTER_AUTH == "password"
                else None
            ),
            request.app.state.config.CODE_EXECUTION_JUPYTER_TIMEOUT,
        )

        return output
    else:
        raise HTTPException(
            status_code=400,
            detail="Code execution engine not supported",
        )


=======
>>>>>>> dfef03c8e (同步远程)
class MarkdownForm(BaseModel):
    md: str


@router.post("/markdown")
async def get_html_from_markdown(
<<<<<<< HEAD
    form_data: MarkdownForm, user=Depends(get_verified_user)
=======
    form_data: MarkdownForm,
>>>>>>> dfef03c8e (同步远程)
):
    return {"html": markdown.markdown(form_data.md)}


class ChatForm(BaseModel):
    title: str
    messages: list[dict]


@router.post("/pdf")
async def download_chat_as_pdf(
<<<<<<< HEAD
    form_data: ChatTitleMessagesForm, user=Depends(get_verified_user)
=======
    form_data: ChatTitleMessagesForm,
>>>>>>> dfef03c8e (同步远程)
):
    try:
        pdf_bytes = PDFGenerator(form_data).generate_chat_pdf()

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment;filename=chat.pdf"},
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/db/download")
async def download_db(user=Depends(get_admin_user)):
    if not ENABLE_ADMIN_EXPORT:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )
    from open_webui.internal.db import engine

    if engine.name != "sqlite":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DB_NOT_SQLITE,
        )
    return FileResponse(
        engine.url.database,
        media_type="application/octet-stream",
        filename="webui.db",
    )


@router.get("/litellm/config")
async def download_litellm_config_yaml(user=Depends(get_admin_user)):
    return FileResponse(
        f"{DATA_DIR}/litellm/config.yaml",
        media_type="application/octet-stream",
        filename="config.yaml",
    )
