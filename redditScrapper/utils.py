from fpdf import FPDF
from io import BytesIO
def clean_text(text: str) -> str:
    """
    Replace smart quotes and unsupported chars with safe equivalents.
    Returns ASCII-limited string.
    """
    replacements = {
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "–": "-",
        "—": "-",
        "…": "...",
        "\u00a0": " ",
    }
    for src, target in replacements.items():
        text = text.replace(src, target)

    return "".join(ch for ch in text if ord(ch) < 256)


class PersonaPDF(FPDF):
    """Custom PDF class with styled header."""

    def __init__(self, username: str):
        super().__init__()
        self.username = username
        self.set_auto_page_break(auto=True, margin=15)

    def header(self) -> None:
        """Draws page header with username."""
        self.set_font("Arial", "B", 14)
        self.set_fill_color(0, 102, 204)  # blue
        self.set_text_color(255)
        self.cell(0, 12, f"Reddit Persona: u/{self.username}",
                  ln=True, align="C", fill=True)
        self.set_text_color(0)
        self.ln(4)

    def section_title(self, title: str) -> None:
        """Section heading style."""
        self.set_font("Arial", "B", 12)
        self.set_text_color(255, 85, 0)  # orange
        self.cell(0, 10, title, ln=True)
        self.set_text_color(0)

    def section_body(self, text: str) -> None:
        """Section body style."""
        self.set_font("Arial", size=11)
        self.multi_cell(0, 7, clean_text(text))
        self.ln(4)


def save_persona_as_pdf(persona_text: str,
                        username: str) -> BytesIO:
    """
    Build a structured PDF in memory and return BytesIO buffer
    for Streamlit download.
    """
    pdf = PersonaPDF(username=username)
    pdf.add_page()

    keywords = [
        "Age", "Occupation", "Status", "Location", "Archetype",
        "Behaviour", "Habits", "Frustrations", "Motivations",
        "Goals", "Needs", "Personality", "Quotes"
    ]

    sections: dict[str, list[str]] = {"Summary": []}
    current = "Summary"

    for line in persona_text.splitlines():
        line = line.strip()
        if not line:
            continue

        lower = line.lower()
        matched = next((kw for kw in keywords
                       if kw.lower() in lower and ":" in line), None)
        if matched:
            current = matched
            sections[current] = []
        else:
            sections[current].append(line)

    for title, lines in sections.items():
        if lines:
            pdf.section_title(title)
            pdf.section_body("\n".join(lines))

    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    return BytesIO(pdf_bytes)
