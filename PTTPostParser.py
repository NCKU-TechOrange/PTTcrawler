import re
import json
from PTTCommons import PTTCommons

class PTTPostParser:

	def __init__(self, post, soup):
		self.pttPost = post
		self.contentContainer = soup.find(PTTCommons.HtmlClassTags.CONTENT_CONTAINER)
		self.ipInfoContainer = soup.find(re.compile(PTTCommons.HtmlClassTags.POST_SOURCE_MSG))
		self.pushMsgContainer = soup.find_all(HTMLCommons.DIVISION,PTTCommons.HtmlClassTags.PUSH)

	def parse(self):
		self.__parseAuthor()
		self.__parseTitle()
		self.__parseDate()
		self.__parseIP()
		self.__parseContent()
		self.__parseMsgs()

	def __parseAuthor(self):
		self.pttPost.setAuthor(self.contentContainer.contents[1].contents[0].contents[1].string.replace(' ',''))

	def __parseTitle(self):
		self.pttPost.setTitle(self.contentContainer.contents[1].contents[2].contents[1].string.replace(' ',''))

	def __parseDate(self):
		self.pttPost.setDate(self.contentContainer.contents[1].contents[3].contents[1].string)

	def __parseIP(self):
		try:
			ipAddress = re.search("[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*",str(self.ipInfoContainer)).group()
			self.pttPost.setIP(ipAddress)
		except:
			self.pttPost.IP.setIP("N/A")

	def __parseContent(self):
		# TODO
		# the content parsing is really messy...
		# need a more flexible version
		# For now, using Dien-Yang's methodology
		content = str(self.contentContainer).contents[1]
		content = content.split("</div>")
		content = content[4].split("<span class=\"f2\">※ 發信站: 批踢踢實業坊(ptt.cc),")
		self.pttPost.setContent(content[0].replace(' ','').replace('\n', '').replace('\t', ''))

	def __parseMsgs(self):
		# TODO
		# Same with __parseMsg. Too messy.
		# Perhaps need another class for messages
		# and, what is nu all??
		nu all , likeCount , nlikeCount , neutralCount ,message = 0,0,0,0,0,{}

		for msgs in self.pushMsgContainer:
			totalPushCount += 1
			push_tag = msgs.find(HTMLCommons.SPAN,PTTCommons.HtmlClassTags.PUSH_TAG).string.replace(' ','')
			push_userid = msgs.find(HTMLCommons.SPAN,PTTCommons.HtmlClassTags.PUSH_USERID).string.replace(' ','')
			push_content = msgs.find(HTMLCommons.SPAN,PTTCommons.HtmlClassTags.PUSH_CONTENT).string.replace(' ', '').replace('\n', '').replace('\t', '')
			push_ipdatetime = msgs.find(HTMLCommons.SPAN,PTTCommons.HtmlClassTags.PUSH_TIME).string.replace('\n', '')

		message[totalPushCount]={"PUSH_STATUS":push_tag,"PUSH_AUTHOR":push_userid,"PUSH_CONTENT":push_content,"PUSH_TIME":push_ipdatetime}

		self.pttPost.setMsg(message)

		if push_tag == PTTCommons.PushTagsCH.LIKE:
			likeCount += 1
		elif push_tag == PTTCommons.PushTagsCH.NLIKE:
			nlikeCount += 1
		else:
			neutralCount += 1

		pushCountInfo = {"LIKE":likeCount,"NLIKE":nlikeCount,"NEUTRAL":neutralCount,"TOTAL":totalPushCount}

		self.pttPost.setMsgCountInfo(pushCountInfo)

	def storeAsJSON(self, storePath, message):
		data = {"ID":self.pttPost.postIDString, "AUTHOR":self.pttPost.POST_ID, 
			"TITLE":self.pttPost.TITLE, "DATE":self.pttPost.DATE,
			"IP_ADDR":self.pttPost.IP, "CONTENT":self.pttPost.CONTENT,
			"PUSH":self.pttPost.MSG, "PUSH_COUNT":self.pttPost.MSG_COUNT_INFO}

		JSONData = json.dumps(data,ensure_ascii=False,indent=4,sort_keys=True)+','

		self.__store(JSONData, storePath)

	def __store(self,data,path):
		with open(path, 'a') as file:
			file.write(data)
