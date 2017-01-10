# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
if os.path.isfile("./output.txt"):
	os.remove("./output.txt")
import re
import unicodedata
import xml.sax
class wikiHandler( xml.sax.ContentHandler ):
   
   def __init__(self):
      self.title = ""
      self.text = ""
      self.id=""
      self.flag=0

   # Call when an element starts
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      self.text = ""
      if tag == "page":
		self.flag=1	
   # Call when an elements ends
   def endElement(self, tag):
      fo = open("output.txt","a")
      if self.CurrentData == "title":
		fo.write("/////////////////////////////////////////Title///////////////////////////////////////"+"\n")
		fo.write(self.title+"\n")
      elif self.CurrentData == "text":
        	info = re.compile(r"{{Infobox.*\n}}",re.DOTALL)
        	infoMatch = info.search(self.text,re.MULTILINE)
		if infoMatch is not None: 
        		infoBox = infoMatch.group()
        		fo.write("///////////////////////////////////INFOBOX///////////////////////////////////"+"\n")
        		fo.write(infoBox+"\n")
        		remInfoBox = re.compile(re.escape(infoBox))
			self.text = remInfoBox.sub('',self.text)  

        	ref  = re.compile(r"(==References==)(.*)(==External links==)",re.DOTALL)
        	refMatch = ref.search(self.text,re.MULTILINE)
		if refMatch is not None:
        		references = refMatch.group(2)   #References Data
        		fo.write("/////////////////////////////////References///////////////////////////////////"+"\n")
        		fo.write(references+ "\n")
			remRef = re.compile(re.escape(references))
			self.text = remRef.sub('',self.text) 
		extLinks = re.compile(r"(==External links==\n)(.*\n)*(\*+.*)")
		extLinksMatch = extLinks.search(self.text)
		if extLinksMatch is not None:
				externalLinks = extLinksMatch.group()
				fo.write("/////////////////////////////////External Links///////////////////////////////////"+"\n")
        			fo.write(externalLinks+ "\n")
				remExt = re.compile(re.escape(externalLinks))
	 			self.text = remExt.sub('',self.text)
	 	category = re.compile(r'\[\[Category:.*]]')
		categoryMatch = category.findall(self.text)
		if len(categoryMatch)!=0:
				fo.write("/////////////////////////////////Categories///////////////////////////////////"+"\n")
				for line in categoryMatch:	
					fo.write(line+"\n")
					lineMatch = re.compile(re.escape(line))
					self.text = lineMatch.sub('',self.text)
		self.text = re.sub(r"\n+","\n",self.text)
		body = self.text
		fo.write("/////////////////////////////////Body///////////////////////////////////"+"\n")
        	fo.write(body+ "\n")
      elif self.CurrentData == "id" and self.flag==1:
      		fo.write("///////////////////////////////////////ID//////////////////////////////////////////"+"\n")
      		fo.write(self.id+"\n")
		self.flag=0


      self.CurrentData = ""

   # Call when a character is read
   def characters(self, content):
      
      if self.CurrentData == "title":
         self.title = content
      elif self.CurrentData == "text":
         self.text += content
      elif self.CurrentData == "id":
      	  self.id =  content

if __name__ == '__main__':
	parser = xml.sax.make_parser()
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)
	Handler = wikiHandler()
   	parser.setContentHandler( Handler )
   	parser.parse("wiki-search-small.xml")
