import tkinter as tk
from tkinter import ttk
from langchain_ollama import OllamaLLM
import PyPDF2
import os

def read_pdf_file(file_path, page_numbers):
    try:
        # Open the PDF file in read-binary mode
        with open(file_path, 'rb') as file:
            # Create a PyPDF2 reader object
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)

            if page_numbers == "all":
                page_numbers = list(range(num_pages))
            else:
                try:
                    page_numbers = [int(page_number) for page_number in page_numbers.split(',')]
                    page_numbers = [page_number - 1 for page_number in page_numbers]  # Adjust for zero-based indexing
                except ValueError:
                    print("Invalid page numbers. Please enter valid integers separated by commas.")
                    return None

            # Initialize an empty string to store the PDF contents
            pdf_contents = ''

            # Iterate over each page in the PDF
            for page_number in page_numbers:
                if 0 <= page_number < num_pages:
                    pdf_contents += pdf_reader.pages[page_number].extract_text()
                else:
                    print(f"Page {page_number + 1} is out of range.")

            # Return the PDF contents as a string
            return pdf_contents

    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None

def summarize_pdf(file_path, page_numbers):
    pdf_contents = read_pdf_file(file_path, page_numbers)
    if pdf_contents:
        model = OllamaLLM(model="llama3.2")
        results = model.invoke(pdf_contents + "Summarize the data in a understandable manner, while giving atleast 500 words of the page content without ommitting keywords or formulas or definitions")
        return results
    else:
        return "Failed to read PDF file."

def generate_summary():
    file_path = file_entry.get()
    page_numbers = page_entry.get()
    summary = summarize_pdf(file_path, page_numbers)
    summary_text.delete(1.0, tk.END)
    summary_text.insert(tk.END, summary)

# Create the GUI

root = tk.Tk()

root.title("PDF Summarizer")


# Create a custom style

style = ttk.Style()

style.theme_use("clam")  # Use the "clam" theme as a base


# Define a custom style for our widgets

style.configure("RoundedWidget.TFrame", background="#ADD8E6", borderwidth=2, relief="ridge")  # Light blue

style.configure("RoundedWidget.TEntry", fieldbackground="#ffffff", foreground="#000000", borderwidth=2, relief="ridge")

style.configure("RoundedWidget.TButton", foreground="#ffffff", background="#4caf50", borderwidth=2, relief="ridge")


# Create a ttk.Frame as the main container

main_frame = ttk.Frame(root, style="RoundedWidget.TFrame")

main_frame.pack(fill="both", expand=True)


# Create rounded widgets

file_label = ttk.Label(main_frame, text="Enter file path:", style="RoundedWidget.TLabel")

file_label.grid(row=0, column=0, padx=10, pady=10)

file_entry = ttk.Entry(main_frame, width=50, style="RoundedWidget.TEntry")

file_entry.grid(row=0, column=1, padx=10, pady=10)


page_label = ttk.Label(main_frame, text="Enter page numbers (comma-separated, or 'all'):", style="RoundedWidget.TLabel")

page_label.grid(row=1, column=0, padx=10, pady=10)

page_entry = ttk.Entry(main_frame, width=50, style="RoundedWidget.TEntry")

page_entry.grid(row=1, column=1, padx=10, pady=10)


generate_button = ttk.Button(main_frame, text="Generate Summary", command=generate_summary, style="RoundedWidget.TButton")

generate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


summary_text = tk.Text(main_frame, width=80, height=20, bg="#87CEEB", fg="#000000", highlightthickness=0, highlightbackground="#87CEEB")  # Slightly darker blue

summary_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


root.mainloop()