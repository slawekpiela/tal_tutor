from tal_utils import  convert_pdf_to_txt

pdf_path = 'data/test.pdf'
text = convert_pdf_to_txt(pdf_path)
print(text)
