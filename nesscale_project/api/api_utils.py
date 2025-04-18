import frappe


def remove_default_fields(data):
    default_fields = {
        "owner",
        "creation",
        "modified",
        "modified_by",
        "docstatus",
        "idx",
        "doctype",
        "links",
    }
    # Remove default fields
    for field in default_fields:
        data.pop(field, None)
    return data


def get_global_defaults():
    return frappe.get_doc("Global Defaults", "Global Defaults")
    