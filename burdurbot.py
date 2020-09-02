import requests
import json
import praw
import time
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials
import traceback

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
client = gspread.authorize(creds)
worksheet = client.open('BurdurBot').sheet1
worksheet2 = client.open('BOT').sheet1

karaliste = ("PeriodicDioxide","KrgzBey","CrayzEbabil3","Yavuzardaergul2","HolyAyran","kahnivore","Nonstol")
reddit = praw.Reddit(
    client_id='',
    client_secret='',
    username='PeriodicDioxide',
    password='',
    user_agent='u/ruzgarerik Bot')
while True:
	try:
		for submission in reddit.subreddit("KGBTR").new(limit=10):
			sayac = 0
			sayac2=0 
			linkler = []
			reply = 0
			yorumlar = []
			ensonposttarih=""
			ensonyorumtarih=""
			author = str(submission.author)
			url = "https://www.reddit.com/user/{}/top_karma_subreddits.json"
			r = requests.get(url.format(author), headers = {'User-agent': 'u/ruzgarerik bot'})
			data = r.json()
			burdurlu = "burdurland" in str(data)
			if burdurlu == True:
				print("----------------------------------------")
				print(author,"burdurlu")
				s = requests.get('https://api.pushshift.io/reddit/submission/search/?author={}&subreddit=burdurland'.format(author))
				submissiondata = s.json()
				sayac=0
				sayac2=0
				reply = 0
				linkler = []
				yorumlar = []
				for element in submissiondata['data']:
					sayac=sayac+1
				try:
					ensonpost = submissiondata['data'][0]['created_utc']
					ensonposttarih = datetime.datetime.fromtimestamp(int(ensonpost))
				except:
					print(author,"postu yok")
					ensonposttarih = ""
				c = requests.get('https://api.pushshift.io/reddit/comment/search/?author={}&subreddit=burdurland'.format(author))
				commentdata = c.json()
				for element in commentdata['data']:
					sayac2=sayac2+1


				try:
					ensonyorum = commentdata['data'][0]['created_utc']
					ensonyorumtarih = datetime.datetime.fromtimestamp(int(ensonyorum))

				except Exception:
					print(author," yorumu yok")
					ensonyorumtarih = ""
					traceback.print_exc()
					
				sid = submission.id
				try:
					cell = worksheet.find(sid)
					if cell:
						reply = 1
						print(author, "id veritabanında var")
						print("----------------------------------------")
						tarih = datetime.date.today()
						worksheet2.append_row([sid,author,str(tarih)])
		
				except Exception:
					print(author,"id veritabanında yok")
					reply = 0
					traceback.print_exc()


				try:
					if reply == 0:
						if author in karaliste:
							reply=1
							print(author,"kara listede cevap verilmiyor")
							print("----------------------------------------")
							tarih = datetime.date.today()
							worksheet2.append_row([sid,author,str(tarih)])
						else:
							reply=0
							print(author,"kara listede değil")
				except Exception:
					print("hata")
					traceback.print_exc()


				try:
					if reply == 0:
						if sayac <= 2 and sayac2 <= 10:
							reply = 1
							print(author, "şart yerine geldi az bulgurlu")
							print("----------------------------------------")
							tarih = datetime.date.today()
							worksheet2.append_row([sid,author,str(tarih)])
						else:
							print(author, "çok bulgurlu")
				except Exception:
					traceback.print_exc()
					print("hata")


				if reply == 0:
					submission.reply('''
# Burdurlu Normie Tespit Edildi !
***
***
^{} ^Paylaşım ^Yapmış

^En ^Son ^Paylaşım ^tarihi {} GMT+0

^{} ^Yorum ^Yapmış

^En ^Son ^Yorum ^Tarihi {} GMT+0
***
^Bip ^Bop. ^Ben ^Burdurlu ^Bulucu ^Bot.
[KGBTR Burdurlu Kullanıcılar Veritabanı ](https://kgbtrburdurlular.herokuapp.com/)
***
	'''.format(sayac,ensonposttarih,sayac2,ensonyorumtarih))
					print("Görev tamamlandı bulgurlu bildirildi")
					print("----------------------------------------")
					tarih = datetime.date.today()
					worksheet.append_row([sid,author,str(tarih)])
					worksheet2.append_row([sid,author,str(tarih)])


			else:
				sid = submission.id
				print(author,"burdurlu değil")
				try:
					cell = worksheet2.find(sid)
					if cell:
						reply = 1
						print(author, "id veritabanında var temiz")
					else:
						reply = 0
				except:
					reply = 0
				if reply == 0:
					tarih = datetime.date.today()
					worksheet2.append_row([sid,author,str(tarih)])
		print("++++++++++++++++++++++++++++++++++++++++")
		print("ilk 10 bitti")
		print("++++++++++++++++++++++++++++++++++++++++")
	except Exception:
		print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
		print("                 HATA                   ")
		traceback.print_exc()
		print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
