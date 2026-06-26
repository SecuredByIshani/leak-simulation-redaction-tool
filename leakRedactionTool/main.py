import pikepdf
pdf=pikepdf.Pdf.open('sample.pdf')
pdf_metadata=pdf.docinfo
for key, value in pdf_metadata.items():
    print(f'{key}:{value}')