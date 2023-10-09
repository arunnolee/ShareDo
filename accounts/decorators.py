from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from .models import UserModel


def isVerifiedClient(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="signin"):
    """
    Decorator for views that checks that the logged in user is verified or not,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.verification.is_verified == True,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator