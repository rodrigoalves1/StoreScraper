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
class Product(models.Model):
	url = models.CharField(max_length=300);
	size = models.CharField(max_length=300,blank=True);
	price = models.FloatField(null=True,blank=True);

	def __str__(self):
		return self.url;

	def get_product_name(self):
		return self.url[24:len(self.url)-5];

	def check_product(self):
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
						ans = self.check_size(bsObj)
						if ans:
							send_mail("Product in size available: "+self.get_product_name(),"The following product, in the desired size, is now available \n" + self.url,"rodrigo.alves182@gmail.com", ["raan@cin.ufpe.br"],fail_silently=False );
							self.delete()
					elif self.price != "":
						self.check_price(bsObj)
					else:
						send_mail("Product available: "+self.get_product_name(),"The following product is now available \n" + self.url,"rodrigo.alves182@gmail.com", ["raan@cin.ufpe.br"],fail_silently=False );				
						self.delete()

	def check_size(self,bsObj):
		lista = bsObj.find("ul",{"class":re.compile("^product-sizes-list")})
		disabledLabels = lista.findAll("label",{"class":re.compile("^label-size-disabled")})
		bolean = True
		for label in disabledLabels:
			if label.get_text().strip() == self.size:				
			#if the desired size is in the disabledLabels list it means that it is not available
				bolean = False
		return bolean

	def check_price(self,bsObj):
		price = bsObj.find("span",{"property":re.compile("^gr:hasCurrencyValue")})
		if float(price.get_text().strip().replace(",",".")) < self.price:
			send_mail("Lower price found for product: "+self.get_product_name(),"The following product: \n" + self.url+"\n has now a lower price.","rodrigo.alves182@gmail.com", ["raan@cin.ufpe.br"],fail_silently=False );
			self.price = float(price.get_text().strip().replace(",","."))
			self.save()




