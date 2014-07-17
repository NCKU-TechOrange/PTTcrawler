import requests
from bs4 import BeautifulSoup
from time import sleep
from HTMLCommons import HTMLCommons
from PTTCommons import PTTCommons
from PTTPost import PTTPost
from PTTPostParser import PTTPostParser

class PTTCrawler:
	
	COOKIES = {"over18": "1"}
	boardName = ""
	startIndex = 0
	endIndex = 0
	outerIndexURL = "http://www.ptt.cc/bbs/{board}/index{indexNo}.html"
	innerPostURL = "http://www.ptt.cc{postURL}"

	def __init__(self,boardName,sIndx, eIndx):
		self.boardName = boardName
		self.startIndex = sIndx
		self.endIndex = eIndx

	def crawl(self, outputPath):
		print("---- Starting crawl for Board: " + self.boardName + " from index " + str(self.startIndex) + " to " + str(self.endIndex) + " ----")
		currentCrawledIndex = self.startIndex
		postID = 0
		postIDString = ""
		
		for i in range(self.endIndex-self.startIndex+1):

			# 1st: the URL to establish connection with
			# 2nd: cookies
			response = requests.get(
				url=PTTCrawler.outerIndexURL.format(board = self.boardName, indexNo = str(currentCrawledIndex)),
				cookies=PTTCrawler.COOKIES
				)
			soup = BeautifulSoup(response.text)
			
			for tag in soup.find_all(HTMLCommons.DIVISION,PTTCommons.HtmlClassTags.OUTER_POST):
				try:
					link = str(tag.find_all(HTMLCommons.HYPERLINK))
					link = link.split("\"")
					link = PTTCrawler.innerPostURL.format(postURL = link[1])
					postID += 1
					postIDStringPrefix = self.boardName + "_" + str(currentCrawledIndex)
					postIDString = postIDStringPrefix + "_" + str(postID)
					self.__parsePost(link,postIDString, outputPath)
				except:
					pass

			sleep(0.2)
			currentCrawledIndex += 1

	def __parsePost(self,link,postIDString, outputPath):
		print("Parsing post "+postIDString)
		response = requests.get(url=link,cookies=PTTCrawler.COOKIES)
		soupHtmlParser = BeautifulSoup(response.text)

		postToParse = PTTPost(postIDString)
		postParser = PTTPostParser(postToParse, soupHtmlParser)
		
		postParser.parse()
		postParser.storeAsJSON(outputPath) 
