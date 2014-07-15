from HTMLCommons import HTMLCommons
from PTTCommons import PTTCommons

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

	def crawl(self):
		currentCrawledIndex = sIndx
		postID = 0
		postIDString = ""

		for i in range(eIndx-sIndx+1):

			postIDStringPrefix = self.BoardName + "_" + str(currentCrawledIndex)

			# 1st: the URL to establish connection with
			# 2nd: cookies
			response = requests.get(
				PTTCrawler.outerIndexURL.format(board = self.boardName, indexNo = str(currentCrawledIndex)),
				PTTCrawler.COOKIES
				)
			soup = BeautifulSoup(response.text)
			
			for tag in soup.find_all(HTMLCommons.DIVISION,PTTCommons.HtmlClassTags.OUTER_POST):
				try:
					link = str(tag.find_all(HTMLCommons.HYPERLINK))
					link = link.split("\"")
					link = PTTCrawler.innerPostURL.format(postURL = link[1])

					postID += 1
					postIDString = postIdStringPrefix + "_" + postID
					__parsePost(link,postIDString)
				except:
					pass

			sleep(0.2)
			currentCrawledIndex += 1

	def __parsePost(self,postIDString):
		response = requests.get(link,PTTCrawler.COOKIES)
		soupHtmlParser = BeautifulSoup(response.text)

		postToParse = PTTPost(postIDString)
		postParser = PTTPostParser(postToParse, soupHtmlParser)
		
		postParser.parse()
		
		postParser.storeAsJSON("data2.json") 
