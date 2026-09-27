from pypdf import PdfReader

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text.strip()
    except Exception as error:
        raise RuntimeError(f"PDF extraction failed: {error}")
