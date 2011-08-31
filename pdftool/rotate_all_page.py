# -*- coding: utf-8 -*-

from pyPdf import PdfFileWriter, PdfFileReader

def main(filename):
  print "Rotate all page of PDF:", filename

  # expect filename as "*.pdf"
  output_filename = filename.replace(".pdf", "") + "_rotated.pdf"

  original = PdfFileReader(file(filename, 'rb'))
  rotated = PdfFileWriter()
    
  page_num = original.getNumPages()

  for i in xrange(0, page_num):
    rotated.addPage(original.getPage(i).rotateClockwise(180))

  outputStream = file(output_filename, "wb")
  rotated.write(outputStream)
  outputStream.close()
    
    
if __name__ == "__main__":
  main("test.pdf")
  
