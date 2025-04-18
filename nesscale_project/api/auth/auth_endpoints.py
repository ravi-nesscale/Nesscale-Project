from nesscale_project.api.auth import Auth
from .models import CreateUser

auth_endpoints = {
    # authentication end-points
    "login": {"methods": {"POST"}, "function": Auth().login, "allow_guest": True},
    "logout": {"methods": {"POST"}, "function": Auth().logout, "allow_guest": False},
    "create_user": {"methods": {"POST"}, "function": Auth().create_user,"model":CreateUser, "allow_guest": True},
}