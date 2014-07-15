import re
import sys
import json
import requests
from time import sleep
from bs4 import BeautifulSoup  
from PTTCrawler import PTTCrawler


boardName = str(sys.argv[1])
startIndex = int(sys.argv[2])
endIndex = int(sys.argv[3])

crawler = PTTCrawler(boardName, startIndex, endIndex)
crawler.crawl()
