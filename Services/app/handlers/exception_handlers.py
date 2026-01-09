"""Exception Handlers"""
import traceback
import logging
from pydantic import ValidationError
from fastapi import HTTPException, Request
from pymongo import errors
from starlette import status
from starlette.responses import JSONResponse


async def api_exception_handler(request: Request, exc: Exception):
    """Handle API exceptions."""

    logging.info("APIExceptionHandler: %s", exc)
    content = "".join(traceback.format_exception(
        exc, value=exc, tb=exc.__traceback__))

    if isinstance(exc, ValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()}
        )
    if isinstance(exc, errors.DuplicateKeyError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Document with this combination already exists."}
        )
    if isinstance(exc, errors.PyMongoError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"An error occurred with PyMongo: {content}"}
        )

    # Handle HTTPException for Unauthorized Access
    if isinstance(exc, HTTPException):
        # Handle specifically unauthorized access
        if exc.status_code == status.HTTP_401_UNAUTHORIZED:
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail}
            )
        elif exc.status_code == status.HTTP_403_FORBIDDEN:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "detail": "Forbidden access. You do not have permission for this resource."}
            )

        # Generic HTTPException handler
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": content}
    )
