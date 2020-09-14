import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,InlineKeyboardButton,InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler,
                          ConversationHandler)
from time import sleep
import requests
import time
import os 
import sched
import threading
import gspread
from oauth2client.service_account import ServiceAccountCredentials
os.environ['TZ']='Portugal'
time.tzset()
gmail_user = 'mundohbl2020@gmail.com'
gmail_password = 'Hblbot2020'
subject= ' Nova Avaliação no BOT'
sent_from = gmail_user
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1PUVYTUywilJjJNuBHv06gJXEo8X8ddovJ232OgLYWOs/edit#gid=0").sheet1
user_sheet=client.open_by_url("https://docs.google.com/spreadsheets/d/1PUVYTUywilJjJNuBHv06gJXEo8X8ddovJ232OgLYWOs/edit#gid=1831337301").get_worksheet(1)
# date_sheet=client.open_by_url("https://docs.google.com/spreadsheets/d/1PUVYTUywilJjJNuBHv06gJXEo8X8ddovJ232OgLYWOs/edit#gid=1788730953").get_worksheet(2)
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
 
logger = logging.getLogger(__name__)
PORT = int(os.environ.get('PORT', 5000))
CODE,BREAK,ENDBREAK,FINISHBREAK,EVALUATION,GOAL,GOAL_ACHIEVING,BREAKFAST,IMP_BREAKFAST,AGE,HEIGHT,WEIGHT,MOTIVATION,PHONE,RESULTS = range(15)
coach_data=[]
TOKEN="1295514171:AAGGiqZHneD8REKvHVAg_k_XDBm2ti3t1dI"
def get_name(update):
	if update.message.chat.first_name != None:
		if update.message.chat.last_name != None:
			return str(update.message.chat.first_name)+' '+str(update.message.chat.last_name)
		else:
			return update.message.chat.first_name
	elif update.message.chat.username != None:
		return update.message.chat.username
	else:
		return "Sir"
def start(update, context): 
	coach_data=[]
	update.message.reply_text(
        'Olá <b>{}!</b>\n\n'
'Eu sou o <b>Nutrition Assistant</b>, o seu assistente, que lhe vai dar '
'informações exclusivas sobre nutrição, como fazer uma '
'reeducação alimentar e informação sobre a nutrição Herbalife '
'Nutrition.'.format(get_name(update)),
        parse_mode="HTML")
	sleep(5)
	update.message.reply_text('Para podermos avançar com a sua Avaliação de Bem-Estar '
'Online, receber o Ebook <b>“A nova ciência para Perder Gordura e '
'não voltar a ganhá-la”</b> e informações sobre como otimizar os '
'seus objetivos.',parse_mode="HTML")
	sleep(5)
	update.message.reply_text('Precisamos que escreva abaixo o <b>CÓDIGO</b> do seu <b>Nutrition '
'Coach</b> para podermos avançar: ',parse_mode="HTML")
	return CODE
 
 
def code(update, context):
    user = update.message.from_user
    code=str(update.message.text)
    is_code_correct=False
    try:
    	data= sheet.get_all_records()
    	i=1
    	for row in data:
    		i=i+1
    		if str(row['Access Code']) == code.upper():
    			is_code_correct= True
    			coach_data=row
    			sheet.update('A{}'.format(str(i)),code.upper())
    except:
    	is_code_correct=False

    try:
    	ucell=user_sheet.find(str(update.message.chat.id))
    	ucount=ucell.row
    except:
    	ucount = len(user_sheet.get_all_records())+2
    	if ucount ==0:
    		ucount=2

    if is_code_correct :
    	row='A'+str(ucount)+":"+'C'+str(ucount)
    	user_sheet.update(row,[[str(update.message.chat.id),str(code.upper()),'Active']])
    	user_sheet.update('Q{}'.format(str(ucount)),get_name(update))
    	update.message.reply_text('Parabéns, código correto!\n'
'O seu Nutrition Coach é:\n\n'
'<b>{}</b>\n'
'<b>+{}</b>\n\n'
'<b>Ps:</b> Quando quiser sair, deixar de receber as nossas informações , a '
'qualquer momento escreva > /stop\n\nE quando quiser procurar os comandos é só colocar / e vai '
'aparecer um menu para escolher vários opções.'.format(coach_data["Coach's Name and Surname"],coach_data['Coach Mobile Phone']),parse_mode="HTML")
    	reply_keyboard = [['SIM QUERO FAZER AVALIAÇÃO AGORA'] ,['QUERO FAZER AVALIAÇÃO MAIS TARDE']]
    	sleep(5)
    	update.message.reply_text('Para podermos indicar o seu plano nutricional e saber o seu peso ideal, '
'IMC, etc é necessário fazer a nossa <b>Avaliação de Bem-Estar Online.</b>\n '
'(menos de 3 minutos)\n\n'
'<b>Escolha uma das opções abaixo para '
'continuar:\n'
'👇👇👇👇👇👇👇</b>',parse_mode="HTML",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,resize_keyboard=True))
    	return EVALUATION
    else:
    	row='A'+str(ucount)+":"+'C'+str(ucount)
    	user_sheet.update(row,[[str(update.message.chat.id),None,'InActive']])
    	update.message.reply_text("o código que você digitou está errado")
 
def evaluate_now(update,context):
	reply_keyboard=[['PERDER PESO'],['AUMENTAR DE PESO'],['MELHORAR BEM-ESTAR'],['+ PERFORMANCE DESPORTIVA']]
	update.message.reply_text('Parabéns <b>{}</b> pela decisão!\n\n'
'Esta Avaliação será muito rápida, mas tente responder o mais correto possível '
'para o seu Coach, o(a) possa ajudar com o plano nutricional indicado para si!\n\n <b>⚠️‼️ PARA QUE NÃO HAJA\n'
'ERROS NA SUA AVALIAÇÃO\n'
'ONLINE, FAÇA A AVALIAÇÃO\n'
'TODA SEGUIDA, SEM\n'
'PARAGENS ATÉ AO FIM!</b>'.format(get_name(update)),parse_mode="HTML")
	update.message.reply_text('<b>Qual o seu objetivo?</b>\n(Escolha uma das opções abaixo:)',parse_mode="HTML",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,resize_keyboard=True))
	return GOAL

def evaluate_later(update, context):
    user = update.message.from_user
    rowno=user_sheet.find(str(update.message.chat.id)).row
    coach_row=sheet.find(user_sheet.acell('B{}'.format(str(rowno))).value).row
    coach_data=sheet.row_values(coach_row)
    
    update.message.reply_text('Está bem, não há problema!\n\n'
'Pode fazer depois a sua <b>AVALIAÇÁO ONLINE</b>, para isso só terá '
'que <b>clicar no comando abaixo:</b>\n\n /evaluation \n\n'
'Entretanto vamos deixar-lhe aqui abaixo o nosso <b>Ebook:</b>\n\n'
'<b>“A nova ciência para Perder '
'Gordura e não voltar a ganhá-la”.</b>\n\n Faça o <b>download agora</b>, este <b>Ebook</b> vai-lhe ajudar muito a '
'entender o que se passa na nossa alimentação e muita '
'informação sobre alguns mitos.\n\n '
'👇👇👇👇👇👇👇👇👇',parse_mode="HTML")
    sleep(5)
    update.message.reply_photo(photo=open("2.png","rb"))
    sleep(5)
    update.message.reply_text('<a href="https://drive.google.com/u/0/uc?id=1ls5MVWSIk9HzUH1dUIURZAgSM86Zjz3i&export=download">Clique aqui para download – <b>EBOOK – “A Nova Ciência para Perder Gordura e não voltar a Ganhá-la”</b></a>',parse_mode="HTML")
    sleep(9)
    update.message.reply_text('A partir de amanhã vamos enviar-lhe conteúdo exclusivo, esteja atendo(a) aqui no assistente.') 
    kb=[[InlineKeyboardButton('PERDER PESO',url="https://"+coach_data[6]+".nutricaosaudavel.net/perder-peso.php")],
    [InlineKeyboardButton('AUMENTAR DE PESO',url="https://"+coach_data[6]+".nutricaosaudavel.net/aumentar-peso.php")],
    [InlineKeyboardButton('MELHORAR BEM-ESTAR',url="https://"+coach_data[6]+".nutricaosaudavel.net/bem-estar.php")],
    [InlineKeyboardButton('+ PERFORMANCE DESPORTIVA',url="https://"+coach_data[6]+".nutricaosaudavel.net/desporto.php")]]
    update.message.reply_text('Certamente quer saber como pode '
'atingir os seus resultados!\n\n'
'Escolha uma das opções, em função '
'dos objetivos que pretende, e será '
'direcionado(a) para um site '
'explicativo de como poderá '
'participar nas nossas <b>MARATONAS '
'SAUDÁVEIS DE 10 DIAS</b> e atingir a '
'sua melhor versão de sempre e para '
'sempre!\n\n'
'Mas antes disso, veja alguns \n <b>Resultados '
'INCRÍVEIS!</b>',parse_mode="HTML")
    sleep(5)
    update.message.reply_photo(photo=open("3.png","rb"))
    update.message.reply_photo(photo=open("4.png","rb"))
    update.message.reply_photo(photo=open("13.png","rb"))
    update.message.reply_photo(photo=open("11.png","rb"))
    update.message.reply_text('<b>ESCOLHA A OPÇÃO PARA CONHECER O SEU PLANO NUTRICIONAL E COMO PODE '
'PARTICIPAR NA MARATONA SAUDÁVEL 10 DIAS!\n\n'
'👇👇👇👇👇👇👇👇👇👇</b>',parse_mode="HTML")
    sleep(5)
    update.message.reply_photo(photo=open("12.png","rb"))
    sleep(5)
    update.message.reply_text('👇👇👇👇👇👇👇👇👇👇',reply_markup=InlineKeyboardMarkup(kb,one_time_keyboard=True))
    sleep(20)
    update.message.reply_text('Qualquer dúvida não hesite em contactar o seu <b>Coach Pessoal</b>, '
'pois sou apenas um ROBOT 🤖☺️\n\n'
'Até amanhã, om o nosso primeiro vídeo incrível, fique atento(a)!\n\n<b>{}\n'
'Telm: {}</b>\n\n'
'https://{}.nutricaosaudavel.net/objetivo.php'.format(coach_data[2],coach_data[4],coach_data[6]),parse_mode="HTML")
    return ConversationHandler.END

 
 

 
def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())
 
    return ConversationHandler.END
def update_sheet(update,context,col):
	goal=update.message.text
	cell=user_sheet.find(str(update.message.chat.id))
	user_sheet.update('{}{}'.format(col,str(cell.row)),goal)

def goal1(update,context):
	update_sheet(update,context,'D')
	reply_keyboard=[['ATÉ 5KG'],['ENTRE 5KG A 10KG'],['MAIS DE 10KG']]
	update.message.reply_text('<b>Quantos Kg quer Perder?</b>\n(Escolha uma das opções abaixo:)',parse_mode="HTML",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,resize_keyboard=True))
	return GOAL_ACHIEVING

def goal2(update,context):
	update_sheet(update,context,'D')
	reply_keyboard=[['ATÉ 5KG'],['ENTRE 5KG A 10KG'],['MAIS DE 10KG']]
	update.message.reply_text('Quantos Kg quer Aumentar?',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,resize_keyboard=True))
	return GOAL_ACHIEVING

def goal3(update,context):
	update_sheet(update,context,'D')
	reply_keyboard=[['MELHORAR O PEQUENO-ALMOÇO'],['AUMENTAR OS NÍVEIS DE ENERGIA']]
	update.message.reply_text('O que gostaria de melhorar?',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,resize_keyboard=True))
	return GOAL_ACHIEVING

def goal4(update,context):
	update_sheet(update,context,'D')
	reply_keyboard=[['RECUPERAÇÃO PÓS-TREINO'],['PRÉ-TREINO E LANCHES']]
	update.message.reply_text('O que gostaria de melhorar?',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,resize_keyboard=True))
	return GOAL_ACHIEVING

def goal_achieving(update,context):
	indices = {'PERDER PESO':'E','AUMENTAR DE PESO':'F','MELHORAR BEM-ESTAR':'G','+ PERFORMANCE DESPORTIVA':'H'}
	rowno=user_sheet.find(str(update.message.chat.id)).row
	goal = str(user_sheet.acell('D{}'.format(str(rowno))).value)
	update_sheet(update,context,indices[goal])
	reply_keyboard=[['SIM, ESTOU!'],['NÃO, MAS QUERO AJUDA!']]
	update.message.reply_text('<b>Já está a fazer algo, para atingir esse objetivo?</b>\n(Escolha uma das opções abaixo:)',parse_mode="HTML",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,resize_keyboard=True))
	return BREAKFAST
def breakfast(update,context):
	update_sheet(update,context,'I')
	reply_keyboard=[['LEITE, CEREAIS, PÃO'],['CAFÉ, BOLOS, ETC'],['BATIDOS DE FRUTA, IOGURTE'],['NADA']]
	update.message.reply_text('Ambos sabemos que a alimentação é um fator importante para '
'o nosso bem-estar.\n\n'
'<b>O que costuma comer ao pequeno almoço?</b>\n(Escolha uma das opções abaixo:)',parse_mode="HTML",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,resize_keyboard=True))
	return IMP_BREAKFAST

def imp_breakfast(update,context):
	update_sheet(update,context,'J')
	reply_keyboard=[['SIM SABIA'],['NÃO SABIA']]
	sleep(5)
	update.message.reply_text('<b>Sabia que o pequeno-almoço é a refeição mais importante do dia?</b>',parse_mode="HTML",reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True,resize_keyboard=True))
	return BREAK

def middle_break1(update,context):
	update.message.reply_text('Está comprovado que quem faz um <b>pequeno-almoço '
'equilibrado</b> (rico em vitaminas, gorduras boas, minerais e '
'proteínas) aumenta a energia, melhora o humor e tem um '
'maior controlo do apetite e por consequência <b>consegue '
'controlar melhor o peso.</b>\n\n'
'Na imagem abaixo, vai poder ver como deveria de ser a divisão '
'das nossas escolhas, para ter uma vida plena.',parse_mode="HTML")
	sleep(7)
	update.message.reply_photo(photo=open("1.png","rb"))
	sleep(9)
	update.message.reply_text('<b>{}</b> para saber o resultado do seu IMC (Índice '
'de Massa Corporal) precisamos de algumas informações '
'para fazer-mos os cálculos.\n\n'
'*TUDO o que colocar é 100% confidencial'.format(update.message.chat.first_name),parse_mode="HTML")
	sleep(5)
	update.message.reply_text('<b>Quantos anos têm?</b>\n(Exemplo: 45)',parse_mode="HTML")
	return AGE

def age(update,context):
	update_sheet(update,context,'K')
	age=update.message.text
	update.message.reply_text('<b>Qual é a sua altura?</b>\n‼️ Por favor coloque (.) e '
'<b>não</b> (,) escreva em'
'metros.\n\n'
'<b>Exemplo:</b> 1.85',parse_mode="HTML")
	return HEIGHT

def height(update,context):
	update_sheet(update,context,'L')
	update.message.reply_text('<b>Por último, qual é o seu peso?</b>\n‼️ Por favor coloque (.) e '
'<b>não</b> (,) escreva em KG.\n\n'
'<b>Exemplo:</b> 80.5',parse_mode="HTML")
	return WEIGHT

def weight(update,context):
	update_sheet(update,context,'M')
	weight=float(update.message.text)
	rowno=user_sheet.find(str(update.message.chat.id)).row
	height = float(user_sheet.acell('L{}'.format(str(rowno))).value)
	bmi= weight/(height**2)
	user_sheet.update('O{}'.format(str(rowno)),'{:.2f}'.format(bmi))
	reply_keyboard=[['POUCA'],['ALGUMA'],['MUITA']]
	update.message.reply_text('Qual o <b>Grau de motivação</b> que tem neste momento para iniciar '
'um Plano Nutricional e atingir os resultados que pretende?',parse_mode="HTML",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,resize_keyboard=True))
	return MOTIVATION

def motivation(update,context):
	update_sheet(update,context,'N')
	update.message.reply_photo(photo=open("10.png","rb"))
	sleep(5)
	update.message.reply_text('Quer saber o <b>RESULTADO DA SUA AVALIAÇÃO</b> e receber o nosso '
'<b>EBOOK GRÁTIS ?</b> \n\n<b>“A nova ciência para Perder Gordura e não '
'voltar a ganhá-la”</b>\n\n'
'Só terá que colocar o seu <b>número de telemóvel</b>, com o <b>indicativo</b> '
'do seu <b>País</b> \n\n<b>Exemplo:</b> +351960000000\n\n'
'Coloque o número correto não fazemos <b>SPAM.</b>\n\nOs dados são para lhe conseguir fornecer o <b>RESULTADO da '
'AVALIAÇÁO</b>, e o seu <b>Nutrition Coach</b> lhe prestar o melhor '
'serviço de aconselhamento.\n\n Coloque abaixo o seu '
'<b>contacto telefónico</b>\n'
'👇👇👇👇',parse_mode="HTML")
	return PHONE



def wrong_phone(update,context):
	update.message.reply_text('Por favor introduza, os valores corretamente. (Os valores '
'aceites são só números, não coloque texto à frente)\n\n'
'<b>Exemplo: +351960000000</b>\n\n'
'<b>Digite de novo o valor correto:</b>',parse_mode="HTML")
	return PHONE

def phone(update,context):
	update_sheet(update,context,'P')
	rowno=user_sheet.find(str(update.message.chat.id)).row
	user_data=user_sheet.row_values(str(rowno))
	coach_row=sheet.find(user_data[1]).row
	coach_data=sheet.row_values(coach_row)
	goal=str(user_data[4]).strip()+str(user_data[5]).strip()+str(user_data[6]).strip()+str(user_data[7]).strip()
	email_text= """\
<html>
<head></head>
<body>

<p>Olá <b>{}</b> acabou de ser efetuada uma <b>Avaliação Online no BOT</b>
com sucesso, entre em contacto já com este lead, os dados da avaliação
estão abaixo:<br/><br/>
<b>NOME E APELIDO:</b> {}<br/><br/>

<b>TELEMÓVEL DO LEAD:</b> {}<br/><br/>

<b>IDADE:</b> {}<br/><br/>

<b>ALTURA:</b> {} <br/><br/>

<b>PESO:</b> {} KG<br/><br/>

<b>RESULTADO IMC:</b> {}<br/><br/>

<b>OBJETIVO:</b> {}<br/><br/>

<b>OBJETIVO QUE PROCURA :</b> {}<br/><br/>

<b>ESTÁ A FAZER ALGO? :</b> {}<br/><br/>

<b>O QUE COME AO PEQUENO ALMOÇO:</b> {}<br/><br/>

<b>GRAU DE MOTIVAÇÃO:</b> {}<br/><br/>

Bons negócios<br/>
Equipa MundoHBL

""".format(coach_data[2],user_data[16],user_data[15],user_data[10],user_data[11],user_data[12],user_data[14],user_data[3],goal,user_data[8],user_data[9],user_data[13])
	# email_text=email_text.encode('iso-8859-1')
	msg = MIMEMultipart('alternative')

	msg['From'] = sent_from
	msg['To'] = coach_data[3]
	msg['Subject'] = subject

	part2 = MIMEText(email_text, 'html')
	msg.attach(part2)
	smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo()
	smtpserver.login(gmail_user, gmail_password)
	smtpserver.sendmail(sent_from,coach_data[3],msg.as_string())
	kb=[['VER RESULTADO AGORA >>']]
	update.message.reply_text('<b>Clique no botão abaixo para ver '
'o resultado da sua Avaliação e '
'ganhar o Ebook!\n'
'👇👇👇👇👇👇👇</b>',parse_mode="HTML",reply_markup=ReplyKeyboardMarkup(kb,one_time_keyboard=True,resize_keyboard=True))
	url="https://herokumessaging.herokuapp.com/schedule?user="+str(update.message.chat.id)
	response = requests.get(url)
	return RESULTS

def results(update,context):
	rowno=user_sheet.find(str(update.message.chat.id)).row
	bmi= user_sheet.acell('O{}'.format(str(rowno))).value
	coach_row=sheet.find(user_sheet.acell('B{}'.format(str(rowno))).value).row
	coach_data=sheet.row_values(coach_row)
	update.message.reply_text('Parabéns <b>{}</b>\n\n'
'Acabou de concluir a avaliação de Bem-estar Online com sucesso!\n\n Análise concluída ✅\n\n'
'O seu Índice de Massa Corporal, vai revelar se o seu Peso está acima, '
'normal ou abaixo dos padrões de saúde.\n\n <b>RESULTADO:</b>\n'
'O seu <b>IMC</b> é: <b>{}</b>\n\n'
'Veja abaixo o que isto significa? 🤔'.format(get_name(update),bmi),parse_mode="HTML")
	sleep(5)
	update.message.reply_photo(photo=open("6.png","rb"))
	sleep(5)
	update.message.reply_text('Significa que se considerarmos que o <b>IMC ideal</b> é entre 18.6 e '
'24.9 e o seu é <b>{}</b>, só terá que ver a sua '
'classificação na imagem acima. 👆'.format(bmi),parse_mode="HTML")
	sleep(9)
	reply_keyboard=[['ESTOU E MUITO'],['ESTAVA A CONTAR']]
	update.message.reply_text('<b>Está surpreendido(a) com o resultado?</b>',parse_mode="HTML",reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True,resize_keyboard=True))
	return ENDBREAK

def end_break2(update,context):
	rowno=user_sheet.find(str(update.message.chat.id)).row
	coach_row=sheet.find(user_sheet.acell('B{}'.format(str(rowno))).value).row
	coach_data=sheet.row_values(coach_row)	
	print("hi")
	update.message.reply_text('Também pode ver na tabela abaixo, quantos <b>KG</b> deveria de ter, '
'só terá que enquadrar com a sua constituição: pequena; média '
'e grande e terá o peso ideal. ',parse_mode="HTML")
	update.message.reply_photo(photo=open("7.png","rb"))
	sleep(15)
	update.message.reply_photo(photo=open("2.png","rb"))
	sleep(7)
	update.message.reply_text('Aqui está o EBOOK, <b>“A nova ciência para Perder Gordura e não voltar a ganhá-la”.</b> Só '
'terá que fazer o download, vai adorar o que vai aprender.\n'
'👇👇👇👇👇👇',parse_mode="HTML")
	sleep(5)
	update.message.reply_text('<a href="https://drive.google.com/u/0/uc?id=1ls5MVWSIk9HzUH1dUIURZAgSM86Zjz3i&export=download">Clique aqui para download – <b>EBOOK – “A Nova Ciência para Perder Gordura e não voltar a Ganhá-la”</b></a>',parse_mode="HTML")
	sleep(15)
	update.message.reply_text('Queremos ajuda-lo(a) atingir os resultados que pretende '
'<b>({})</b> mas para isso necessitamos de '
'implementar pequenas mudanças alimentares..\n'
'Mudanças que muitas pessoas desconhecem 👍'.format(user_sheet.acell('D{}'.format(str(rowno))).value),parse_mode="HTML")
	sleep(8)
	update.message.reply_text('Aqui é que entra o nosso papel, como <b>Coach de Nutrição</b>, para '
'o(a) ajudar a fazer uma reeducação alimentar definitiva e '
'aprender a comer para sempre!\n\n'
'Mas concorda comigo que hoje em dia os alimentos tem muitos '
'pesticidas e muito poucos nutrientes… o que faz com que seja '
'difícil conseguir manter resultados duradouros sem passar fome. \n\nPor isso a necessidade de <b>usar suplementos</b>, para colmatar as '
'deficiências nutricionais dos alimentos e ajudar a <b>baixar calorias.</b>',parse_mode="HTML")
	sleep(8)
	reply_keyboard=[['SIM, JÁ USEI'],['OUVI FALAR'],['NÃO CONHEÇO']]
	update.message.reply_text('Nós representamos a maior Empresa de Nutrição do Mundo, que se chama <b>Herbalife Nutrition</b>, já conhece?',parse_mode="HTML",reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True,resize_keyboard=True))
	return FINISHBREAK

def middle_break3(update,context):
	rowno=user_sheet.find(str(update.message.chat.id)).row
	coach_row=sheet.find(user_sheet.acell('B{}'.format(str(rowno))).value).row
	coach_data=sheet.row_values(coach_row)	
	sleep(8)
	update.message.reply_text('<b>A Herbalife Nutrition é a Empresa líder Mundial nesta área:</b>\n'
'✅ Mais de 40 anos no mercado\n\n'
'✅ Presente em mais de 94 Países\n\n'
'✅ Única Empresa de nutrição com um prémio Nobel da Medicina\n\n'
'✅ Mais de 300 Médicos e Cientistas\n\n'
'✅ 30 dias de garantia de satisfação\n\n'
'✅ Acompanhamento personalizado\n\n'
'✅ Grupos Online de motivação\n\n'
'✅ Líder Mundial de Nutrição e controlo de peso.',parse_mode="HTML")
	sleep(12)
	update.message.reply_photo(photo=open("8.png","rb"))
	sleep(8)
	update.message.reply_text('Mais de 250 equipas e atletas de renome Mundial '
'patrocinados, como é o caso do Cristiano Ronaldo um dos '
'melhores desportistas de todos os tempos.')
	sleep(8)
	update.message.reply_photo(photo=open("9.png","rb"))
	sleep(8)
	update.message.reply_text('Certamente quer saber como pode atingir os <b>RESULTADOS</b> que milhões de pessoas à '
'volta do Mundo conseguiram!\n\n'
'Conheça abaixo alguns <b>RESULTADOS</b> de pessoas que tiveram resultados incríveis, você '
'poderá ser a próxima pessoa!',parse_mode="HTML")
	sleep(8)
	update.message.reply_photo(photo=open("3.png","rb"))
	update.message.reply_photo(photo=open("4.png","rb"))
	update.message.reply_photo(photo=open("13.png","rb"))
	update.message.reply_photo(photo=open("11.png","rb"))
	kb=[[InlineKeyboardButton('PERDER PESO',url="https://"+coach_data[6]+".nutricaosaudavel.net/perder-peso.php")],
 	[InlineKeyboardButton('AUMENTAR DE PESO',url="https://"+coach_data[6]+".nutricaosaudavel.net/aumentar-peso.php")],
 	[InlineKeyboardButton('MELHORAR BEM-ESTAR',url="https://"+coach_data[6]+".nutricaosaudavel.net/bem-estar.php")],
	[InlineKeyboardButton('+ PERFORMANCE DESPORTIVA',url="https://"+coach_data[6]+".nutricaosaudavel.net/desporto.php")]]
	update.message.reply_text('<b>ESCOLHA UMA OPÇÃO PARA CONHECER O SEU PLANO NUTRICIONAL E COMO PODE '
'PARTICIPAR NA MARATONA SAUDÁVEL 10 DIAS!</b>\n\n'
'E após clicar num botão abaixo, será direcionado(a) para um site altamente explicativo '
'de como pode atingir os RESULTADOS que pretende!\n\n'

'👇👇👇👇👇👇👇👇👇👇',parse_mode="HTML")
	sleep(8)
	update.message.reply_photo(photo=open("12.png","rb"))
	sleep(8)
	update.message.reply_text('👇👇👇👇👇👇👇👇👇👇',reply_markup=InlineKeyboardMarkup(kb,one_time_keyboard=True))
	sleep(8)
	sleep(8)
	update.message.reply_text('Qualquer dúvida não hesite em contactar o seu Coach Pessoal, pois sou apenas um '
'ROBOT 🤖☺\n\n'
'Até amanhã, com o nosso primeiro vídeo incrível, fique atento(a) \n\n'
'<b>{}\n'
'Telm: {}</b>\n\n'
'https://{}.nutricaosaudavel.net/objetivo.php'.format(coach_data[2],coach_data[4],coach_data[6]),parse_mode="HTML")
	return ConversationHandler.END

def echo(update,context):
	query=update.callback_query
	query.answer()
	if query.data == '/see_results':
		results(query,context)

def stop(update,context):
	rowno=user_sheet.find(str(update.message.chat.id)).row
	coach_row=sheet.find(user_sheet.acell('B{}'.format(str(rowno))).value).row
	coach_data=sheet.row_values(coach_row)
	user_sheet.update('C{}'.format(str(rowno)),'InActive')
	update.message.reply_text('Temos pena que nos vá abandonar 😭, mas a qualquer '
'momento pode voltar 😜.\n\n'
'Para voltar a receber conteúdo exclusivo sobre Nutrição, só '
'terá que clicar aqui => /start\n\n'
'Para esclarecimentos adicionais, contacte o seu Nutrition '
'Coach\n\n'
'<b>{}</b>\n'
'Telm: {}\n\n'
'https://{}.nutricaosaudavel.net/objetivo.php'.format(coach_data[2],coach_data[4],coach_data[6]),parse_mode="HTML")
	return ConversationHandler.END


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN,use_context=True)
 
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
 
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),CommandHandler('evaluation', evaluate_now)],
 
        states={
            CODE: [MessageHandler(Filters.regex('[A-Za-z0-9]'), code)],
 
            EVALUATION: [MessageHandler(Filters.regex('QUERO FAZER AVALIAÇÃO MAIS TARDE'), evaluate_later),
                    MessageHandler(Filters.regex('SIM QUERO FAZER AVALIAÇÃO AGORA'), evaluate_now)],

            GOAL: [MessageHandler(Filters.regex('PERDER PESO'), goal1),
                    MessageHandler(Filters.regex('AUMENTAR DE PESO'), goal2),
                    MessageHandler(Filters.regex('MELHORAR BEM-ESTAR'), goal3),
                    MessageHandler(Filters.regex('PERFORMANCE DESPORTIVA'), goal4)],

            GOAL_ACHIEVING: [MessageHandler(Filters.regex('[A-Za-z0-9 ]'), goal_achieving)],
            BREAKFAST: [MessageHandler(Filters.regex('[A-Za-z0-9 ]'), breakfast)],
            IMP_BREAKFAST: [MessageHandler(Filters.regex('[A-Za-z0-9 ]'), imp_breakfast)],
            AGE: [MessageHandler(Filters.regex('^[0-9]+$'), age)],
            HEIGHT: [MessageHandler(Filters.regex('^[0-9.]+$'), height)],
            WEIGHT: [MessageHandler(Filters.regex('^[0-9.]+$'), weight)],
            MOTIVATION: [MessageHandler(Filters.regex('[A-Za-z0-9]'), motivation)],
            PHONE: [MessageHandler(Filters.regex('^[+0-9]+$'), phone),
            		MessageHandler(Filters.regex('[A-Za-z]+$'), wrong_phone)],
            RESULTS: [MessageHandler(Filters.regex('VER RESULTADO AGORA >>'),results)],
            BREAK: [MessageHandler(Filters.regex('[A-Za-z0-9 ]'), middle_break1),
                    MessageHandler(Filters.regex('[A-Za-z0-9 ]'), middle_break1)],
            ENDBREAK: [MessageHandler(Filters.regex('[A-Za-z0-9 ]'), end_break2),
                    MessageHandler(Filters.regex('[A-Za-z0-9 ]'), end_break2)],
            FINISHBREAK: [MessageHandler(Filters.regex('[A-Za-z0-9 ]'), middle_break3),
                    MessageHandler(Filters.regex('[A-Za-z0-9 ]'), middle_break3),
                    MessageHandler(Filters.regex('[A-Za-z0-9 ]'), middle_break3)],
                    
        },
 
        fallbacks=[CommandHandler('stop', stop)]
    )


    dp.add_handler(conv_handler)
    dp.add_handler(CallbackQueryHandler(echo))
    dp.add_handler(CommandHandler('stop', stop))
 
    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://nutritionbot23.herokuapp.com/{}'.format(TOKEN))
    # updater.bot.setWebhook('https://50ed665f45f4.ngrok.io/{}'.format(TOKEN))
 
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
 
 
if __name__ == '__main__':
    main()