import urllib
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

def tigerSearchPrice(item):
	tigerUrl = " http://www.tigerdirect.ca/applications/SearchTools/search.asp?keywords=" + urllib.quote_plus(item)
	response = urllib2.urlopen(tigerUrl)
	html = response.read()
	soup = BeautifulSoup(html)

	allResults = soup.find('div', class_='resultsWrap')
	products = allResults.find_all('div', class_='product')
	first = products[0]
	priceDiv = first.find('div', class_='salePrice')
	price = priceDiv.contents[1] + "." + priceDiv.contents[2].contents[1]
	return price

def canadaSearchPrice(item):
	canadaUrl = "http://www.canadacomputers.com/advanced_search_result.php?keywords=" + urllib.quote_plus(item)
	response = urllib2.urlopen(canadaUrl)
	html = response.read()
	soup = BeautifulSoup(html)

	allResults = soup.find('table', class_='productListing')
	first = allResults.contents[1]
	relevantRow = first.find_all('td', valign ='middle')[1].contents
	price = 0
	#if object has special price, then row has 4 entries
	#else it has just one entry
	if len(relevantRow) > 1:
		spPriceElem = relevantRow[-1].find('span', class_='productSpecialPrice')
		price = spPriceElem.contents[0]
	else:
		price = relevantRow[0]
	return price.strip()

def ncixSearchPrice(item):
	ncixUrl = "http://search.ncix.com/search?q=" + urllib.quote_plus(item)
	response = urllib2.urlopen(ncixUrl)
	html = response.read()
	soup = BeautifulSoup(html)

	firstResult = soup.find('div', id ='searchresult')
	priceElem = firstResult.find('font', class_='listing')
	price = priceElem.contents[0].contents[0]
	return price.strip()


def amazoncaSearchPrice(item):
	amazoncaUrl = "http://www.amazon.ca/s/?field-keywords=" + urllib.quote_plus(item)
	response = urllib2.urlopen(amazoncaUrl)
	html = response.read()
	soup = BeautifulSoup(html)

	firstResult = soup.find_all('div', id ='rightResultsATF')[0]
	priceElem = firstResult.find('span', class_='a-size-base a-color-price s-price a-text-bold')
	priceFull = priceElem.contents[0]
	price = priceFull.split()[1]
	return price.strip()

def search(searchFn, items):
	results = {}
	for item in items:
		results[item] = searchFn(item)
	return results

def tigerSearchList(items):
	return search(tigerSearchPrice, items)

def canadaSearchList(items):
	return search(canadaSearchPrice, items)

def ncixSearchList(items):
	return search(ncixSearchPrice, items)

def amazoncaSearchList(items):
	return search(amazoncaSearchPrice, items)

def printResults(results):
	for k in results:
		print k + " : " + results[k]

def printChart():
	items = ["4790k", "4690k", "asus gtx 970 strix", "msi z97 gaming 5", "crucial mx100 256gb" ]

	print "Getting prices from tigerdirect"
	tigerPrices = tigerSearchList(items)

	print "Getting prices from canadacomputers"
	canadaPrices = canadaSearchList(items)

	print "Getting prices from ncix"
	ncixPrices = ncixSearchList(items)

	print "Getting prices from Amazon.ca"
	amazoncaPrices = amazoncaSearchList(items)

	print "\n\n"

	print '%20s' % '' + "\tTiger\t\tCanada\t\tNCIX\t\tAmazon.ca"
	for i in items:
		itemName = '%20s' % i
		print itemName + "\t" + tigerPrices[i] + "\t\t" + canadaPrices[i] + "\t\t" + ncixPrices[i] + "\t\t" + amazoncaPrices[i]

def test():
	print tigerSearchList(["4790k", "4690k", "asus gtx 970 strix", "msi z97 gaming 5", "crucial mx100 256gb" ])
	print canadaSearchList(["4790k", "4690k", "asus gtx 970 strix", "msi z97 gaming 5", "crucial mx100 256gb" ])
	print ncixSearchList(["4790k", "4690k", "asus gtx 970 strix", "msi z97 gaming 5", "crucial mx100 256gb" ])
	print amazoncaSearchList(["4790k", "4690k", "asus gtx 970 strix", "msi z97 gaming 5", "crucial mx100 256gb" ])

print "RK's Price comparison tool"
t = datetime.now()
printChart()
tdiff = datetime.now() - t
print "\n\nTime taken: " + str(tdiff)





