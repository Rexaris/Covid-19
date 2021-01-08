import urllib.request
from bs4 import BeautifulSoup
import re
import datetime
import locale
import sys
import json
import os
import matplotlib.pyplot as plt


locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
Dates=[]
Inzidenzes=[]
Infizierte=[]
Genesene=[]
Gestorbene=[]
AktuellInfizierte=[]
NeuInfektionen=[]


filePath = os.path.dirname(sys.argv[0])
dataFile=filePath+"/burgenlandkreisdeData_Burgenlandkreis_aktuell.json"

def loadFile(filename):
    try:
        with open(filename,"a+") as infile:
            infile.seek(0)
            oldData=json.load(infile)
    except json.JSONDecodeError:
        oldData=[]
        safeFile(filename,oldData)
    
    resultData=[]
    for data in oldData:#doppelte Einträge entfernen
        if data not in resultData:
            resultData.append(data)
    return resultData

def safeFile(fileName,data):
    data=sorted(data,key=lambda k:datetime.datetime(k["year"],k["month"],k["day"]),reverse=True)
    with open(fileName,"w") as outfile:
            json.dump(data,outfile,indent=4,sort_keys=True)
            print("neue Daten gespeichert")

def extractLastNumber(text):
    resultText=""
    for i in range(len(text)):
        if text[-i-1].isdigit()==True:
            resultText=text[-i-1]+resultText
            
        elif text[-i-1]!="." and len(resultText)>0:
            break
    if resultText=="":
        return -1
    return int(resultText)


def extractLastFloat(text):
    resultText=""
    for i in range(len(text)):
        if text[-i-1].isdigit()==True or text[-i-1]==",":
            resultText=text[-i-1]+resultText
            
        elif text[-i-1]!="." and len(resultText)>0:
            break
    if resultText=="":
        return -1
    return float(resultText.replace(",","."))


oldData=loadFile(dataFile)


for oData in oldData:
    oDate=datetime.datetime(oData["year"], oData["month"], oData["day"])
    oInzidenz=oData["inzidenz"]
    Dates.append(oDate)
    Inzidenzes.append(oInzidenz)
    print(oDate,oInzidenz)


fp = urllib.request.urlopen("https://corona.burgenlandkreis.de/de/coronanews/aktuelles-zum-corona-virus.html")
mybytes = fp.read()

mystr = mybytes.decode("utf8")
fp.close()

soup=BeautifulSoup(mystr,'html.parser')
ps=soup.find(class_="title").findNext().find_all("p")

tmp_i=0

try:
    first=True
    for p in ps:
        
        dates=p.find_all(string=re.compile("Update")) # nach Keyword "Update" suchen. Dies wird in jeder Überschrift verwendet
        if len(dates)==1: # nur wenn "Update" gefunden wurde
            tmp_i=tmp_i+1
            date=""
            date_txt=dates[0] #Text des Datums extrahieren
            date_words=date_txt.split(" ") # wörter des Datums extrahieren
            for date_word in date_words:
                if date_word.count(".")==2: # im "Wort" muss zweimal ein "." vorkommen damit es das Datum ist
                    for date_char in date_word: # nur Zahlen und . zulassen
                        if date_char.isdigit() or date_char==".":
                            date+=date_char
            if date[1]==".": # fehlende führende 0 beim Tag ergänzen
                date="0"+date
            if date[4]==".": # fehlende führende 0 beim Monat ergänzen
                date=date[:3]+"0"+date[3:]
            date=date[:10]# zu lange Daten abschneiden
            date_time_obj = datetime.datetime.strptime(date, '%d.%m.%Y')
            #print(date_time_obj)
            
            #if date_time_obj not in Dates: #doppelte Einträge verhindern
                
            Dates.append(date_time_obj)
            
            # if first==True or tmp_i==5:
            #     first=False
            contenti=p.next.next
            for i in range(10):#suchen bis update nicht mehr im contenti vorkommt
                #print(contenti)
                if  "Update" not in contenti:#"Update" in contenti.contents:#contenti.count("Update")==0: #str(type(contenti))=="<class 'bs4.element.NavigableString'>" and contenti.find("Update")>0 or
                    #print("noUpdate",contenti)
                    break
                #print(type(contenti),contenti)
                contenti=contenti.next
            
            #print(date_time_obj)
            Infiziert_i=-1
            Genesen_i=-1
            Gestorben_i=-1
            Inzidenz_i=-1
            for i in range(150): # nach Daten suchen, maximal 50 mal weitergehen
                if "Update" in contenti:
                    #print("break:", contenti)
                    break
                if "Anzahl" in contenti:
                    if "Infiziert" in contenti:
                        Infiziert_i=extractLastNumber(contenti)
                        #print("Infiziert:", Infiziert_i)
                        
                    if "Genesen" in contenti:
                        Genesen_i=extractLastNumber(contenti)
                        #print("Genesen:", Genesen_i)
                    if "Gestorben" in contenti:
                        Gestorben_i=extractLastNumber(contenti)
                        #print("Gestorbene:",  Gestorben_i)
                    #print(contenti)
                if "Burgenlandkreises)[1]:" in contenti:#nach Inzidenz-Zeile suchen
                    #print(date_time_obj)
                    contenti2=contenti
                    for j in range(4):
                        #print(contenti2)
                        tmpcontenti="NIX"
                        if "(Stand" in contenti2:
                            iSuffix=contenti2.find("(Stand")
                            #print("SUffix_",iSuffix)
                            tmpcontenti=str(contenti2[:iSuffix])
                            break
                        
                        if "," in contenti2:
                            
                            ikommaPos=contenti2.find(",")
                            if len(contenti2)>7:
                                tmpcontenti=contenti2[ikommaPos-3:ikommaPos+3]
                            else:
                                tmpcontenti=contenti2
                           # print("komma Found:", contenti2 ,tmpcontenti)
                            break
                        
                        contenti2=contenti2.next
                        
                        
                        
                    if tmpcontenti=="NIX":
                        print(contenti2)
                    Inzidenz_i=extractLastFloat(tmpcontenti)        
                    #print(Inzidenz_i)
                    print()
                    
                
                contenti=contenti.next
            Infizierte.append(Infiziert_i)
            Genesene.append(Genesen_i)
            Gestorbene.append(Gestorben_i)
            Inzidenzes.append(Inzidenz_i)
               
       
except:
    print("Unexpected error:", sys.exc_info())
    
NeuInfektionen=[0]    
for i in reversed(range(len(Infizierte))):
    if i==len(Infizierte)-1:
        if Infizierte[i]==-1:
            Infizierte[i]=0
        if Genesene[i]==-1:
            Genesene[i]=0 
        if Gestorbene[i]==-1:
            Gestorbene[i]=0                 
    
    if Infizierte[i]==-1:
        Infizierte[i]=Infizierte[i+1]
    if Genesene[i]==-1:
        Genesene[i]=Genesene[i+1] 
    if Gestorbene[i]==-1:
        Gestorbene[i]=Gestorbene[i+1]
    AktuellInfizierte.insert(0,Infizierte[i]-Genesene[i]-Gestorbene[i])
    if i<len(Infizierte)-1:
        NeuInfektionen.insert(0,Infizierte[i]-Infizierte[i+1])
        


    
    
# for i in range(len(Infizierte)):
#     print(Dates[i])
#     print(Infizierte[i])
#     print(Genesene[i])
#     print(Gestorbene[i])
#     print(AktuellInfizierte[i])
#     print(NeuInfektionen[i])
#     print(Inzidenzes[i])
#     print()
    
    
    
#var tmpX=new Date(tmpYear,tmpMonth-1,tmpDay,tmpHour,tmpMinute);
#%%
JSONArray=[]
for i in range(len(Inzidenzes)):
    tmpInzidenz=Inzidenzes[i]
    tmpYear=Dates[i].year
    tmpMonth=Dates[i].month
    tmpDay=Dates[i].day
    tmpHour=0
    tmpMinute=0
    if tmpInzidenz>0:
        JSONArray.append({"year":tmpYear,"month":tmpMonth,"day":tmpDay,"hour":tmpHour,"minute":tmpMinute,"inzidenz":tmpInzidenz})

safeFile(dataFile, JSONArray)

#print(Dates)
#print(Inzidenzes)
plt.plot(Dates,Infizierte,label="Infizierte")
plt.plot(Dates,Genesene,label="Genesene")
plt.plot(Dates,Gestorbene,label="Gestorbene")
plt.plot(Dates,AktuellInfizierte,label="Aktuelle Infektionen")
plt.plot(Dates,NeuInfektionen,label="Neuinfektionen")
plt.plot(Dates,Inzidenzes,label="7-Tage-Inzidenz")
plt.legend()
