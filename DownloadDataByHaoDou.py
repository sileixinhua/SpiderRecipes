# 2017年12月6日 00点51分
# 作者：橘子派_司磊
# 爬虫：抓好豆菜谱
# 目标网址：http://www.haodou.com/recipe/30/

from bs4 import BeautifulSoup
import requests
import os
import urllib.request
import re

# C:\Code\Recipes\Data\HaoDou\490
# C:\Code\Recipes\Data\HaoDou\14059_1201100

# 30-490 为页面简单
# 14059-1201100 为复杂
# id = 29
id = 29

# error_number为抓取错误的页面
error_number = 0

while(id <= 490):
	id = id + 1
	try:
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
		url = requests.get('http://www.haodou.com/recipe/'+str(id)+'/', headers=headers)
		print("当前爬取的网址为：" + url.url)
		html_doc = url.text
		soup = BeautifulSoup(html_doc,"lxml")

		recipe_name = soup.find(id="showcover").get('alt')
		print("菜谱的名字为：" + recipe_name)

		img_html = soup.find(id="showcover").get('src')
		print("获取图片为：" + img_html)

		file = open('C:\\Code\\Recipes\\Data\\HaoDou\\490\\' + recipe_name + '.jpg',"wb")
		req = urllib.request.Request(url=img_html, headers=headers) 
		try:
			image = urllib.request.urlopen(req, timeout=10)
			pic = image.read()
		except Exception as e:
			print(e)
			print(recipe_name + "下载失败：" + img_html)

		# 遇到错误，网站反爬虫
		# urllib.error.HTTPError: HTTP Error 403: Forbidden
		# 原因是这里urllib.request方法还需要加入“, headers=headers”
		# 头文件来欺骗，以为我们是客户端访问
		file.write(pic)
		print("图片下载成功")
		file.close()

		drop_html = re.compile(r'<[^>]+>',re.S)

		full_text = []

		recipe_text = soup.find_all('dd')
		for text_str in recipe_text:
			text = drop_html.sub('',str(text_str.find_all('p')))
			text = text.replace("[", "")
			text = text.replace("]", "")
			if text != '':
				print(text)
				full_text.append(text)
	
		# print(recipe_text)
		file = open('C:\\Code\\Recipes\\Data\\HaoDou\\490\\' + recipe_name + '.txt', 'w')
		file.writelines(str(full_text))
		file.close()
	except Exception as e:
		print(e)
		error_number = error_number + 1
	else:
		continue

print("抓取错误的页面数量为：" + str(error_number))

while(id < 1201100):
	id = id + 1
	try:
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
		url = requests.get('http://www.haodou.com/recipe/'+str(id)+'/', headers=headers)
		print("当前爬取的网址为：" + url.url)
		html_doc = url.text
		soup = BeautifulSoup(html_doc,"lxml")

		# http://www.haodou.com/recipe/14059/
		recipe_name = soup.find(id="showcover").get('alt')
		print("菜谱的名字为：" + recipe_name)

		img_html = soup.find(id="showcover").get('src')
		print("获取图片为：" + img_html)

		file = open('C:\\Code\\Recipes\\Data\\HaoDou\\14059_1201100\\' + recipe_name + '.jpg',"wb")
		req = urllib.request.Request(url=img_html, headers=headers) 
		try:
			image = urllib.request.urlopen(req, timeout=10)
			pic = image.read()
		except Exception as e:
			print(e)
			print(recipe_name + "下载失败：" + img_html)
		else:
			continue

		# 遇到错误，网站反爬虫
		# urllib.error.HTTPError: HTTP Error 403: Forbidden
		# 原因是这里urllib.request方法还需要加入“, headers=headers”
		# 头文件来欺骗，以为我们是客户端访问
		file.write(pic)
		print("图片下载成功")
		file.close()	

		# 爬取 简介 full_text_introduction
		full_text_introduction = []
		full_text_introduction = soup.find(id="sintro").get('data')
		print("简介")
		print(full_text_introduction)

		# 爬取 食材 主料 full_text_ingredients
		full_text_ingredients = []
		full_text_ingredients = soup.findAll("li", { "class" : "ingtmgr" })
		print("主料")
		for text in full_text_ingredients:
			print(text.text)

		# 爬取 食材 辅料 full_text_accessories
		full_text_accessories = []
		full_text_accessories = soup.findAll("li", { "class" : "ingtbur" })
		print("辅料")
		for text in full_text_accessories:
			print(text.text)

		# 爬取 步骤 图 full_text_step_img
		full_text_step_img = soup.findAll("img", { "width" : "190" })
		print("图")
		img_number = 0
		for text in full_text_step_img:			
			print(text.get('src'))
			img_html = text.get('src')
			file = open('C:\\Code\\Recipes\\Data\\HaoDou\\14059_1201100\\' + recipe_name + '_' + str(img_number) + '.jpg',"wb")
			req = urllib.request.Request(url=img_html, headers=headers) 
			img_number = img_number + 1
			try:	
				image = urllib.request.urlopen(req, timeout=10)
				pic = image.read()
				file.write(pic)
				print("图片下载成功")
				file.close()
			except Exception as e:
				print(e)
				print(recipe_name + "下载失败：" + img_html)
			# else:
			# 	continue

		# 爬取 步骤 文字 full_text_step_text
		full_text_step_text = []
		full_text_step_text = soup.findAll("p", { "class" : "sstep" })
		print("文字")
		for text in full_text_step_text:
			print(text.text)

		# 爬取 小贴士 full_text_tip
		full_text_tip = []
		full_text_tip = soup.find(id="stips").get('data')
		print("小贴士")
		print(full_text_tip)

		# 全部写入TXT文件
		file = open('C:\\Code\\Recipes\\Data\\HaoDou\\14059_1201100\\' + recipe_name + '.txt', 'w')
		full_text = []
		full_text.append(full_text_introduction)
		full_text.append(full_text_ingredients)
		full_text.append(full_text_accessories)
		full_text.append(full_text_step_text)
		full_text.append(full_text_tip)

		full_text = BeautifulSoup(str(full_text),"lxml").text

		file.writelines(str(full_text))
		file.close()

	except Exception as e:
		print(e)
		error_number = error_number + 1
	else:
		continue
