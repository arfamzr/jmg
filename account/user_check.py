from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from functools import wraps


def is_manager(user):
    return user.is_manager


def is_jmg_state(user):
    return user.is_jmg_state


def is_jmg_state_admin(user):
    return user.is_jmg_state_admin


def is_jmg_hq(user):
    return user.is_jmg_hq


def is_super_admin(user):
    return user.is_super_admin


def user_is_manager():

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if is_manager(request.user):
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return _wrapped_view
    return decorator


def user_is_jmg_state():

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if is_jmg_state(request.user):
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return _wrapped_view
    return decorator


def user_is_jmg_state_admin():

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if is_jmg_state_admin(request.user):
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return _wrapped_view
    return decorator


def user_is_jmg_hq():

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if is_jmg_hq(request.user):
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return _wrapped_view
    return decorator


def user_is_super_admin():

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if is_super_admin(request.user):
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return _wrapped_view
    return decorator


class UserIsManagerMixin(UserPassesTestMixin):
    def test_func(self):
        return is_manager(self.request.user)


class UserIsJMGStateMixin(UserPassesTestMixin):
    def test_func(self):
        return is_jmg_state(self.request.user)


class UserIsJMGStateAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return is_jmg_state_admin(self.request.user)


class UserIsJMGHQMixin(UserPassesTestMixin):
    def test_func(self):
        return is_jmg_hq(self.request.user)


class UserIsSuperAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return is_super_admin(self.request.user)
