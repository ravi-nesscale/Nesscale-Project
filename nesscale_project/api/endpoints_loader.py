from nesscale_project.api.auth.auth_endpoints import auth_endpoints
# from nesscale_project.api.masters.masters_endpoints import masters_endpoints
from nesscale_project.api.modules.modules_endpoints import *

def get_combined_endpoints():
    """
    Combines all endpoint dictionaries from different modules.
    """
    combined_endpoints = {}
    modules = [
        auth_endpoints,
        # masters_endpoints,
        # auth_endpoints,
        
    ]

    for module in modules:
        combined_endpoints.update(module)

    return combined_endpoints