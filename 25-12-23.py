import PyPDF2
from re import compile, match, sub


def open_pdf(path):
    with open(path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)

        # Get the number of pages in the PDF
        pages = len(pdf_reader.pages)
        # print(pages) # 21 pages

        # Initialize an empty list to store lines of text
        all_lines = []

        # Define a regular expression pattern for the date format
        date_pattern = compile(r"\b\d{2}\.\d{2}\.\d{2}\b")

        # Iterate through all pages
        for page_num in range(pages):
            page = pdf_reader.pages[page_num]

            # Extract text and split into lines
            lines = page.extract_text().splitlines()

            # Add lines to the overall list
            new_line = []
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

                    all_lines.append(line)

        accruals = 0
        withdrawals = 0

        for line in all_lines:
            if line[2].lower() == "пополнение":
                accruals += line[1]
            else:
                withdrawals += line[1]

        accruals = round(accruals)
        withdrawals = round(withdrawals)

        return f"Пополнения карты: {accruals} КЗТ\nРасходы по карте: {withdrawals} КЗТ"


res = open_pdf("kaspi_bank_DEC_2023/kaspi_bank_sep22-sep23.pdf")
print(res)
