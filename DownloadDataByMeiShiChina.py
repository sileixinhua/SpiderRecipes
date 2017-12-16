# 2017年12月6日 00点51分
# 作者：橘子派_司磊
# 爬虫：抓美食天下菜谱
# 目标网址：http://home.meishichina.com/recipe-1.html

from bs4 import BeautifulSoup
import requests
import os
import urllib.request

# C:\Code\Recipes\Data\MeiShiChina

# 1-363298 页面
id = 1
# error_number为抓取错误的页面
error_number = 0

while(id < 363298):
	id = id + 1
	try:
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
		url = requests.get('http://home.meishichina.com/recipe-'+str(id)+'.html', headers=headers)
		print("当前爬取的网址为："+url.url)
		html_doc = url.text
		soup = BeautifulSoup(html_doc,"lxml")

		# 爬取 菜名 recipe_name
		recipe_name = []
		recipe_name = soup.find(id="recipe_title").get("title")
		print(recipe_name)

		# 爬取 菜图片
		recipe_img = soup.findAll("a", { "class" : "J_photo" })
		for img in recipe_img:
			img_html = img.find("img").get("src")
			print(img_html)
			file = open('C:\\Code\\Recipes\\Data\\MeiShiChina\\' + recipe_name + '.jpg',"wb")
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

		# 爬取 食材明细 
		recipe_material = []
		# tip: 如果 div后面加空格的话 即 "div " ，则结果汉字都变成乱码 且 进行不下去
		# 最终发现输出结果是乱码的原因是使用了get_text()函数，应该用 .text
		recipe_material = soup.findAll("div", { "class" : "recipeCategory_sub_R clear" })
		for material in recipe_material:
			print(material.text)

		# 爬取 评价 recipe_judgement
		recipe_judgement = []
		recipe_judgement = soup.findAll("div", { "class" : "recipeCategory_sub_R mt30 clear" })
		for judgement in recipe_judgement:
			print(judgement.text)

		# 爬取 做法步骤 图片
		# <img alt="鸭脚、鸡爪煲的做法步骤：6" src="http://i3.meishichina.com/attachment/recipe/201007/201007052343079.JPG@!p320"/>
		recipe_step_img = soup.findAll("div", { "class" : "recipeStep_img" })
		number = 0
		for img in recipe_step_img:
			img = img.find_all("img")
			for img_html in img:
				img_html = img_html.get("src")
				print(img_html)

				file = open("C:\\Code\\Recipes\\Data\\MeiShiChina\\" + recipe_name + "_" + str(number) + ".jpg","wb")
				req = urllib.request.Request(url=img_html, headers=headers) 
				number = number + 1
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

		# 爬取 做法步骤 文字 recipe_step_text
		recipe_step_text = []
		recipe_step_text = soup.findAll("div", { "class" : "recipeStep_word" })
		for step_text in recipe_step_text:
			print(step_text.text)

		# 爬取 小窍门 recipe_tip
		recipe_tip = []
		recipe_tip = soup.findAll("div", { "class" : "recipeTip" })
		for tip in recipe_tip:
			print(tip.text)

		# 全部写入TXT文件
		file = open("C:\\Code\\Recipes\\Data\\MeiShiChina\\" + recipe_name + ".txt", "w")
		full_text = []
		full_text.append(recipe_name)
		full_text.append(recipe_material)
		full_text.append(recipe_judgement)
		full_text.append(recipe_step_text)
		full_text.append(recipe_tip)

		full_text = BeautifulSoup(str(full_text),"lxml").text

		file.writelines(str(full_text))
		file.close()

	except Exception as e:
		print(e)
		error_number = error_number + 1
	else:
		continue
