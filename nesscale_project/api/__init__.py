import frappe
from bs4 import BeautifulSoup
from nesscale_project.api.modules.log import log
from nesscale_project.api.endpoints_loader import get_combined_endpoints


# Get all API endpoints
endpoints = get_combined_endpoints()


def get_allow_guest(type: str):
    endpoint = endpoints.get(type)
    return endpoint.get("allow_guest", False) if endpoint else False


@frappe.whitelist(methods=["POST", "GET", "PUT", "DELETE"], allow_guest=True)
@log()
def v1(type: str, data: dict | None = None, **kwargs):
    """
    data param is for POST and should be converted to Pydantic Model
    """
    endpoint = endpoints.get(type)

    if not endpoint:
        gen_response(404, "Endpoint not found.")
        return

    if frappe.request.method not in endpoint["methods"]:
        gen_response(405, "Method not allowed.")
        return
    allow_guest = get_allow_guest(type)

    if not allow_guest and frappe.session.user == "Guest":
        gen_response(403, "Guest access not allowed for this endpoint.")
        return
    if not data:
        data = dict()

    model = endpoint.get("model")
    if model:
        data = model(**data)

    try:
        if frappe.request.method == "POST":
            frappe.db.begin()

        if not model:
            result = endpoint["function"](**data)
        else:
            result = endpoint["function"](data)

        if frappe.request.method == "POST":
            frappe.db.commit()
    except frappe.AuthenticationError:
        return gen_response(500, frappe.response["message"])
    except Exception as e:
        frappe.log_error(title="Carpenter Error", message=frappe.get_traceback())
        result = str(e)
        return gen_response(500, result)
    finally:
        if frappe.request.method == "POST":
            frappe.db.close()

    gen_response(
        200,
        frappe.response["message"],
        result,
    )
    return


def gen_response(status, message, data=None):
    frappe.response["http_status_code"] = status
    if status == 500:
        frappe.response["message"] = BeautifulSoup(str(message)).get_text()
    else:
        frappe.response["message"] = message
    if data is not None:
        frappe.response["data"] = data