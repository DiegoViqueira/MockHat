"""Students"""
import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Query
from starlette.requests import Request
from pymongo.errors import DuplicateKeyError

from app.enums.role import Role
from app.models.student import Student
from app.models.student_list import StudentList

router = APIRouter(prefix='/students', tags=["Students"])


@router.post("", response_model=Student,
             responses={
                 400: {"description": "Student already exists"},
                 401: {"description": "Not authenticated"},
                 403: {"description": "You are not allowed to create a student"},
                 500: {"description": "Internal server error"},
             })
async def create_student(
        student: Student,
        request: Request):
    """Create a student."""

    try:
        user = request.state.user

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated")

        if not user.is_admin:
            raise HTTPException(
                status_code=403, detail="You are not allowed to create a student")

        new_student = Student(
            name=student.name,
            last_name=student.last_name,
            account_id=user.id,
            email=student.email
        )

        await new_student.create()

        return new_student

    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=400, detail="Student already exists"
        ) from e
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error("Error creating student: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) from e


@router.patch("/{student_id}", response_model=Student,
              responses={
                  404: {"description": "Student not found"},
                  500: {"description": "Internal server error"},
              })
async def update_student(
        request: Request,
        student_id: str,
        student: Student):
    """Update a student."""

    user = request.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated")

    if not user.is_admin:
        raise HTTPException(
            status_code=403, detail="You are not allowed to update a student")

    updated_student = await Student.get(student_id)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student Not Found.")

    updated_student.name = student.name
    updated_student.last_name = student.last_name
    updated_student.updated_at = datetime.utcnow()
    updated_student.email = student.email
    updated_student.active = student.active

    await Student.save(updated_student)

    return updated_student


@router.get("/actives", response_model=StudentList,
            responses={
                401: {"description": "Not authenticated"},
                403: {"description": "You are not allowed to list students"},
                500: {"description": "Internal server error"},
            })
async def list_active_students(request: Request):
    """List active students."""

    user = request.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated")

    if not user.is_admin:
        raise HTTPException(
            status_code=403, detail="You are not allowed to list students")

    try:
        students = await Student.find({"active": True}).to_list()
        total = await Student.find({"active": True}).count()

        return StudentList(students=students, total=total)

    except Exception as e:
        logging.error("Error listing active students: %s", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error listing active students.") from e


@router.get("", response_model=StudentList,
            responses={
                401: {"description": "Not authenticated"},
                403: {"description": "You are not allowed to list students"},
                500: {"description": "Internal server error"},
            })
async def list_students(request: Request, limit: int = Query(10, alias="limit"), skip: int = Query(0, alias="offset")):
    """List students."""

    user = request.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated")

    if not user.is_admin:
        raise HTTPException(
            status_code=403, detail="You are not allowed to list students")

    try:
        students = await Student.find({"account_id": user.id}).skip(skip).limit(limit).to_list(limit)
        total = await Student.find({"account_id": user.id}).count()

        return StudentList(students=students, total=total)

    except Exception as e:
        logging.error("Error list Students from database: %s", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error list Students.") from e
