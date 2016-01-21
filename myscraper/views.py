from django.shortcuts import render
from django.http import HttpResponse
from myscraper.models import Product
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from bs4 import BeautifulSoup
import time
import threading

# Create your views here.
def index(request):
	try:
		threads = threading.enumerate()
		bol = True
		for t in threads:
			print(t.getName())
			if t.getName() == "Kanui":
				bol = False
		if bol:
			thread = threading.Thread(target=start_scraping)
			thread.daemon = True
			thread.setName("Kanui")
			thread.start()
			thread = threading.Thread(target=keep_it_on)
			thread.daemon = True
			thread.setName("KeepOn")
			thread.start()
			return HttpResponse("Now Scrapping your products at kanui.com.br")
		else:
			return HttpResponse("Kanui scrapper already running")

	except:
		return HttpResponse("An error occurred, please contact the site administrator")
	
def keep_it_on():
	while True:
		print("acorda diabo")
		html = urllib2.urlopen("https://kanuiscraper.herokuapp.com/myscraper/")
		bsObj = BeautifulSoup(html)
		time.sleep(100)
def start_scraping():
	count = 0 
	while True:
			list = Product.objects.all()
			print("iniciou busca kanui")
			print(count)
			print("\n")
			for link in list:
				#print(link.price)
				#print(link.size)
				if link.status == 'e':
					print(link)
					if link.store == 'ka':
						link.kanui_check_product()
					elif link.store == 'ns':
						link.netshoes_check_product()
					elif link.store == 'ce':
						link.centauro_check_product()
			count += 1
			time.sleep(1800)