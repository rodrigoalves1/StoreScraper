from django.db import models
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from bs4 import BeautifulSoup
from django.core.mail import send_mail
import smtplib
import re

# Create your models here.

STATUS_CHOICES = (
	('e', 'Enabled'),
	('d', 'Disabled'),
)
STORE_CHOICES = (
	('ka', 'Kanui'),
	('ns', 'Netshoes'),
	('ce', 'Centauro'),
)


class Product(models.Model):
	url = models.CharField(max_length=300);
	size = models.CharField(max_length=300,blank=True,default="");
	price = models.FloatField(null=True,blank=True,default=None);
	status = models.CharField(max_length=1, choices=STATUS_CHOICES,default='e')
	store = models.CharField(max_length=2, choices=STORE_CHOICES,default='ka')


	def __str__(self):
		return self.url;

	################################################## KANUI #######################################################

	def kanui_get_product_name(self):
		return self.url[24:len(self.url)-5];

	def kanui_check_product(self):
		try:
			html = urllib2.urlopen(self.url)
		except urllib2.HTTPError as e:
			print(e)
		else:
			if html is None:
				print("url not found")
			else:
				bsObj = BeautifulSoup(html)
				lista = bsObj.findAll(text="Produto esgotado")
				#if there is no out-of-stock msg proceed the code to check if desired size is available
				if len(lista) == 0:
					if self.size != "":
						ans = self.kanui_check_size(bsObj)
						if ans:
							send_mail("Product in size available: "+self.kanui_get_product_name(),"The following product, in the desired size, is now available \n" + self.url,"", ["MAIL"],fail_silently=False );
							self.status = 'd'
							self.save()
					elif self.price is not None:
						self.kanui_check_price(bsObj)
					else:
						send_mail("Product available: "+self.kanui_get_product_name(),"The following product is now available \n" + self.url,"", ["MAIL"],fail_silently=False );				
						self.status = 'd'
						self.save()

	def kanui_check_size(self,bsObj):
		lista = bsObj.find("ul",{"class":"product-sizes-list difference"})
		bolean = False
		
		for li in lista.findAll('li'):
			print(li.label)
			if li.label.attrs['class'] != re.compile("^label-size-disabled") and li.label.get_text().strip() == self.size:				
			#iff the desired size is in the disabledLabels list it means that it is not available
				bolean = True
		return bolean

	def kanui_check_price(self,bsObj):
		price = bsObj.find("span",{"property":re.compile("^gr:hasCurrencyValue")})
		if float(price.get_text().strip().replace(",",".")) < self.price:
			send_mail("Lower price found for product: "+self.kanui_get_product_name(),"The following product: \n" + self.url+"\n has now a lower price.","", ["MAIL"],fail_silently=False );
			self.price = float(price.get_text().strip().replace(",","."))
			self.save()

	########################################## NETSHOES ##################################################
	def netshoes_get_product_name(self):
		return self.url[35:];

	def netshoes_check_product(self):
		try:
			html = urllib2.urlopen(self.url)
		except urllib2.HTTPError as e:
			print(e)
		else:
			if html is None:
				print("url not found")
			else:
				bsObj = BeautifulSoup(html)
				lista = bsObj.findAll(text="Produto indisponível")
				#if there is no out-of-stock msg proceed the code to check if desired size is available
				if len(lista) == 0:
					if self.size != "":
						ans = self.netshoes_check_size(bsObj)
						print(ans)
						if ans:
							send_mail("Product in size available: "+self.netshoes_get_product_name(),"The following product, in the desired size, is now available \n" + self.url,"", ["MAIL"],fail_silently=False );
							self.status = 'd'
							self.save()
					elif self.price is not None:
						#print("entrou2")
						self.netshoes_check_price(bsObj)
					else:
						send_mail("Product available: "+self.netshoes_get_product_name(),"The following product is now available \n" + self.url,"", ["MAIL"],fail_silently=False );				
						self.status = 'd'
						self.save()

	def netshoes_check_size(self,bsObj):
		lista = bsObj.find("ul",{"class":re.compile("^product-attr-list"),"data-type":"2"})
		bolean = False
		##print(len(lista))
		
		for li in lista.findAll('li'):
			#print(li.span)
			if li.span.attrs['class'] != "attr-name unavailable" and li.span.get_text().strip() == self.size:				
			#iff the desired size is in the disabledLabels list it means that it is not available
				bolean = True
		return bolean

	def netshoes_check_price(self,bsObj):
		price = bsObj.find("strong",{"class":re.compile("^new-price")})
		#print(float(price.get_text()[3:].strip().replace(",",".")))
		if float(price.get_text()[3:].strip().replace(",",".")) < self.price:
			send_mail("Lower price found for product: "+self.netshoes_get_product_name(),"The following product: \n" + self.url+"\n has now a lower price.","", ["MAIL"],fail_silently=False );
			self.price = float(price.get_text()[3:].strip().replace(",","."))
			self.save()


################################################## CENTAURO #######################################################
	def getParams(self):
		params = self.url.split("?")[1]
		params = params.split('=')
		pairs = zip(params[0::2], params[1::2])
		answer = dict((k,v) for k,v in pairs)
		return answer

	def centauro_get_product_name(self):
		return self.url[28:];

	def centauro_check_product(self):
		try:
			html = urllib2.urlopen(self.url)
		except urllib2.HTTPError as e:
			print(e)
		else:
			if html is None:
				print("url not found")
			else:
				bsObj = BeautifulSoup(html)
				lista = bsObj.findAll(text={"Produto indisponível","Produto esgotado"})
				#if there is no out-of-stock msg proceed the code to check if desired size is available
				if len(lista) == 0:
					if self.size != "":
						ans = self.centauro_check_size(bsObj)
						print(ans)
						if ans:
							send_mail("Product in size available: "+self.centauro_get_product_name(),"The following product, in the desired size, is now available \n" + self.url,"", ["MAIL"],fail_silently=False );
							self.status = 'd'
							self.save()
					elif self.price is not None:
						#print("entrou2")
						self.centauro_check_price(bsObj)
					else:
						send_mail("Product available: "+self.centauro_get_product_name(),"The following product is now available \n" + self.url,"", ["MAIL"],fail_silently=False );				
						self.status = 'd'
						self.save()

	def centauro_check_size(self,bsObj):
		if self.url[len(self.url)-5:] == ".html":
			lista = bsObj.find("ul",{"class":"selector-list text"})
		else:
			params = self.getParams()
			lista = bsObj.find("ul",{"class":"selector-list text","data-ref":params.get("cor")})
		bolean = False
		#print(lista)
		
		for li in lista.findAll('li'):
			#print(li.label.span)
			if li.label.span.get_text().strip() == self.size:				
			#iff the desired size is in the disabledLabels list it means that it is not available
				bolean = True
		return bolean

	def centauro_check_price(self,bsObj):
		price = bsObj.find("span",{"itemprop":re.compile("^price")})
		#print(float(price.get_text()[3:].strip().replace(",",".")))
		if float(price.get_text()[3:].strip().replace(",",".")) < self.price:
			send_mail("Lower price found for product: "+self.centauro_get_product_name(),"The following product: \n" + self.url+"\n has now a lower price.","", ["MAIL"],fail_silently=False );
			self.price = float(price.get_text()[3:].strip().replace(",","."))
			self.save()

