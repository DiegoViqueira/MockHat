"""Scopes"""
from enum import Enum


class Scopes(Enum):
    ADMIN = 'admin'
    STUDENT = 'student'
    TEACHER = 'teacher'
