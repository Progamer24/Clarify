from langchain_ollama import OllamaLLM
import PyPDF2
import os
def read_pdf_file(file_path):
    try:
        # Open the PDF file in read-binary mode
        with open(file_path, 'rb') as file:
            # Create a PyPDF2 reader object
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            page_numbers_to_print=input(f"There are {num_pages} pages in the PDF. Please enter the page numbers you want to summarize, separated by commas (e.g., 1, 3, 5):")
            try:
                page_numbers_to_print = [int(page_number) for page_number in page_numbers_to_print.split(',')]
                page_numbers_to_print = [page_number - 1 for page_number in page_numbers_to_print]  # Adjust for zero-based indexing
            except ValueError:
                print("Invalid page numbers. Please enter valid integers separated by commas.")
                return None
            # Initialize an empty string to store the PDF contents
            pdf_contents = ''
            
            # Iterate over each page in the PDF
            for page_number in page_numbers_to_print:
                if 0 <= page_number < num_pages:
                    pdf_contents += pdf_reader.pages[page_number].extract_text()
                else:
                    print(f"Page {page_number + 1} is out of range.")

            # Return the PDF contents as a string
            return pdf_contents
    
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None
def read_xl_file():
    fin_file_path=os.path.join("C:", "Users", "arunh", "Downloads", "FinancialReport.pdf")   
    finance_data = read_pdf_file(fin_file_path)
    return finance_data


choice=int(input("Finance or Academics?(1/2)"))
if choice==1:
    ml_content=read_xl_file()
    model = OllamaLLM(model="llama3.2")
    results = model.invoke(ml_content+"Summarise the data in an understandable manner, showing growth or deprecitation in the business over the past quarters")
elif choice==2:
    pdf_file_path = os.path.join("C:", "Users", "arunh", "Downloads", "leph108.pdf")
    pdf_contents = read_pdf_file(pdf_file_path)
    model = OllamaLLM(model="llama3.2")
    results = model.invoke(pdf_contents+"Summarise the data in a understandable manner, while giving atleast 500 words of the page content without ommitting keywords or formulas or definitions")


print(results)