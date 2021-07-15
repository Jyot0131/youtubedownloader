import requests
import sys
import os
from datetime import datetime
import re

def new():
	file_url = str(input("Give Youtube Video url : "))
	r = requests.get(file_url, stream = True)
	with open("data.txt" ,"wb") as pdf:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				pdf.write(chunk)
	r.close()

	links = {}
	substr = ["\"itag\":17" , "\"itag\":18" , "\"itag\":22" , "\"itag\":37" , "\"itag\":38"]
	for i in substr:
		with open("data.txt","r") as fp:
			for line in fp:
				start = line.find(i)
				if start != -1:
					tempnum = start+17
					tempstr = line[tempnum]
					while tempstr != "\"" :
						tempnum += 1
						tempstr = line[tempnum]
					link = line[start+17:tempnum]
					link = link.replace("\\u0026","&")
					#print(i)
					#print(link)
					print()
					if i == "\"itag\":17":
						links.update(p144 = link)
					elif i == "\"itag\":18":
						links.update(p360 = link)
					elif i == "\"itag\":22":
						links.update(p720 = link)
					elif i == "\"itag\":37":
						links.update(p1080 = link)
					elif i == "\"itag\":38":
						links.update(p3072 = link)
	substr1 = "<title>"
	substr2 = "</title>"
	start = end = -1

	with open("data.txt","r") as fp:
		for line in fp:
			if line.find(substr1) != -1:
				start = line.find(substr1)
			if line.find(substr2) != -1:
				end = line.find(substr2)
			if start != -1 and end != -1:
				break
	os.remove("data.txt")
	title = line[start+7:end-10]
	title = re.sub(r'[^a-zA-Z0-9 ]',r'',title)
	title = title.strip()
	title = re.sub(' +', ' ', title)
	print(title)
	if os.path.isfile(title+".mp4") == True :
		print()
		print("File alreay downloaded, try resume downloading (option 2) if it was interrupted !")
		sys.exit()

	print()
	print("--- Available Resolutions ---")
	for resol in links:
		print(resol[1:]+str("p"))
	print()
	res = str(input("Give video resolution you want to download : "))
	
	if "144p" in res:
		link = (links["p144"])
	elif "360p" in res:
		link = (links["p360"])
	elif "720p" in res:
		link = (links["p720"])
	elif "1080p" in res:
		link = (links["p1080"])
	elif "3072p" in res:
		link = (links["p3072"])
	else:
		print("Invalid Resolution !")
		sys.exit()

	r = requests.get(link, stream=True)
	total = int(r.headers.get('content-length'))
	print("\n---Video size---")
	print(total/1024,"KiB")
	print(total/1024/1024,"MiB")
	print(total/1024/1024/1024,"GiB")
	r.close()
		
	ans = str(input("\nDo You Want To Download The Video ? Y/y/N/n : "))
	
	if ans in ["N","n"]:
		print("Abort !")
	elif ans in ["Y","y"]:
		vid_name = title + ".mp4"
		print("\nHang on, Downloading the %s file" % vid_name)
		downloaded = 0
		print()
		with open("youtube_logs.txt","a") as fi:
			fi.write(file_url+"\n")
			fi.write(res+"\n")
			fi.write(datetime.now().strftime('%d-%m-%Y %H:%M:%S')+"\n\n")
		r = requests.get(link, stream = True)
		with open(vid_name ,"wb") as pdf:
			for chunk in r.iter_content(chunk_size=1024*8):
				downloaded += len(chunk)
				if chunk:
					pdf.write(chunk)
				prog = (downloaded/total)*100
				print("--- %.2fMiB/%.2fMiB dowloaded, %.2f %% Done ---" % (downloaded/1024/1024,total/1024/1024,prog), end="\r")
		print()
	else:
		print("\nHuman error !")





def resume():

	file_url = str(input("\nGive Youtube video url : "))
	r = requests.get(file_url, stream = True)
	with open("data.txt" ,"wb") as pdf:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				pdf.write(chunk)
	r.close()


	substr1 = "<title>"
	substr2 = "</title>"
	start = end = -1

	with open("data.txt","r") as fp:
		for line in fp:
			if line.find(substr1) != -1:
				start = line.find(substr1)
			if line.find(substr2) != -1:
				end = line.find(substr2)
			if start != -1 and end != -1:
				break
	title = line[start+7:end-10]
	title = re.sub(r'[^a-zA-Z0-9 ]',r'',title)
	title = title.strip()
	title = re.sub(' +', ' ', title)
	print(title)
	vid_name = title + ".mp4"
	if os.path.isfile(vid_name) == False :
		print("File does not exists, check if partially downloaded file is in the current location ! or try using 1st option.")
		os.remove("data.txt")
		sys.exit()

	var = 0
	res = ""
	with open("youtube_logs.txt","r") as fi:
		for line in fi:
			if file_url in line:
				var = 1
				continue
			if var==1:
				res = str(line)
				break

	substr = ""
	if "144p" in res:
		substr = "\"itag\":17"
	elif "360p" in res:
		substr = "\"itag\":18"
	elif "720p" in res:
		substr = "\"itag\":22"
	elif "1080p" in res:
		substr = "\"itag\":37"
	elif "3072p" in res:
		substr = "\"itag\":38"

	with open("data.txt","r") as f:
		for line in f:
			start = line.find(substr)
			if start != -1:
				tempnum = start+17
				tempstr = line[tempnum]
				while tempstr != "\"" :
					tempnum += 1
					tempstr = line[tempnum]
				link = line[start+17:tempnum]
				link = link.replace("\\u0026","&")
				print()
	
	os.remove("data.txt")
	r = requests.get(link, stream=True)
	downloaded = os.path.getsize(vid_name)
	total = int(r.headers.get('content-length'))
	r.close()
	print()
	print("----> Download Status <----")
	print("--- %.2fMiB/%.2fMiB dowloaded, %.2f %% Done ---" % (downloaded/1024/1024,total/1024/1024,(downloaded/total)*100))
	ans = str(input("\nDo You Want To Resume Download The Video ? Y/y/N/n : "))
	
	if ans in ["N","n"]:
		print("Abort !")
	elif ans in ["Y","y"]:
		print("\nHang on, Resume Downloading the %s file" % vid_name)
		resume_header = {'Range': 'bytes=%d-' % downloaded}
		r = requests.get(link, stream = True, headers = resume_header)
		total = downloaded
		try:
			total += int(r.headers.get('content-length'))
		except:
			print("No video size found !")
		print()
		with open(vid_name ,"ab") as pdf:
			for chunk in r.iter_content(chunk_size=1024*8):
				downloaded += len(chunk)
				if chunk:
					pdf.write(chunk)
				prog = (downloaded/total)*100
				print("--- %.2fMiB/%.2fMiB dowloaded, %.2f %% Done ---" % (downloaded/1024/1024,total/1024/1024,prog), end="\r")
		r.close()
		print()
	else:
		print("\nHuman error !")




print()
print("-----Instructions-----")
print()
print("1. Please Do Not Change File Name or File Location Untill Video is Fully(100%) Downloaded !")
print("2. Do not edit,modify or delete log file")
print()
bi = int(input("Press 1 for new download or 2 for resume download : "))
if bi == 1:
	new()
	print()
elif bi == 2:
	resume()
	print()
else:
	print("Human error !")
