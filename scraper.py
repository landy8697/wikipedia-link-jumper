import requests # for making standard html requests
from bs4 import BeautifulSoup # magical tool for parsing html data
import json # for parsing data
from pandas import DataFrame as df # premier library for data organization

#URL = "https://en.wikipedia.org/wiki/Special:Random"
URL = "https://en.wikipedia.org/wiki/Scotia,_Nebraska"
page = requests.get(URL)
page.encoding = 'ISO-885901'
soup = BeautifulSoup(page.text, 'html.parser')
#file = open('html.txt', 'w', encoding="utf-8")

ref = soup.find(class_="mw-headline",id="References")
#print(ref)
for element in ref.find_all_next():
    element.decompose()
#file.write(soup.prettify())
#file.close()

links = set()
for link in soup.findAll('a'):
    if (link.get('href') is not None and '/wiki/' in link.get('href') and 'Special' not in link.get('href') and 'File' not in link.get('href') and link.get('class') != 'interlanguage-link interwiki-th mw-list-item' 
    and link.get('class') != 'interlanguage-link-target' and link.get('class')!='extiw'):
        links.add(link.get('href'))
        
        print(link.get('href'), link.getText())
        '''
        if(link.get('class') is not None):
            pass
            print(link.get('href'), link.get('class'))
        '''
        




'''
URL = "https://locations.familydollar.com/id/"
page = requests.get(URL)
page.encoding = 'ISO-885901'
soup = BeautifulSoup(page.text, 'html.parser')

#print(soup.prettify())


dollar_tree_list = soup.find_all(class_ = 'itemlist')
print(type(dollar_tree_list))
#for i in dollar_tree_list[:2]:
#  print(i)


example = dollar_tree_list[2].contents[0] #.contents is a list of one item
print(example)
print(example.attrs)
print(example['href'])


city_hrefs = [] # initialise empty list

for i in dollar_tree_list:
    cont = i.contents[0]
    href = cont['href']
    city_hrefs.append(href)

#  check to be sure all went well
for i in city_hrefs[:3]:
  print(i)

page2 = requests.get(city_hrefs[2]) # again establish a representative example
soup2 = BeautifulSoup(page2.text, 'html.parser')
arco = soup2.find_all(type="application/ld+json")
print(arco[1])

'''

