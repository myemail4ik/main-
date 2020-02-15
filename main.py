#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
from datetime import datetime
import random
import os
import requests
import time
from random import shuffle
import pic #pic.picture(imgage_way,img_text)
import random_list


tokenvk = "110d381ed79978477c80de7452b829c4860ba00d83fc86be21eb237b41211a8276e2e4a21847ed371cb67"
#tokenvk = os.environ.get('vktoken')


#prosba ='\n  не забывайте про "/", иначе бот не будет читать ваши сообщения'
hi ="привет, вот что я могу:"
commands =" \n 1) /Топ (предложит выбрать жанр и выведет топ 5 в этом жанре)\n 2) Прятки (угадай где находится Мирай) \n 3) Играть (проверь свои знания в аниме) \n 4) Тест \n 5) /Cигна (сигна от Анимагик) \n 6) Камень|Ножницы|Бумага"
top ="Выбирете жанр: \n 1) /Варя (топ 5 любимых аниме Вари) \n 2) /Драма \n 3) /Экшн \n  4) /Школа \n 5) /Комедия \n  6) /Фэнтези \n 7) /Романтика \n 8) /Повседнев (повседневность) \n 9) /Музыка (музыкальне) \n 10) /Новинки"


collvo= 10 # кол во жанров
collvoinfile = 5 # кол во аниме в одном аниме
testcolvo = 50 # кол во аниме в тесте 

romantika ="romantic.txt"
fantasy="fantasy.txt"
comedy ="comedy.txt"
whatlike ="varya.txt"
school ="shool.txt"
novelty = "novelty.txt"
drama = "drama.txt"
action = "action.txt"
routine = "routine.txt"
musical = "musical.txt"



##%%%%%%%%%%%%%%% globals %%%%%%%%%%%%%%
commas=["привет","пока","/топ","прятки","/exit","/next","тест","1","2","3","4","начать","играть","/сигна", "Камень|Ножницы|Бумага"] # all commands
levl=0 #10
oldanime =0
olddanime=0
answe=0
err=0
qe=0

testcolvo=testcolvo+1
#@@@@@@@@@@@@@@@@@@ def @@@@@@@@@@@@@@@@@

print("------start-------")

def find_first_word(some_str):
    for i in some_str.split("/"):
        i = i.rstrip(",")
        if i[0].isalpha():
            return i


def send(text, user): #отпр текст
	vk_session.method("messages.send",{'user_id': user, 'message': text, 'random_id':0} )

def sendmax(text,user,file,key): # текст+idd+ картинка + json
	d =0	
	if file!=0:
		fistwrld =find_first_word(file)
		if fistwrld!="game":
			file ="pictures/" + str(file)
			print(str(file))
		a = vk_session.method("photos.getMessagesUploadServer")
		b = requests.post(a['upload_url'], files={'photo':open(file,'rb')}).json()
		c = vk_session.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
		d = "photo{}_{}".format(c["owner_id"], c["id"])
	keyboard=0
	if key!=0:
		keyboard=open("json/"+key,"r",encoding='utf-8').read()

	time.sleep(1)	
	vk_session.method("messages.send",{'user_id': user, 'message': text, 'keyboard' : keyboard, 'attachment': d, 'random_id':0} )
	file =0	


#------------sigma------------

def signa(textim,idd):
	if len(textim)<21:
		text="Лови сигну от Анимагик))"
		pic.picture("pictures/signa.jpg",textim,idd)
		time.sleep(1)
		file = str(idd)+'.jpg'
		a = vk_session.method("photos.getMessagesUploadServer")
		b = requests.post(a['upload_url'], files={'photo':open(file,'rb')}).json()
		c = vk_session.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
		d = "photo{}_{}".format(c["owner_id"], c["id"])
		keyboard=0
		keyboard=open("json/main.json","r",encoding='utf-8').read()

		time.sleep(1)	
		vk_session.method("messages.send",{'user_id': idd, 'message': text, 'keyboard' : keyboard, 'attachment': d, 'random_id':0} )
		time.sleep(2)
		path = os.path.join(os.path.abspath(os.path.dirname(__file__)), (str(idd)+'.jpg'))
		os.remove(path)
	else:
		sendmax("Много букв",idd,0,"main.json")		

def stone_scissors_paper(response,bot_answer):
	out="False_stone_scissors_paper"
	if response == "камень" and bot_answer=="ножницы" and response!= bot_answer:
		out="True_stone_scissors_paper"

	if response == "бумага" and bot_answer=="камень" and response!= bot_answer:
		out="True_stone_scissors_paper"

	if response == "ножницы" and bot_answer=="бумага" and response!= bot_answer:
		out="True_stone_scissors_paper"
	if response == bot_answer:
		out="null_stone_scissors_paper"	

	return out			


"""
def signa1(err,idd,response):
	signa_response=''
	if len(response)>6:
		for s in range (6):
		    signa_response = signa_response + response[s]
		    print(signa_response)

	if signa_response=="/сигна":
		signa_response = response.replace("/сигна",'')
		signa_response = str(signa_response)
		print(signa_response)
		if signa_response[0]==" ":
			signa_response= signa_response[1:]
		print(signa_response[0])
		if len(signa_response)<=18:	
			signa(signa_response,idd)
		else:
			sendmax("Слишком длинный текст",idd,0,"main.json")	
		err = 0
	return err		
"""	
#--------------------------------

def topchick(failname): # открытите текст файла /топ
    f = open(failname, "r",encoding = 'utf-8')
    data = f.read()
    f.close()
    return data



def test(testcolvo): # массив теста тест
	r = list(range(1,testcolvo))
	shuffle(r)
	return r




def randnumanime(): # играть
	randomnum1=random.randint(1,testcolvo)
	print("randomnum1:"+str(randomnum1))

	b = list(range(1,testcolvo))
	shuffle(b)
	print("b="+str(b))
	randomnum = str(b[int(randomnum1-2)])

	if randomnum == 39:
		randomnum = randomnum - 2
	if randomnum == 1 or 2:
		randonumber = 4	

	print(str(randomnum))	
	r = list(range(1,testcolvo))
	shuffle(r)
	print("r="+str(r))
	randomnum = int(randomnum)
	randompi = str(r[randomnum-2])
	print("out: "+str(randompi))
	return randompi




def game_gener(randompic): # чтение ответа и отправка теста или игра
	way_game = "game/"+randompic+"/question.txt"
	print(way_game) 
	with open(way_game, 'r', encoding='utf-8') as f:
		answer_ques = f.read().splitlines()
	f.close()
	answer = answer_ques[0]
	print("ответ:" + str(answer))
	question = open(way_game, 'r', encoding='utf-8')
	questions= question.read()
	questions =questions[1 : ]
	picture =way_game = "game/"+randompic+"/picture.jpg"
	picture = str(picture)
	time.sleep(1)
	sendmax("Варианты ответов \n"+questions,idd, picture,"test.json")
	return answer

def game_check(resp,ansver,json): # свериться правильный ли ответ в тест или играть
	checkstatus = 2
	testmark="err"
	if resp=="1":
		if resp == ansver:
		  	testmark ="Правильно"
		  	checkstatus = 1
		  	print(testmark)
		  	sendmax(testmark,idd,"ryght.jpg",json)
		if resp!= ansver:
		    testmark ="Упс, ошибочка"
		    checkstatus = 1
		    print(testmark)
		    sendmax(testmark,idd,"ron.png",json)

	if resp=="2":
		if resp == ansver:
		    testmark ="Правильно"
		    checkstatus = 1
		    print(testmark)
		    sendmax(testmark,idd,"ryght.jpg",json)
		if resp!= ansver:
		    testmark ="Упс, ошибочка"
		    checkstatus = 1
		    print(testmark)
		    sendmax(testmark,idd,"ron.png",json)	
		     	

	if resp=="3":
		if resp == ansver:
		    testmark ="Правильно"
		    checkstatus = 1
		    print(testmark)
		    sendmax(testmark,idd,"ryght.jpg",json)
		if resp!= ansver:
		    testmark ="Упс, ошибочка"
		    checkstatus = 1
		    print(testmark)			
		    sendmax(testmark,idd,"ron.png",json)

	if resp=="4":
		if resp == ansver:
		    testmark ="Правильно"
		    checkstatus = 1
		    print(testmark)
		    sendmax(testmark,idd,"ryght.jpg",json)
		if resp!= ansver:
		    testmark ="Упс, ошибочка"
		    checkstatus = 1
		    print(testmark)
		    sendmax(testmark,idd,"ron.png",json)
	return checkstatus	        


def error(err, commas,response, signa_err): # ошибки
	summerr=0
	err=0

	for numbererr in range(int(len(commas))):
		print("err_for:"+str(numbererr))
		if response!= commas[numbererr]:
		    summerr= summerr+1
		       	
	print(str(len(commas))+"sum_err:"+str(summerr))

	if summerr == int(len(commas)):
		print("sum_err:"+str(summerr))
		err=1
	summerr=0

	if signa_err==True:
		err=0

	return err		

#----------------------top----------------



def top_mess(resp,top,err): # топ
	levl =0	
	if resp=="/романтика":
		sendmax(top,idd,0,"top.json")
		textin =topchick("top/"+romantika)
		resp= resp.replace("/","")
		send(resp + ": \n" + textin, idd)
		err =0

	if resp=="/новинки":
		sendmax(top,idd,0,"top.json")
		textin =topchick("top/"+novelty)
		resp= resp.replace("/","")
		send(resp + ": \n" + textin, idd)
		err =0


	if resp=="/драма":
		sendmax(top,idd,0,"top.json")
		textin = topchick("top/"+drama)
		resp= resp.replace("/","")
		send(resp + ": \n" + textin, idd)
		err =0

		
	if resp=="/экшн":
		sendmax(top,idd,0,"top.json")
		textin = topchick("top/"+action) 
		resp= resp.replace("/","")
		send(resp + ": \n" + textin, idd)
		err =0


	if resp=="/школа":
		sendmax(top,idd,0,"top.json")
		textin = topchick("top/"+school)
		resp= resp.replace("/","")
		send(resp + ": \n" + textin, idd)
		err =0


	if resp=="/варя":
		sendmax(top,idd,0,"top.json")
		textin = topchick("top/"+whatlike)
		resp= resp.replace("/","")
		send(resp + ": \n" + textin, idd)
		err =0

	
	if resp=="/комедия":
		sendmax(top,idd,0,"top.json")
		textin = topchick("top/"+comedy)
		resp= resp.replace("/","")
		send(resp + ": \n" + textin, idd)
		err =0

	if resp=="/фэнтези":
		sendmax(top,idd,0,"top.json")
		textin= topchick("top/"+fantasy)
		resp= resp.replace("/","")
		send(resp + ": \n" + textin, idd)
		err =0

	if resp=="/повседнев":
		sendmax(top,idd,0,"top.json")
		textin =topchick("top/"+routine)
		resp= resp.replace("/","")
		send(resp + ": \n" + textin, idd)
		err =0

	if resp=="/повседневность":
		sendmax(top,idd,0,"top.json")
		textin =topchick("top/"+routine)
		resp= resp.replace("/","")
		send(resp + ": \n" + textin, idd)
		err =0

	if resp=="/музыка":
		sendmax(top,idd,0,"top.json")
		textin =topchick("top/"+ musical)
		resp= resp.replace("/","")
		send(resp + ": \n" + textin, idd)
		err =0
	return err		



#--------------------------------

vk_session=vk_api.VkApi(token=tokenvk)

session_api=vk_session.get_api
longpoll = VkLongPoll(vk_session)

while True:
	for event in longpoll.listen():
	   if event.type == VkEventType.MESSAGE_NEW:
		   print(str(event.user_id))
		   print("new message: "+ str(datetime.strftime(datetime.now(), "%H:%M:%S")))
		   print("text: "+str(event.text))
		   idd = event.user_id
		   response = event.text.lower()
		   if response[0]==" ":
		   	response[0]=''
		   user = vk_session.method("users.get", {"user_ids": idd})
		   name_idd = user[0]['first_name']
		   #############################################
		   
		   if event.to_me:
		       signa_err=False
		       if levl == 9 and response!="/сигна":
		       	signa(response,idd)
		       	signa_err=True
		       	levl=0
		       	err=0	

		       response= response.replace(" ","")

		       err = error(err, commas, response, signa_err)
		       print("err_exit:"+str(err))

		       if response=="пока":
		       	sendmax("Пока;)",idd,"bay.jpg","hiafterbay.json")
		       	levl=0
		       	err=0


		       if response=="привет" or response=="назад":
		       	sendmax(hi+"\n"+commands,idd,"hi.jpg","main.json")
		       	levl=0
		       	err=0

		       if response=="начать":
		       	sendmax(hi+"\n"+commands,idd,"hi.jpg","main.json")
		       	levl=0
		       	err=0


		       if response == "/сигна":
		       	print("signa_levl_9")
		       	sendmax("Введите текст",idd,0,0)
		       	levl=9
		       	err=0
		       

#-------------------------------------------------			   	

		       if response=="камень|ножницы|бумага":
		       	number_figer=["камень","ножницы","бумага"]
		       	shuffle(number_figer)
		       	number_figer=number_figer[1]
		       	number_figer=str(number_figer)
		       	answer= str(number_figer)
		       	print("answer_bot: "+str(number_figer))
		       	time.sleep(1)
		       	sendmax("Попробуй обыграй меня)",idd,0,"stone_paper_scissors.json")
		       	err=0
		       	levl=10

		       if levl==10 and response!= "камень|ножницы|бумага" :
		       	number_figer=stone_scissors_paper(response,number_figer)
		       	if number_figer=="True_stone_scissors_paper":
		       		sendmax("Да ну тебя, плохая игра",idd,"mirai_right.jpg","main.json")
		       		levl=0
		       		err=0

		       	if number_figer=="False_stone_scissors_paper":
		       		sendmax("Я выиграла) Я загадывала " + answer+")",idd,"mirai_ron.png","main.json")
		       	err=0
		       	levl=0
		       	if number_figer=="null_stone_scissors_paper":
		       		sendmax("Ничья...",idd,"mirai_ron_nech.png","main.json")
		       	err=0
		       	levl=0


		       if response =="играть":
		       	err=0
		       	print(str(oldanime)+"|||"+str(olddanime))
		       	numberanime=randnumanime()
		        if numberanime == olddanime or oldanime:
		       		numberanime=randnumanime()
		       		print(str(oldanime)+"|||"+str(olddanime))
		       	olddanime = oldanime
		       	oldanime = numberanime
		       	time.sleep(1)
		       	levl =2	
		       	answe = game_gener(numberanime)



		       	

		       if levl ==2:
		       	err=0
		       	levl = game_check(response,answe,"main.json")


#--------------------------topcommand----------------------		       
		       if response=="тест":
		       	mark = 0
		       	levl=3
		       	err=0
		       	massiveanimetest = test(testcolvo)
		       	print(len(massiveanimetest))
		       	print(massiveanimetest[1])
		       	print(massiveanimetest)
		       	firstqe = str(massiveanimetest[0])
		       	secondqe = str(massiveanimetest[1])
		       	therdqe = str(massiveanimetest[2])
		       	fourthqe =str(massiveanimetest[3])
		       	fifthqe =str(massiveanimetest[4])
		       	sendmax("№1",idd,0,0)
		       	answertest = game_gener(firstqe)

		       if response=="/next" and qe==1:
		       	levl=4
		       	sendmax("№2",idd,0,0)
		       	answertest = game_gener(secondqe)

		       if response=="/next" and qe==2:		
		       	levl=5
		       	sendmax("№3",idd,0,0)
		       	answertest = game_gener(therdqe)

		       if response=="/next" and qe==3:
		       	levl=6
		       	sendmax("№4",idd,0,0)
		       	answertest = game_gener(fourthqe)
		       if response=="/next" and qe==4:
		       	levl=7
		       	sendmax("№5",idd,0,0)
		       	answertest = game_gener(fifthqe)
		      	 	


		       
		       if levl == 3:
		       	err=0
		       	levl = game_check(response,answertest,"test5.json")
		       	if response==answertest:
		       		mark = mark+1
		       	qe=1
		       	levl = 3

		       if levl == 4:
		       	err=0
		       	levl = game_check(response,answertest,"test5.json")
		       	if response==answertest:
		       		mark = mark+1
		       	qe=2
		       	levl = 4

		       if levl == 5:
		       	err=0
		       	levl = game_check(response,answertest,"test5.json")
		       	if response==answertest:
		       		mark = mark+1
		       	qe=3
		       	levl = 5

		       if levl == 6:
		       	err=0
		       	levl = game_check(response,answertest,"test5.json")
		       	if response==answertest:
		       		mark = mark+1
		       	qe=4
		       	levl = 6

		       if levl == 7:
		       	err=0
		       	levl = game_check(response,answertest,"balltest5.json")
		       	if response==answertest:
		       		mark = mark+1
		       	levl = 7
		       	qe=0


		       if response =="/балл":	
		       	sendmax(str(mark)+"/5",idd,0,"main.json")
		       	if mark==5:
		       		sendmax("Ты ответил привильно на все 5 вопросов)",idd,"prise.png","main.json")
		       	levl = 0
		       	mark=0
		       	qe=0
		       	

		       if response=="/exit":
		       	qe=0
		       	levl = 0
		       	mark=0
		       	sendmax(hi+"\n"+commands,idd,"hi.jpg","main.json")

#-------------------------------------

		       if response=="прятки":
		       	list_variant=list(range(1,4))
		       	true_result = 1
		       	true_result = random_list.massive_random(list_variant)
		       	print("true_result_game_guess ответ:" + str(true_result))
		       	true_result = str(true_result)
		       	sendmax("Угадай где Мирай",idd,"background.jpg","game_guess.json")
		       	levl=8
		       	err =0
		     

		       if levl == 8 and true_result == response and response !="прятки":
		       	sendmax("Правильно", idd, str(true_result)+".jpg", "main.json")
		       	levl=0
		       	err=0

		       if levl == 8 and true_result!= response  and response !="прятки":
		       	print("ron_game")
		       	sendmax("Упс, ошибочка(", idd, str(true_result)+".jpg", "main.json")
		       	levl=0
		       	err=0	


		       if response=="/топ":
		       	print(response)
		       	sendmax(top,idd,0,"top.json")
		       	err =0

		       err=top_mess(response,top,err)	

		       if err == 1:
		      		sendmax('ERROR  Я не знаю такую команду((',idd,"error.jpg","main.json")
		      		err=0
		      		