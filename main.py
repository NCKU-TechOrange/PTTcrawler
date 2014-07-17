import sys
import requests
from PTTCrawler import PTTCrawler


boardName = str(sys.argv[1])
startIndex = int(sys.argv[2])
endIndex = int(sys.argv[3])
outputPath = str(sys.argv[4])

crawler = PTTCrawler(boardName, startIndex, endIndex)
crawler.crawl(outputPath)
