from fpdf import FPDF
from io import BytesIO

def clean_text(text):
    replacements = {
        '“': '"', '”': '"',
        '‘': "'", '’': "'",
        '–': '-', '—': '-',
        '…': '...',
        '\u00a0': ' ',
    }
    for src, target in replacements.items():
        text = text.replace(src, target)
    return ''.join(c for c in text if ord(c) < 256)


class PersonaPDF(FPDF):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("Arial", 'B', 14)
        self.set_fill_color(0, 102, 204)  # Blue
        self.set_text_color(255)
        self.cell(0, 12, f"Reddit Persona: u/{self.username}", ln=True, align='C', fill=True)
        self.set_text_color(0)
        self.ln(4)

    def section_title(self, title):
        self.set_font("Arial", 'B', 12)
        self.set_text_color(255, 85, 0)  # Orange
        self.cell(0, 10, title, ln=True)
        self.set_text_color(0)

    def section_body(self, text):
        self.set_font("Arial", size=11)
        self.multi_cell(0, 7, clean_text(text))
        self.ln(4)


def save_persona_as_pdf(persona_text, username):
    pdf = PersonaPDF(username=username)
    pdf.add_page()

    section_keywords = [
        "Age", "Occupation", "Status", "Location", "Archetype",
        "Behaviour", "Habits", "Frustrations", "Motivations",
        "Goals", "Needs", "Personality", "Quotes"
    ]

    lines = persona_text.splitlines()
    sections = {}
    current_section = "Summary"
    sections[current_section] = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        matched = False
        for keyword in section_keywords:
            if keyword.lower() in line.lower() and ':' in line:
                current_section = keyword.title()
                sections[current_section] = []
                matched = True
                break

        if not matched:
            sections[current_section].append(line)

    for title, content_lines in sections.items():
        if content_lines:
            pdf.section_title(title)
            pdf.section_body("\n".join(content_lines))

    # Return as downloadable BytesIO
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    return BytesIO(pdf_bytes)
