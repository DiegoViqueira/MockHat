"""HTTP Exception Handler"""

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.i18n.locales.translation_manager import TranslationManager


translator = TranslationManager("en")


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""

    lang = translator.get_lang_from_request(request)
    translator.set_language(lang)
    translated_detail = translator.translate(exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": translated_detail})
