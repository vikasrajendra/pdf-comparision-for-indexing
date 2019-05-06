import io
import os
import RAKE
import mysql.connector
import PyPDF2
from mysql.connector import Error
import json
from heapq import nlargest

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


def extract_text_by_page(pdf_path):
    # extracting the file name from the path
    file_name = os.path.split(pdf_path)[1]
    print(file_name)
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
    text_in_list = []
    with open(pdf_path, 'rb') as fh:
        for idx, page in enumerate(PDFPage.get_pages(fh,
                                                     caching=True,
                                                     check_extractable=True)):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)
            text = fake_file_handle.getvalue()

            # text_in_list.append(fake_file_handle.getvalue())

            # text = json.dumps(text)

            print(text)
            # text_in_list = text.split(',')
            # print(text_in_list)
            # print(len(text_in_list))

            # close open handles
            converter.close()
            fake_file_handle.close()

            # using python-rake library to create a rake object with NLTK's stopwords
            r = RAKE.Rake(RAKE.RanksNLLongStopList())
            max_key_extracted = 15

            # extracting keywords using NLTK and rake
            # with the given stopwords for a page which returns keywords and score

            final_text = r.run(text)
            # final_text.append(file_name)
            # final_text.append(idx+1)
            # print(len(final_text))
            # print(final_text)
            # final_dic = dict(final_text)
            # top_10 = nlargest(15, final_dic, key=final_dic.get)

            sorted_result = sorted(final_text, key=lambda x: x[1], reverse=True)
            sorted_result = sorted_result[:max_key_extracted]

            for keyword, score in sorted_result:
                print(keyword)
            exit(0)


def main():
    pdf_path = 'D:\\DummyDir\\files\\cpa-sap-miracle_v1.2.pdf'
    extract_text_by_page(pdf_path)


if __name__ == '__main__':
    main()
