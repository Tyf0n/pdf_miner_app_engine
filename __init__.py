#!/usr/bin/python2.5
# -*- coding: utf-8 -*
# Copyright © 2010 Andrew D. Yates
# All Rights Reserved.
"""Integrate PDF miner terminal application into App Engine.

This could be extended to use all of pdfminer's functionality
including XML conversion, table of contents extraction, and embedded
jpeg image extraction.

PDFMiner by Yusuke Shinyama
http://www.unixuser.org/~euske/python/pdfminer
"""
__authors__ = ['"Andrew D. Yates", <andrew.yates@hhmds.com>']


import StringIO

from pdfminer import converter
from pdfminer import layout
from pdfminer import pdfinterp
from pdfminer import pdfparser


def pdf_to_text(pdf):
  """Return extracted text from PDF.

  Warning: This function can be slow... up to 300ms per page
  This function does not perform optical character recognition.

  Args:
    pdf: bytestring of PDF file
  Returns:
    str of text extracted from `pdf` contents.
  """
  # make input and output buffers
  in_buffer = StringIO.StringIO(pdf)
  out_buffer = StringIO.StringIO()

  # configure pdf parser
  parser = pdfparser.PDFParser(in_buffer)
  doc = pdfparser.PDFDocument()
  parser.set_document(doc)
  doc.set_parser(parser)
  doc.initialize(password='')
  rsrcmgr = pdfinterp.PDFResourceManager()
  laparams = layout.LAParams()
  
  # convert pdf to text
  device = converter.TextConverter(
    rsrcmgr, outfp=out_buffer, codec='utf-8', laparams=laparams)
  interpreter = pdfinterp.PDFPageInterpreter(rsrcmgr, device)

  for page in doc.get_pages():
    interpreter.process_page(page)

  return out_buffer.getvalue()
