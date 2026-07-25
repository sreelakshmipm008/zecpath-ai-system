import pdfplumber
import fitz  # PyMuPDF


def extract_pdf_text(file_path):
    """
    Extract text and tables from a PDF file.
    Uses PyMuPDF as a fallback for better handling of complex layouts.
    """

    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page_number, page in enumerate(pdf.pages, start=1):

            # ---------- Extract normal text ----------
            page_text = page.extract_text()

            # ---------- Fallback for complex layouts ----------
            if not page_text or len(page_text.strip()) < 100:

                doc = fitz.open(file_path)

                page_fitz = doc[page_number - 1]

                # Extract text blocks with coordinates
                blocks = page_fitz.get_text("blocks")

                # Sort blocks from top to bottom, left to right
                blocks.sort(key=lambda block: (block[1], block[0]))

                page_text = ""

                for block in blocks:
                    page_text += block[4] + "\n"

                doc.close()

            if page_text:
                text += page_text + "\n"

            # ---------- Extract tables ----------
            tables = page.extract_tables()

            if tables:

                text += f"\n--- Tables on Page {page_number} ---\n"

                for table in tables:

                    for row in table:

                        cleaned_row = [
                            cell.strip() if cell else ""
                            for cell in row
                        ]

                        text += " | ".join(cleaned_row) + "\n"

                    text += "\n"

    return text