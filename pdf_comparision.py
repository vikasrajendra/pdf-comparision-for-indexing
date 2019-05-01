import PyPDF2
import RAKE
import os.path
import mysql.connector
from mysql.connector import Error
import json


def text_extractor(path):
    # opening the pdf file from the destination
    pdf_file_obj = open(path, 'rb')

    # extracting the file name from the path
    file_name = os.path.split(path)[1]
    print(file_name)

    # creating a pdf reader object for the pdf file
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)

    # empty list to store text from each pdf
    pdf_pages = []

    # looping over each page to extract text
    for page in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page)
        # appending the extracted text from each page to a list which will have text from all the pages of the input pdf
        pdf_pages.append(page_obj.extractText())

    # print(pdf_pages)

    try:
        connection = connection = mysql.connector.connect(host='localhost',
                                                          database='pdf_database',
                                                          user='vikas',
                                                          password='Miracle')
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL database... MySQL Server version on ", db_info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("Your connected to - ", record)
    except Error as e:
        print("Error while connecting to MySQL", e)

    # using python-rake library to create a rake object with NLTK's stopwords
    r = RAKE.Rake(RAKE.RanksNLLongStopList())

    # extracting keywords using NLTK and rake with the given stopwords for a page which returns keywords and score

    final_keywords = []
    keywords_score = []

    for p in range(len(pdf_pages)):
        # keywords_score = r.run(pdf_pages[p])
        keywords_score.append(r.run(pdf_pages[p]))
        for idx1, r1 in enumerate(keywords_score):
            final_keywords = []
            for r2 in r1:
                final_keywords.append(r2[0])
        add_keywords = ("INSERT INTO keywords "
                        "(keywords, slide_number, filename)"
                        "VALUES (%s, %s, %s)")
        data_slide_number = idx1+1
        data_filename = file_name
        data_keyword = (json.dumps(final_keywords), data_slide_number, data_filename)

        # insert keywords in table
        cursor.execute(add_keywords, data_keyword)
        connection.commit()


def main():
    path = 'D:\\DummyDir\\files\\AP_Process_Automation.pdf'
    text_extractor(path)


if __name__ == "__main__":
    main()
