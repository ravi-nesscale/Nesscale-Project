from nesscale_project.api.modules.project import Project
from .models import *

project_endpoints = {
    "create_project_details": {
        "methods": {"POST"},
        "function": Project().create_project_details,
        "allow_guest": False,
        "model": CreateProjectDetails,
    },
    "get_project_details_list": {
        "methods": {"GET"},
        "function": Project().get_project_details_list,
        "allow_guest": False,
        "model": GetProjectList,
    },
    "get_project_details__by_id": {
        "methods": {"GET"},
        "function": Project().get_project_details__by_id,
        "allow_guest": False,
        "model": GetProjectByID,
    },
    "update_project_details": {
        "methods": {"POST"},
        "function": Project().update_project_details,
        "allow_guest": False,
        "model": UpdateProjectDetails,
    },
    "delete_project": {
        "methods": {"POST"},
        "function": Project().delete_project,
        "allow_guest": False,
        "model": GetProjectByID,
    },
}