# WhatsApp Automation Pro 🚀

**Advanced WhatsApp Marketing & Automation Connector for Frappe / ERPNext**

Connect your ERPNext site directly to your **WhatsApp Automation Platform** instance and automate your customer communications instantly.

---

## 🌟 Key Features

- ✅ **Automated Notifications**: Send professional WhatsApp messages on Sales Invoice submission.
- ✅ **Lead Engagement**: Instantly send a welcome message to new leads.
- ✅ **Dynamic Templates**: Support for Jinja templates to personalize messages with customer data.
- ✅ **WhatsApp Integration**: Seamlessly connects to your custom WhatsApp Marketing Platform instance.
- ✅ **Secure Authentication**: Encrypted API token storage.
- ✅ **Marketplace Ready**: Built with Frappe's best practices for security and performance.

---

## 🚀 Installation

### Using Bench

```bash
bench get-app https://github.com/nexgenerptechnologies/whatsapp_automation_pro.git
bench install-app whatsapp_automation_pro
```

---

## ⚙️ Setup & Configuration

1. **Get your API Credentials**:
   - Log in to your WhatsApp Automation Platform dashboard (e.g., `https://wasender.digitalsoftech.com`).
   - Go to **Settings > API & Webhooks**.
   - Copy your **Vendor UID** and **API Token**.

2. **Configure ERPNext**:
   - In ERPNext, search for **WhatsApp Automation Settings**.
   - Paste your **Base URL**, **Vendor UID**, and **API Token**.
   - Toggle **Enabled** and save.

3. **Customize Templates**:
   - Enable "Send on Sales Invoice Submit".
   - Customize the message using tags like `{customer_name}` or `{name}`.

---

## 🛡️ License

This project is licensed under the **MIT License**.

---

## 🤝 Support

For support, please contact [nexgenerptechnologies@gmail.com](mailto:nexgenerptechnologies@gmail.com) or visit [nexgenerp.com](https://nexgenerp.com).

*Built with ❤️ by NexGen Enterprises*
