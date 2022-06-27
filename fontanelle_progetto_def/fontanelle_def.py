#
#
# File: fontanelle
# Authors: Talha Imran, Kasun Rajapaksha, Gianmario Fiorini, Shady Khalaile, Cristian Motoc
# Date: 27/06/2022
# Description: ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
##Il nostro bot sarà la salvezza per quelle persone o animali che stanno morendo di sete, 
##questo bot ti consentirà di vedere una mappa di tutte le fontanelle, oppure dirti la posizione della fontana più vicina,
##con la quale poi potresti, volendo, avere indicazioni tramite google maps.
##Tutto questo sia in Italiano che in Inglese!
##Buona bevuta sostenibile! :)
##////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
##Our bot is going be the saving for those people of animals that are dying of thirst,
##this bot will allow you to see a map of all public fountain, or telling you the position of the nearest fountain to you,
##and use google maps to get to it.
##All this both in Italian and in English!
##Have a good drink! :)
##////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

from subprocess import IDLE_PRIORITY_CLASS
from telegram import *
from telegram.ext import *
from math import radians, cos, sin, asin, sqrt
import time
from csvmng.csvmng import CSVManager
import sqlite3
from requests import *
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Fontanelle_Verona")
location = geolocator.geocode("Via Franceschine")
print(location.address)
print((location.latitude, location.longitude))

#var of bottons#
Italiano = "Italiano  🇮🇹"
Fvicina_it = "Indicazioni per la fontanella più vicina  ➤"
Fverona_it = "Mappa delle fontanelle di Verona  🗺"
Ritorno_it="Cambia lingua  ⇦"
English = "English 🇬🇧 / 🇺🇸"
Fvicina_en = "Directions to the nearest drikning fountain ➤"
Fverona_en = "Map of Verona's drinking fountains 🗺"
Ritorno_en="Change language ⇦"

###############
##def get_loc(street:str)->str:
##    geolocator=Nominatim(user_agent="Fontanelle_Verona")
##    location=geolocator.geocode(street)
##    return location.longitude,location.latitude


####funtions###
def mappa_it(update: Update, context: CallbackContext):
    update.message.reply_text(
    'Fontanelle presenti a Verona:/nlink esterno alla mappa di tutte le fontanelle di Verona',
    reply_markup=InlineKeyboardMarkup([
    [InlineKeyboardButton(text='mappa', url='http://u.osmfr.org/m/780217/')],]))

def mappa_en(update: Update, context: CallbackContext):
    update.message.reply_text(
    'Fountains of Verona:/nexternal link to the map of all the fountains in Verona',
    reply_markup=InlineKeyboardMarkup([
    [InlineKeyboardButton(text='map', url='http://u.osmfr.org/m/780217/')],]))


def dist(lat1,lon1, lat2, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return((c * r)*1000)

def startCommand(update: Update, context: CallbackContext) -> None:
    buttons = [[KeyboardButton(English)], [KeyboardButton(Italiano)]]
    testo = "!WELCOME!"
    context.bot.send_message(chat_id=update.effective_chat.id, text=testo, reply_markup=ReplyKeyboardMarkup(buttons))

def messageHandler(update: Update, context: CallbackContext):
    
    global lingua
    #Italiano
    if Italiano in update.message.text:
        lingua = "it"
        buttons = [[KeyboardButton(Fvicina_it)], [KeyboardButton(Fverona_it)], [KeyboardButton(Ritorno_it)]]
        context.bot.send_message(chat_id=update.effective_chat.id, text="Benvenuto!!!\nQuesto bot ti permette di trovare la fontanella più vicina a te.", reply_markup=ReplyKeyboardMarkup(buttons))

    if Fvicina_it in update.message.text:   
        testo = "Invia la tua posizione."
        context.bot.send_message(chat_id=update.effective_chat.id, text=testo)
        dispatcher.add_handler(MessageHandler(Filters.location, distanza))

    if Fverona_it in update.message.text:
        mappa_it(update, context)

    if Ritorno_it in update.message.text:
        lingua = ""
        buttons = [[KeyboardButton(English)], [KeyboardButton(Italiano)]]
        testo = "!BENVENUTO!"
        context.bot.send_message(chat_id=update.effective_chat.id, text=testo, reply_markup=ReplyKeyboardMarkup(buttons))

    #Inglese
    if English in update.message.text:
        lingua = "en"
        buttons = [[KeyboardButton(Fvicina_en)], [KeyboardButton(Fverona_en)],[KeyboardButton(Ritorno_en)]]
        context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome !!! \nThis bot allows you to find the fountain closest to you.", reply_markup=ReplyKeyboardMarkup(buttons))
    
    if Fvicina_en in update.message.text:
        testo = "Send your position "
        context.bot.send_message(chat_id=update.effective_chat.id, text=testo)
        #dispatcher.stop()
        dispatcher.add_handler(MessageHandler(Filters.location, distanza))

    if Fverona_en in update.message.text:
        mappa_en(update, context)

    if Ritorno_en in update.message.text:
        lingua = ""
        buttons = [[KeyboardButton(English)], [KeyboardButton(Italiano)]]
        testo = "!WELCOME!"
        context.bot.send_message(chat_id=update.effective_chat.id, text=testo, reply_markup=ReplyKeyboardMarkup(buttons))
    
                                 
def distanza(update: Update, context: CallbackContext) -> None:
    try:
        lat1 = update.message.location.latitude
        lon1 = update.message.location.longitude
        d = []
        for i in range(0,len(coord_x)):
            d.append(dist(lat1,lon1,coord_x[i],coord_y[i]))
        print(lat1,lon1)
        print(coord_x[i],coord_y[i])
        e = d[:]
        d.sort()
        ind = 0
        for i in range(0,len(d)):
            if d[0]==e[i]:
                ind = i
                break
        if lingua == "it":
            testo_via = "La fontanella più vicina è: " + nome_via[ind]
            testo_dist = "\nDistanza: " + str(round(d[0],2)) + " m"
            testo_CIRCOSCRIZIONI= "\ncircoscrizioni: " + circoscrizioni[ind]
            testo_denominazioni= "\ndenominazione: " + denominazioni[ind]
            context.bot.send_message(chat_id=update.effective_chat.id, text=testo_via+testo_CIRCOSCRIZIONI+testo_denominazioni+testo_dist)
            update.message.reply_location(coord_x[i], coord_y[i])
        elif lingua == "en":
            testo_via = "The closest fontanel is: " + nome_via[ind]
            testo_dist = "\nDistance: " + str(round(d[0],2)) + " m"
            testo_CIRCOSCRIZIONI= "\nCircumscriptions: " + circoscrizioni[ind]
            testo_denominazioni= "\nName: " + denominazioni[ind]
            context.bot.send_message(chat_id=update.effective_chat.id, text=testo_via+testo_CIRCOSCRIZIONI+testo_denominazioni+testo_dist)
            update.message.reply_location(coord_x[i], coord_y[i])
    except:
        #print(exception)
        testo_try = "Attenzione!!!\nInviare solo la posizione attuale.\nInterrompere la condivisione della posizione in tempo reale."
        context.bot.send_message(chat_id=update.effective_chat.id, text=testo_try)

def echo(update: Update, context: CallbackContext) -> None:
    testo = "Error 404"
    context.bot.send_message(chat_id=update.effective_chat.id, text=testo)

#main#   
def main():
    #updater = Updater("5592213185:AAHHK0F0zr_lLSxPqEVTMz2u0DJomafblQQ")
    with open("token.txt", "r") as f:
        TOKEN = f.read()
    updater = Updater(TOKEN)
    print(updater)
    global dispatcher
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", startCommand))
    dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    ##var_of_array##
    nome_via=[]
    circoscrizioni=[]
    denominazioni=[]
    coord_x = []
    coord_y = []

    con = sqlite3.connect("fontanelle.db")
    a=con.execute(""" SELECT NOME_VIA FROM fontanelle_def; """).fetchall()
    #print(a)
    b=con.execute(""" select CIRCOSCRIZ from fontanelle_def; """).fetchall()
    #print(b)
    c=con.execute(""" select DENOMINAZI from fontanelle_def; """).fetchall()
    #print(c)
    d=con.execute(""" SELECT coordinate_x FROM fontanelle_def; """).fetchall()
    #print(d)
    e=con.execute(""" SELECT coordinate_y FROM fontanelle_def; """).fetchall()
    #print(e)

    for i in range(0,len(a)):
        nome_via.append(a[i][0])
        circoscrizioni.append(b[i][0])
        denominazioni.append(c[i][0])
        coord_x.append(e[i][0])
        coord_y.append(d[i][0])

    main()



