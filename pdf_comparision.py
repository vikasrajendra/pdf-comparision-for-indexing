from PyPDF2 import PdfFileWriter, PdfFileReader

inputpdf = PdfFileReader(open("D:\\DummyDir\\files\\cpa-sap-miracle_v1.2.pdf", "rb"))

for i in range(inputpdf.numPages):
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    with open("D:\\DummyDir\\files\\document-page%s.pdf" % i, "wb") as outputStream:
        output.write(outputStream)
