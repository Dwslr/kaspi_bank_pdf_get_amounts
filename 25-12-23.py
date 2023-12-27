import PyPDF2
from re import compile

from datetime import datetime


def kzt_to_rub(path):
    with open(path, "r") as txt:
        content = txt.readlines()

        curr_d = {}

        for line in content:
            line = [elem.strip() for elem in line.split("\t")[:2]]
            date = datetime.strptime(line[0], "%m/%d/%Y")
            week = date.strftime("%W-%Y")
            curr_d[week] = round(float(line[1]), 2)

        return curr_d


curr_d1 = kzt_to_rub("kaspi_bank_DEC_2023/rub-kzt-curr-days.txt")


def open_pdf(path):
    with open(path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)

        # Get the number of pages in the PDF
        pages = len(pdf_reader.pages)
        # print(pages) # 21 pages

        all_lines = []

        # Define a regular expression pattern for the date format
        date_pattern = compile(r"\b\d{2}\.\d{2}\.\d{2}\b")

        # Iterate through all pages
        for page_num in range(pages):
            page = pdf_reader.pages[page_num]

            # Extract text and split into lines
            lines = page.extract_text().splitlines()

            # Add lines to the overall list
            for line in lines:
                if date_pattern.match(line):
                    line = [el.strip() for el in line.split("  ")]
                    line = line[0].split(" ", 1) + line[1:2] + line[4:]
                    # Remove non-numeric characters and replace comma with dot for decimal point
                    line[1] = "".join(
                        char for char in line[1] if char.isdigit() or char in ",."
                    )
                    line[1] = line[1].replace(",", ".")
                    # Convert the cleaned string to a float
                    line[1] = float(line[1])
                    line[0] = datetime.strptime(line[0], "%d.%m.%y")

                    all_lines.append(line)

        accruals = 0
        withdrawals = 0

        for line in all_lines:
            line = line[:4]  # remove extra elements at the end of some lines

            rub = round(line[1] / curr_d1.get(line[0].strftime("%W-%Y")), 2)
            line.append(rub)

            if line[2].lower() == "пополнение":
                accruals += line[4]
            else:
                withdrawals += line[4]

        accruals = round(accruals)
        withdrawals = round(withdrawals)

        return f"Пополнения карты: {accruals} rub\nРасходы по карте: {withdrawals} rub"


res = open_pdf("kaspi_bank_DEC_2023/kaspi_bank_sep22-sep23.pdf")
print(res)
