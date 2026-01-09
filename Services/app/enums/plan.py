"""Plan"""
from enum import Enum


class Plan(Enum):
    """Enum for user plans"""
    FREE = 'free'
    BASIC = 'basic'
    PREMIUM = 'premium'
    BUSINESS = 'business'
    BUSINESS_PRO = 'business_pro'
