import frappe
from whatsapp_automation_pro.api import send_whatsapp_text, get_settings

@frappe.whitelist(allow_guest=True)
def handler():
    """
    Main webhook receiver for your WhatsApp Automation Platform.
    This handles incoming messages and triggers the chatbot logic.
    """
    # Verify method
    if frappe.request.method != "POST":
        return {"status": "error", "message": "Only POST allowed"}

    # Get JSON data from request
    data = frappe.request.get_json()
    if not data:
        return {"status": "error", "message": "No data received"}

    # Common format for WhatsJet clones: 
    # { "phone": "12345", "message": "hello", "instance_id": "xxx" }
    sender_phone = data.get("phone")
    received_message = data.get("message", "").strip().lower()
    instance_id = data.get("instance_id")

    if not sender_phone or not received_message:
        return {"status": "success", "message": "Ignored: No message or phone"}

    settings = get_settings()
    if not settings.enabled or not settings.chatbot_enabled:
        return {"status": "success", "message": "Chatbot disabled"}

    # Process Chatbot Rules
    for rule in settings.chatbot_rules:
        keyword = rule.keyword.strip().lower()
        should_reply = False

        if rule.match_type == "Exact Match":
            if received_message == keyword:
                should_reply = True
        elif rule.match_type == "Contains":
            if keyword in received_message:
                should_reply = True

        if should_reply:
            # We found a match! Send the reply
            send_whatsapp_text(sender_phone, rule.reply_message, instance_id=instance_id)
            return {"status": "success", "message": "Reply sent"}

    return {"status": "success", "message": "No matching rule found"}
