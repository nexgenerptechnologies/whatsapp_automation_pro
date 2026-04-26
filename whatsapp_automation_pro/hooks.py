app_name = "whatsapp_automation_pro"
app_title = "WhatsApp Automation Pro"
app_publisher = "NexGen Enterprises"
app_description = "Advanced WhatsApp Marketing and Automation Connector"
app_email = "nexgenerptechnologies@gmail.com"
app_license = "MIT"

# Document Events
# ----------------
doc_events = {
    "Sales Invoice": {
        "on_submit": "whatsapp_automation_pro.api.send_invoice_notification"
    },
    "Lead": {
        "after_insert": "whatsapp_automation_pro.api.send_welcome_message"
    }
}

# API Endpoints
# --------------
# This allows WhatsJet to send data back to your ERPNext
whitelist_methods = [
    "whatsapp_automation_pro.webhooks.handler"
]
