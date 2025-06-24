import requests
import json
import re
import time
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime
from collections import defaultdict
import os
import textwrap

HIBP_API_KEY = os.getenv("HIBP_API_KEY")

with open("config.json", "r") as f:
    config = json.load(f)
EMAILS = config.get("emails", [])

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        font_path = "DejaVuSans.ttf"
        if os.path.isfile(font_path):
            self.add_font("DejaVu", "", font_path, uni=True)
            self.set_font("DejaVu", "", 12)
        else:
            self.set_font("helvetica", "", 12)
        self.set_left_margin(15)
        self.set_right_margin(15)

    def header(self):
        self.set_font("helvetica", "B", 16)
        self.cell(0, 10, "Dark Web Monitoring Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.set_font("helvetica", "", 12)
        self.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("helvetica", "B", 14)
        self.set_text_color(0, 70, 140)
        self.cell(0, 8, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def breach_entry(self, name, date, dataclasses, description):
        effective_page_width = self.w - self.l_margin - self.r_margin
        self.set_font("helvetica", "B", 12)
        self.cell(0, 6, f"Breach: {name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("helvetica", "", 12)
        self.cell(0, 6, f"Date: {date}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.multi_cell(effective_page_width, 6, f"Leaked Fields: {dataclasses}")
        self.ln(6)

    def list_emails(self, title, emails, breach_map, breach_info):
        effective_page_width = self.w - self.l_margin - self.r_margin
        self.chapter_title(title)
        for email in sorted(emails):
            self.set_font("helvetica", "B", 12)
            self.cell(0, 6, f"- {email}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            if title.startswith("Breached"):
                self.set_font("helvetica", "", 11)
                for breach in breach_map[email]:
                    date = breach_info[breach]["date"]
                    fields = breach_info[breach]["dataclasses"]
                    self.set_x(self.l_margin + 5)
                    self.multi_cell(effective_page_width - 5, 6, f"- {breach} ({date}) - Leaked: {fields}")
                    self.ln(1)
            self.ln(2)

def clean_html(text):
    return re.sub(r'<.*?>', '', text).replace('\n', ' ').strip()

def check_hibp_email(email):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"
    headers = {"hibp-api-key": HIBP_API_KEY, "user-agent": "DarkWebMonitor/1.0"}
    r = requests.get(url, headers=headers)
    print(f"Checking {email} - Status: {r.status_code}")
    if r.status_code == 200:
        print(json.dumps(r.json(), indent=2))
    elif r.status_code == 404:
        print(f"No breach found for {email}")
    else:
        print(f"Error fetching data for {email}: {r.status_code} - {r.text}")
    time.sleep(1.6)
    return r.json() if r.status_code == 200 else []

def generate_report():
    pdf = PDF()
    pdf.add_page()

    unique_breaches = {}
    email_breach_map = defaultdict(list)
    breached_emails = []
    safe_emails = []

    for email in EMAILS:
        hibp = check_hibp_email(email)
        if hibp:
            breached_emails.append(email)
            for item in hibp:
                name = item.get("Name", "Unknown")
                email_breach_map[email].append(name)
                if name not in unique_breaches:
                    unique_breaches[name] = {
                        "date": item.get("BreachDate", "Unknown"),
                        "dataclasses": ", ".join(item.get("DataClasses", [])),
                        "description": clean_html(item.get("Description", ""))
                    }
        else:
            safe_emails.append(email)

    pdf.chapter_title("Summary")
    pdf.list_emails("Breached Emails", breached_emails, email_breach_map, unique_breaches)
    pdf.list_emails("Safe Emails", safe_emails, {}, {})

    pdf.add_page()
    pdf.chapter_title("Breach Descriptions")
    for name, info in unique_breaches.items():
        pdf.breach_entry(name, info["date"], info["dataclasses"], "")

    pdf.output("darkweb_monitoring_report.pdf")
    print("Report saved as darkweb_monitoring_report.pdf")

if __name__ == "__main__":
    generate_report()
