import PyPDF2
import re
import pandas as pd
import json

pdf_file_path = '1-100.pdf'


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text


cardData = []


def extract_phone_numbers(text):
    # Use regular expressions to find phone numbers
    phone_number_pattern = r'\d{10}'
    phone_numbers = re.findall(phone_number_pattern, text)
    return phone_numbers


def extract_names(text):
    names = re.findall(r'Ship To:\s*(.+)', text)
    return names


if __name__ == '__main__':
    pdf_text = extract_text_from_pdf(pdf_file_path)

    phone_numbers = extract_phone_numbers(pdf_text)
    names = extract_names(pdf_text)

    print("Phone Numbers:", phone_numbers)
    print("Names:", names)
    for index, tableData in enumerate(names):
        cardData.append({"name": tableData, "phone": phone_numbers[index]})
    outputFileName = "scrapedData.json"
    print("cardData", cardData)
    with open(outputFileName, "w") as file:
        json.dump({"data": cardData}, file)
    # Save the scraped data to a csv
    df = pd.DataFrame(cardData)
    df.to_csv('scrapedData.csv', index=False)
    print("Data saved to", cardData)
