"""Classes"""

import logging
from fastapi import APIRouter, status, Query, Depends, HTTPException
from starlette.requests import Request

from app.chains.class_analisys_chain import ClassAnalisysChain
from app.enums.deployment import Deployment
from app.enums.provider import Provider
from app.factories.language_model_factory import LanguageModelFactory
from app.models.class_analisys_result import ClassAnalysisResult
from app.models.classes import Class, ListClass
from app.services.classes_service import ClassesService
from app.services.writing_analytics_service import WritingAnalyticsService
from app.models.metrics.class_metrics import ClassMetrics

router = APIRouter(prefix='/classes', tags=["Classes"])


@router.post("", response_model=Class, status_code=status.HTTP_201_CREATED,
             responses={
                 403: {"description": "You are not allowed to create a class"},
                 400: {"description": "Class already exists"},
                 500: {"description": "Error creating class"},
             })
async def create_class(
    request: Request,
    class_: Class,
    service: ClassesService = Depends(ClassesService)
):
    """Create a new class."""
    return await service.create_class(class_, request.state.user)


@router.get("/{class_id}", response_model=Class,
            responses={
                404: {"description": "Class not found"},
                500: {"description": "Error getting class"},
            })
async def get_class(
    request: Request,
    class_id: str,
    service: ClassesService = Depends(ClassesService)
):
    """Get a class by its ID."""
    return await service.get_class(class_id, request.state.user)


@router.get("", response_model=ListClass,
            responses={
                500: {"description": "Error listing classes"},
            })
async def list_classes(
    request: Request,
    limit: int = Query(10, alias="limit"),
    skip: int = Query(0, alias="offset"),
    is_active: bool = Query(None, alias="is_active"),
    search: str = Query(None, alias="search"),
    service: ClassesService = Depends(ClassesService)
):
    """List all classes of the teacher or admin with pagination."""
    return await service.list_classes(
        user=request.state.user,
        limit=limit,
        skip=skip,
        is_active=is_active,
        search=search
    )


@router.put("/{class_id}", response_model=Class,
            responses={
                404: {"description": "Class not found"},
                403: {"description": "You are not allowed to update this class"},
                500: {"description": "Error updating class"},
            })
async def update_class(
    request: Request,
    class_id: str,
    class_update: Class,
    service: ClassesService = Depends(ClassesService)
):
    """Update an existing class."""
    return await service.update_class(class_id, class_update, request.state.user)


@router.get("/{class_id}/analysis", response_model=ClassAnalysisResult,
            responses={
                404: {"description": "Class not found"},
                500: {"description": "Error getting class analysis"},
            })
async def get_class_analysis(
    request: Request,
    class_id: str,
    service: ClassesService = Depends(ClassesService)
):
    """Get class analysis."""

    user = request.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated")

    messages = await service.get_class_ai_messages(class_id)

    if not messages:
        return ClassAnalysisResult(
            summary="Insufficient information provided to generate a comprehensive analysis.",
        )

    model = LanguageModelFactory.create_model(
        provider=Provider.AZURE,
        deployment=Deployment.GPT_41,
        temperature=0.1,
    )
    chain = ClassAnalisysChain(model=model)

    result, token_usage = await chain.run(messages)

    logging.info("Token usage: %s", token_usage)

    return result


@router.get("/{class_id}/metrics", response_model=ClassMetrics,
            responses={
                404: {"description": "Class not found"},
                500: {"description": "Error getting class metrics"},
            })
async def get_class_metrics(
    request: Request,
    class_id: str,
    service: WritingAnalyticsService = Depends(WritingAnalyticsService)
):
    """Get class metrics."""

    score_histogram = await service.get_score_histogram(class_id)
    score_trends = await service.get_score_trend_over_time(class_id)
    criteria_average = await service.get_criteria_average(class_id)
    class_score_metrics = await service.get_class_score_metrics(class_id)
    student_metrics = await service.get_student_metrics(class_id)

    return ClassMetrics(
        score_histogram=score_histogram,
        score_trends=score_trends,
        criteria_average=criteria_average,
        class_score_metrics=class_score_metrics,
        student_metrics=student_metrics
    )
