import frappe
from frappe import _
from frappe.sessions import clear_sessions
from .models import CreateUser

class Auth:
    def __init__(self) -> None:
        self.user = frappe.session.user

    def login(self, usr, pwd):
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(usr, pwd)
        login_manager.post_login()
        self.user = frappe.session.user
        if frappe.response["message"] == "Logged In":
            frappe.response["user"] = self.user
            frappe.response["key_details"] = self.generate_key(login_manager.user)
            
    def logout(self):
        if frappe.session.user == "Guest":
            frappe.throw(_("Login is Required for Logout"))
        frappe.local.login_manager.logout()
        clear_sessions(frappe.session.user, keep_current=False, force=True)
        frappe.response["message"] = _("Successfully logged out.")

    def generate_key(self, user):
        user_details = frappe.get_doc("User", user)
        api_secret = api_key = ""
        if not user_details.api_key and not user_details.api_secret:
            api_secret = frappe.generate_hash(length=15)
            api_key = frappe.generate_hash(length=15)
            user_details.api_key = api_key
            user_details.api_secret = api_secret
            user_details.save(ignore_permissions=True)
        else:
            api_secret = user_details.get_password("api_secret")
            api_key = user_details.get("api_key")
        return {"api_secret": api_secret, "api_key": api_key}
    
    # def create_user(self,data:CreateUser):
    #     doc = frappe.get_doc(doctype="User")
    #     doc.update(data.dict())
    #     doc.insert(ignore_permissions=True)
    #     frappe.response["message"] = _("User Created Successfully")
    #     return doc.username 
    
    def create_user(self, data: CreateUser):
        doc = frappe.get_doc(doctype="User")
        doc.update(data.dict())
        doc.append("roles", {
            "doctype": "Has Role",
            "parentfield": "roles",
            "role": "Employee"
        })
        doc.insert(ignore_permissions=True)
        frappe.response["message"] = _("User Created Successfully")
        return doc.username
