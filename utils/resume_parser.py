import PyPDF2

def extract_resume_text(pdf_path):

    text = ""

    with open(pdf_path, 'rb') as file:

        reader = PyPDF2.PdfReader(file)

        print("TOTAL PAGES:",
              len(reader.pages))

        for page in reader.pages:

            page_text = page.extract_text()

            print(page_text)

            if page_text:

                text += page_text

    return text