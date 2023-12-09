import redis
from rest_framework import permissions

from datacenterCreatorApi import settings
from dcapi.models import Users

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        ssid = request.COOKIES["session_id"]
        value = session_storage.get(ssid).decode("utf-8")
        if value is None and Users.objects.get(email__iexact=value).is_staff:
            return bool(False)
        return bool(True)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        ssid = request.COOKIES["session_id"]
        value = session_storage.get(ssid).decode("utf-8")
        if value is None and Users.objects.get(email__iexact=value).is_superuser:
            return bool(False)
        return bool(True)


class IsAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        ssid = request.COOKIES["session_id"]
        value = session_storage.get(ssid).decode("utf-8")
        if value is not None and value != "expired":
            return bool(True)
        else:
            return bool(False)
