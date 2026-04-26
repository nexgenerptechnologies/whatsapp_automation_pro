import frappe
import requests
import json

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

def send_invoice_notification(doc, method=None):
    """
    Hook function called on Sales Invoice submission.
    """
    settings = get_settings()
    if not settings.enabled or not settings.send_on_invoice_submit:
        return

    customer_phone = doc.contact_mobile or doc.mobile_no
    if not customer_phone:
        return

    # Dynamic message using Jinja
    message_template = settings.invoice_message_template or "Hi {customer_name}, your invoice {name} for {total} is ready."
    message = frappe.render_template(message_template, doc)

    send_whatsapp_text(customer_phone, message)

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
