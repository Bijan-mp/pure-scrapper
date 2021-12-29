from bs4 import BeautifulSoup
import requests

def  get_soup(url=None, html_doc=None, parser="html.parser"):
     if url is not None:
          print("url in not None")
          html_doc = requests.get(url).text 

          # To prevent this error : UnicodeEncodeError: 'charmap' codec can't encode character '\u011f'
          # if show the error use below line
          # html_doc = html_doc.encode('UTF-8')    

     return BeautifulSoup(html_doc, parser)

# url = "https://www.tutorialspoint.com/index.htm"
# url = "https://www.digikala.com/search/category-mobile-phone/"
# req = requests.get(url)
# soup = BeautifulSoup(req.text, "html.parser")
# print(soup.title)
# tag = soup.html.body
# print(dir(tag))
# print(type(tag))
# print(tag.name)
# tag.name = "Bijoo" #change the <body></body> to <Bijoo></Bijoo>
# print (tag)
# for link in soup.find_all('li'):
#      print(link.tags)

# import bs4
# html = '''<b>tutorialspoint</b>, <i>&web scraping &data science;</i>'''
# soup = bs4.BeautifulSoup(html, 'lxml')
# print(soup)

####
# tutorialsP = BeautifulSoup("<div id='gholi' class='tutorialsP'></div>",'lxml')
# tag2 = tutorialsP.div
# print(tag2['class'])

# The *multi-valued* attributes in beautiful soup are shown as list.
# Multiple-valued attributes like (class, ‘rel’, ‘rev’, ‘headers’, ‘accesskey’ and ‘accept-charset’)
# However, if any attribute contains more than one value but it is not multi-valued (like 'id') attributes
# by any-version of HTML standard, beautiful soup will leave the attribute alone −
# tag2['class'] = ['Online-Learning','myclass']
# tag2['style'] = '2007'
# print(tag2)
# del tag2['style']

# By using ‘get_attribute_list’, you get a value that is always a list, string, irrespective of whether it is a multi-valued or not.
# print(tag2.p.get_attribute_list('id'))

####
# # NavigableString Objects
# # The navigablestring objects are used to represent text within tags, rather than the tags themselves.
# # The navigablestring object is used to represent the """contents""" of a tag. To access the contents, use “.string” with tag.
# soup = get_soup("https://www.digikala.com/search/category-mobile-phone/")
# print(soup.string)
# title_tag = soup.title
# print (title_tag.string)
# # You can replace the string with another string but you can’t edit the existing string.
# title_tag.string.replace_with("Online Learning!")
# print(title_tag)
# # BeautifulSoup is the object created when we try to scrape a web resource. So, it is the complete document which we are trying to scrape.
# print(soup.name) # /> [document]

####
# comments
# soup = BeautifulSoup('<p><!-- Everything inside it is COMMENTS --></p>')
# comment = soup.p.string
# type(comment)
# print(soup.p.prettify())

####
# Navigating by tags
html_doc = """
<html><head><title>Tutorials Point</title></head>
<body>
<p class="title"><b>The Biggest Online Tutorials Library, It's all Free</b></p>
<p class="prog">Top 5 most used Programming Languages are:
<a href="https://www.tutorialspoint.com/java/java_overview.htm" class="prog" id="link1">Java</a>,
<a href="https://www.tutorialspoint.com/cprogramming/index.htm" class="prog" id="link2">C</a>,
<a href="https://www.tutorialspoint.com/python/index.htm" class="prog" id="link3">Python</a>,
<a href="https://www.tutorialspoint.com/javascript/javascript_overview.htm" class="prog" id="link4">JavaScript</a> and
<a href="https://www.tutorialspoint.com/ruby/index.htm" class="prog" id="link5">C</a>;
as per online survey.</p>
<p class="prog">Programming Languages</p>
"""
soup = get_soup(html_doc=html_doc)
# print( soup.head.title)
# print( soup.body)
# print( soup.body.b)
# print( soup.body.a) # get first mached tag. will give you only the first tag by that nam
# print( soup.body.find_all("a"))  # Or print( soup.find_all("a")) 

####
# .contents and .children
# head_tag = soup.head
# print(head_tag)
# print(head_tag.contents) # return a list of contents (tags and strings).Note: all strings between tow independent tag consider as an element.
# print(head_tag.contents[0])
# print(head_tag.contents[0].contents)

# .children : Instead of getting them as a list, use .children generator to access tag’s children 
# for child in soup.children: 
#      print(child)

# .descendant : The .descendants attribute allows you to iterate over all of a tag’s children, recursively −
# for child in soup.descendants:
#      print(child)
# Note : 
# >>> len(list(soup.children)) 
# 2
# >>> len(list(soup.descendants))
# 33

####
# .string ; If the tag has only one child, and that child is a NavigableString, the child is made available as .string −
# However, if a tag contains more than one thing, then it’s not clear what .string should refer to, so .string is defined to None −
head_tag = soup.head
# print(head_tag.contents)
# print(head_tag.string)
# .strings and stripped_strings
# If there’s more than one thing inside a tag, you can still look at just the strings. Use the .strings generator −
# for string in soup.strings:
#      print(string)
# To remove extra whitespace, use .stripped_strings generator −
# for string in soup.stripped_strings:
#      print(string)

### .parent : To access the element’s parent element, use .parent attribute.
title_tag = soup.title
# print(title_tag)
# print(title_tag.parent)
# # The parent of a top-level tag like <html> is the Beautifulsoup object itself −
# print(type(soup.html.parent))
# # The .parent of a Beautifulsoup object is defined as None −
# print(type(soup.html.parent.parent))

# .parents : To iterate over all the parents elements, use .parents attribute.
# link = soup.a
# for parent in link.parents:
#      # print(type(parent))
#      # print(parent)
#      if parent is None:
#           print(parent)
#      else:
#           print(parent.name)

# # .next_sibling and previous_sibling :
# # b and c tag in a same level and they are same parrent. b and c are siblings.
# html_doc = "<a><b>TutorialsPoint</b><c><strong>The Biggest Online Tutorials Library, It's all Free</strong></b></a>"
# sibling_soup = get_soup(html_doc=html_doc)
# print(sibling_soup.prettify)
# print(sibling_soup.b.next_sibling)
# # Note: 
# # >>> print(sibling_soup.b.previous_sibling)
# # None
# # >>> print(sibling_soup.c.next_sibling)
# # None

# Note: whene use bellow code next_sibling dose not return anything.
# """
# <html>
# <body>
#    <a>
#       <b>
#          TutorialsPoint
#       </b>
#       <c>
#          <strong>
#             The Biggest Online Tutorials Library, It's all Free
#          </strong>
#       </c>
#    </a>
# </body>
# </html>
# """

# .next_siblings and .previous_siblings
# To iterate over a tag’s siblings use .next_siblings and .previous_siblings.
# for sibling in soup.a.next_siblings:
#      print(repr(sibling))

# # .next_element and previous_element
# last_a_tag = soup.find("a", id="link5")
# print(last_a_tag)
# # /> <a class="prog" href="https://www.tutorialspoint.com/ruby/index.htm" id="link5">C</a>
# print(last_a_tag.next_sibling)
# # /> ';\n \nas per online survey.'
# print(last_a_tag.next_element)
# # /> 'C'
# print(last_a_tag.previous_element)
# # /> ' and\n
# # .next_elements and .previous_elements
# # We use these iterators to move forward and backward to an element.

#### Searching the tree
markup = get_soup(html_doc='<p>Top Three</p><p><pre>Programming Languages are:</pre></p><p><b>Java, Python, Cplusplus</b></p>')
# string filter
elements = markup.find_all('p')

# regex filter
import re
elements = markup.find_all(re.compile('^p'))

# list filter
elements = markup.find_all(['pre', 'b'])

# True : True will return all tags that it can find, but no strings on their own −

# All the filters we can use with find_all() can be used with find() and other searching methods too like find_parents() or find_siblings().
# find_all(name, attrs, recursive, string, limit, **kwargs)
# find(name, attrs, recursive, string, **kwargs)
# find_parents(name, attrs, string, limit, **kwargs)
# find_parent(name, attrs, string, **kwargs)
for t in elements:
     print(t)

# CSS selectors filters
print(soup.select("p:nth-of-type(1)"))

# ### Encodings
# All HTML or XML documents are written in some specific encoding like ASCII or UTF-8.
#  However, when you load that HTML/XML document into BeautifulSoup, it has been converted to Unicode.


################################
# Trouble Shooting
# except(AttributeError, KeyError) as er:
     # pass

# diagnose()
# Whenever we find any difficulty in understanding what BeautifulSoup does to our document or HTML, 
# simply pass it to the diagnose() function. 
# On passing document file to the diagnose() function, we can show how list of different parser handles the document.
from bs4.diagnose import diagnose

with open("20 Books.html",encoding="utf8") as fp:
   data = fp.read()
   
diagnose(data)
