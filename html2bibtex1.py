# python parser for converting a very specific publications page from html to bibtex 
# author : Eleni Kaxiras
# thanks Beautiful Soup!

from bs4 import BeautifulSoup
from sys import argv
import re

filename = argv[1]
soup = BeautifulSoup(open(filename))
soup.prettify()

articles = soup.find_all('li')
for article in articles:
	try:
		#check if there exists an a tag
		link = article.a
		url = link['href']
		url = url.replace('Papers/','') 
		url = url.replace('2011/','') 
		title = link.string.strip()
		title = title.replace('\n','')  # remove '\n' 
		title = title.replace('\"','')  # remove '"' 
		# find <i> tags
		journal = article.i
		journal_name = journal.string
		journal_name = journal_name.replace('\n','')  # remove '\n' only
		# find <b> tags
		volume = article.b
		volume_number = volume.string.strip()
		volume_number = volume_number.replace(',','')  # remove ',' 
		# find author 
		author = article.contents[4].strip()
		author = author.replace('\n','')  # remove '\n' only
		author = re.sub(r',$','',author)  # remove , at end of line 
		author = author.replace(',',' and ')  # remove '\n' only
		author = re.sub(r'and\s+and','and ',author)  # remove double and 
		# find year
		try:
			year = article.contents[8].string.strip()
		except:
			year = article.contents[7].string.strip()
			#continue
		year = year.replace('\n','')
		year = year.replace(',','')
		year = year.strip()
#		print year
		pages = re.search(r'\d*', year)
		if pages:
			pages = pages.group()
#			print pages	
		else:
			print "no match.."
		year = re.search(r'\(\d{4}\)', year)
		year = year.group()
		year = year.replace('(','')  # remove parentesis 
		year = year.replace(')','')  # remove parentesis 
		number = article.parent.get('start')
		print "@article {%s," %number
		print "\ttitle={%s}," %title
		print "\tjournal={%s}," %journal_name
		print "\tvolume={%s}," %volume_number
		print "\tyear={%s}," %year
		print "\tpages={%s}," %pages
		print "\turl={http://scholar.harvard.edu/files/efthimios_kaxiras/files/%s}," %url
		print "\tauthor={%s}," %author
		print "}" 

	except:	
		print "oops"
		continue 
		
 

