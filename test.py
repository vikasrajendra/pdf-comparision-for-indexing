import io
import os
import RAKE
import mysql.connector
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

            text_in_list.append(fake_file_handle.getvalue())

            # text = json.dumps(text)

            # print(text)
            # text_in_list = text.split(',')
            # print(text_in_list)
            # print(len(text_in_list))

            # close open handles
            converter.close()
            fake_file_handle.close()

            # using python-rake library to create a rake object with NLTK's stopwords
            r = RAKE.Rake(RAKE.NLTKStopList())

            # extracting keywords using NLTK and rake
            # with the given stopwords for a page which returns keywords and score

            final_text = r.run(text)
            # final_text.append(file_name)
            # final_text.append(idx+1)
            print(len(final_text))
            final_dic = dict(final_text)
            top_10 = nlargest(15, final_dic, key=final_dic.get)
            print(json.dumps(top_10))

            final_keywords = []
            for a in final_text:
                final_keywords.append(a)
                # print(a)
                # for x in final_keywords:
                #     print(x)
            # print(final_keywords)

            # print(final_keywords)

            # for idx1, r1 in enumerate(final_keywords):
            #     # final_keywords = []
            #     for r2 in r1:
            #         final_keywords.append(r2[0])
            #         print(final_keywords)


        # print(keywords_score)

            # print(final_keywords)


def main():
    pdf_path = 'D:\\DummyDir\\files\\cpa-sap-miracle_v1.2.pdf'
    extract_text_by_page(pdf_path)


if __name__ == '__main__':
    main()
