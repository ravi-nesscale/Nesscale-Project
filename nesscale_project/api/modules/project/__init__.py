import frappe
from frappe import _
import json
from .models import *
from nesscale_project.api.api_utils import remove_default_fields


class Project:
    def __init__(self) -> None:
        self.user = frappe.session.user

    def create_project_details(self, data: CreateProjectDetails):
        doc = frappe.get_doc(dict(doctype="Project"))
        doc.update(data.dict())
        doc.save()
        frappe.response["message"] = _("Project Details created successfully.")
        frappe.response["name"] = doc.name

    def get_project_details_list(self, data: GetProjectList):
        doc_list = frappe.db.get_list(
            "Project",
            filters=data.filters,
            fields=[
                "name",
                "project_name",
                "project_manager",
                "start_date",
                "end_date",
            ],
            order_by="modified desc",
            start=data.start,
            page_length=data.page_length,
        )

        result = []
        for p in doc_list:
            doc = frappe.get_doc("Project", p.name)
            members = []
            for m in doc.members:   
                members.append({
                    "user": m.user,
                    "role": m.role
                })

            result.append({
                "name": doc.name,
                "project_name": doc.project_name,
                "project_manager": doc.project_manager,
                "start_date": doc.start_date,
                "end_date": doc.end_date,
                "members": members
            })

        frappe.response["message"] = "Project list retrieved successfully"
        frappe.response["data"] = result

    def get_project_details__by_id(self,data:GetProjectByID):
        doc = remove_default_fields(
		    json.loads(frappe.get_doc( "Project",data.name).as_json())
	    )
        frappe.response["message"] = _("Project retrieved successfully")
        return doc

    def update_project_details(self, data: UpdateProjectDetails):
        doc = frappe.get_doc("Project", data.name)
        doc.update(data.dict())
        doc.save()
        frappe.response["message"] = _("Project details updated successfully")
        frappe.response["name"] = doc.name

    def delete_project(self, data: GetProjectByID):
        frappe.delete_doc("Project", data.name)
        frappe.response["message"] = _("Project deleted successfully.")
        frappe.response["name"] = data.name
