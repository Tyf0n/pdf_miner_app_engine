#!/usr/bin/python2.5
# -*- coding: utf-8 -*
# Copyright © 2010 Andrew D. Yates
# All Rights Reserved.
"""Integrate PDF miner terminal application into App Engine.

PDFMiner by Yusuke Shinyama
http://www.unixuser.org/~euske/python/pdfminer
"""
__authors__ = ['"Andrew D. Yates", <andrew.yates@hhmds.com>']


import StringIO

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer import converter
from pdfminer.layout import LAParams


def pdf_to_text(pdf):
  """Return extracted text from PDF.

  Warning: This is slow... about 300ms per page
  This function does not perform optical character recognition.

  Args:
    pdf: bytestring of PDF file
  Returns:
    str of text extracted from `pdf` contents.
  """
  DEVICE = converter.TextConverter
  IN_BUFFER = StringIO.StringIO(pdf)
  OUT_BUFFER = StringIO.StringIO()
  
  parser = PDFParser(IN_BUFFER)
  doc = PDFDocument()
  parser.set_document(doc)
  doc.set_parser(parser)
  doc.initialize(password='')
  rsrcmgr = PDFResourceManager()
  laparams = LAParams()
  device = DEVICE(rsrcmgr, outfp=OUT_BUFFER, codec='utf-8', laparams=laparams)
  interpreter = PDFPageInterpreter(rsrcmgr, device)

  for page in doc.get_pages():
    interpreter.process_page(page)

  return OUT_BUFFER.getvalue()

