#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Copyright © 2010 Andrew D. Yates
# All Rights Reserved.
"""Simple HTML form to upload a text PDF and print as text.
"""

import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import pdf_miner_app_engine as pdf_miner


class PDFConverter(webapp.RequestHandler):

  """Convert PDF to Text."""

  def initialize(self, request, response):
    self.write = response.out.write
    super(PDFConverter, self).initialize(request, response)

  def get(self):
    """Display upload HTML form."""
    self.write("<html><body>")
    self.write("<h1>Upload Text PDF</h1>")
    self.write('<form action="%s" method="POST" enctype="multipart/form-data">' \
                 % os.environ['PATH_INFO'])
    self.write('<input type="file" name="pdf_file" />')
    self.write('<input type="submit" value="Submit" />')
    self.write("</form>")
    self.write("</body></html>")

  def post(self):
    """Convert, parse and print text from converted PDF."""
    pdf = self.request.POST['pdf_file'].file.read()
    text = pdf_miner.pdf_to_text(pdf)
    self.write("<html><body>")
    self.write("<h1>Converted PDF Text</h1>")
    self.write("<pre>%s</pre>" % text)
    self.write('<a href="%s">Back to Uploader</a>' % os.environ['PATH_INFO'])
    self.write("</body></html>")
    
    
application = webapp.WSGIApplication(
  [('.*', PDFConverter)],
   debug=True)
    
def main(*args, **kwds):
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
