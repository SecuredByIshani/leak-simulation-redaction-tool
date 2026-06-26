from pypdf import PdfReader

reader = PdfReader("sample.pdf")  # Make sure this PDF exists in your folder
print(f"Number of pages: {len(reader.pages)}")

for i, page in enumerate(reader.pages):
    text = page.extract_text()
    print(f"\n--- Page {i+1} ---\n{text}")
