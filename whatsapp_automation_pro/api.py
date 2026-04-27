import frappe
import requests
import json
from frappe.utils import get_url

def get_settings():
    """Retrieve settings from the 'WhatsApp Automation Settings' DocType."""
    return frappe.get_single("WhatsApp Automation Settings")

@frappe.whitelist()
def send_whatsapp_text(phone, message, instance_id=None):
    """
    Core function to send a text message via WhatsJet API.
    """
    settings = get_settings()
    if not settings.enabled:
        return {"status": "error", "message": "WhatsApp Automation is disabled in settings."}

    # Format phone number (ensure no + or spaces)
    phone = "".join(filter(str.isdigit, phone))
    
    base_url = settings.base_url.strip("/")
    instance = instance_id or settings.default_instance
    
    url = f"{base_url}/api/{settings.vendor_uid}/contact/send-message"
    
    payload = {
        "phone": phone,
        "message": message,
        "instance_id": instance
    }
    
    headers = {
        "Authorization": f"Bearer {settings.get_password('api_token')}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        frappe.log_error(f"WhatsApp Send Error: {str(e)}", "WhatsApp Automation Pro")
        return {"status": "error", "message": str(e)}

def process_dynamic_trigger(doc, method=None):
    """
    Global hook handler for all DocTypes on submit.
    Checks if a trigger is configured in settings.
    """
    settings = get_settings()
    if not settings.enabled:
        return

    # Check for triggers matching this DocType
    for trigger in settings.triggers:
        if trigger.document_type == doc.doctype:
            # Check condition if provided
            if trigger.condition:
                try:
                    if not frappe.safe_eval(trigger.condition, None, {"doc": doc}):
                        continue
                except Exception:
                    frappe.log_error("WhatsApp Condition Error", "WhatsApp Automation Pro")
                    continue
            
            # Get phone number
            phone = doc.get(trigger.phone_field)
            if not phone:
                continue
            
            # Prepare extra context (PDF and Payment Links)
            context = doc.as_dict()
            context['pdf_url'] = get_url(f"/api/method/frappe.utils.print_format.download_pdf?doctype={doc.doctype}&name={doc.name}&format=Standard")
            
            if hasattr(doc, 'get_payment_link'):
                context['payment_url'] = doc.get_payment_link()
            else:
                context['payment_url'] = ""

            # Render and send
            message = frappe.render_template(trigger.message_template, context)
            response = send_whatsapp_text(phone, message)

            # Log the message
            log_whatsapp_message(phone, message, doc.doctype, doc.name, response.get("status"))

def log_whatsapp_message(phone, message, doctype, docname, status):
    """Save a record of the sent message."""
    frappe.get_doc({
        "doctype": "WhatsApp Message Log",
        "receiver_phone": phone,
        "message": message,
        "document_type": doctype,
        "document_name": docname,
        "status": "Sent" if status != "error" else "Failed"
    }).insert(ignore_permissions=True)

def send_invoice_notification(doc, method=None):
    # This is now handled by process_dynamic_trigger if configured in the table
    pass

def send_welcome_message(doc, method=None):
    """
    Hook function called when a new Lead is created.
    """
    settings = get_settings()
    if not settings.enabled or not settings.send_welcome_on_lead:
        return

    if doc.mobile_no:
        message_template = settings.lead_welcome_template or "Welcome {lead_name}! Thank you for your interest."
        message = frappe.render_template(message_template, doc)
        send_whatsapp_text(doc.mobile_no, message)
