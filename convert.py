import os
import pandas as pd
from fpdf import FPDF
import pdfplumber
import csv


def pdf_to_csv(pdf_folder, csv_folder):
    os.makedirs(csv_folder, exist_ok=True)

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            csv_path = os.path.join(csv_folder, filename.replace(".pdf", ".csv"))

            with pdfplumber.open(pdf_path) as pdf:
                all_data = []
                for page in pdf.pages:
                    table = page.extract_table()
                    if table:
                        all_data.extend(table)

            if all_data:
                with open(csv_path, "w", newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerows(all_data)


def csv_to_pdf(csv_folder, pdf_folder):
    os.makedirs(pdf_folder, exist_ok=True)

    for filename in os.listdir(csv_folder):
        if filename.endswith(".csv"):
            csv_path = os.path.join(csv_folder, filename)
            pdf_path = os.path.join(pdf_folder, filename.replace(".csv", ".pdf"))

            df = pd.read_csv(csv_path)
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=6)

            col_count = len(df.columns)
            usable_width = pdf.w - 5 

            col_width = min(usable_width / col_count, 60)  
            line_height = 6

            table_width = col_width * col_count
            start_x = (pdf.w - table_width) / 2
            pdf.set_x(start_x)

            for col in df.columns:
                pdf.cell(col_width, line_height, str(col), border=1)
            pdf.ln(line_height)

            for _, row in df.iterrows():
                pdf.set_x(start_x)
                for item in row:
                    text = str(item)
                    if len(text) > 30:
                        text = text[:27] + '...' 
                    pdf.cell(col_width, line_height, text, border=1)
                pdf.ln(line_height)

            pdf.output(pdf_path)




# csv_to_pdf("bank_statements", "pdfs")
# pdf_to_csv("pdfs", "csvs")
