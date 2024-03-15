import requests
from bs4 import BeautifulSoup	# pip install beautifulsoup4
import bs4

def getHTMLText(url):
	print("getHTMLText")
	try:
		r = requests.get(url, timeout = 60)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except Exception as e:
		return ""

def fillUnivList(ulist, html):
	print("fillUnivList")
	soup = BeautifulSoup(html, "html.parser")
	for tr in soup.find("tbody").children:
		if isinstance(tr, bs4.element.Tag):
			tds = tr('td')
			ulist.append(tds[0].string)

def printUnivList(ulist, num):
	print("printUnivList")
	print("Suc " + str(num))
	for item in ulist:
		print(f"Element: {item}")

def main():
	uinfo_list = []
	print("Mainxx")
	url = "https://www.shanghairanking.cn/rankings/bcur/2023"
	html = getHTMLText(url)
	fillUnivList(uinfo_list, html)
	printUnivList(uinfo_list, 20)

main()





