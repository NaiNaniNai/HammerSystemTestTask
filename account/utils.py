import string

from django.utils.crypto import get_random_string


def generate_referral_code() -> str:
    """Generate random referral code, which consist of digits, letters in upper and lower case"""

    return get_random_string(
        length=6,
        allowed_chars=string.digits + string.ascii_uppercase + string.ascii_lowercase,
    )


def generate_confirm_code() -> str:
    """Generate random confirmation code SMS, which consist of digits, for login"""
    return get_random_string(length=4, allowed_chars=string.digits)
