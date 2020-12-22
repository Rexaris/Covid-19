import urllib.request
from bs4 import BeautifulSoup
import re
import datetime
import locale
import sys
import json
import PATH
#import matplotlib.pyplot as plt


locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
Dates=[]
Inzidenzes=[]

dataFile=PATH.filePath+"halledeData_Halle_aktuell.json"


def safeFile(fileName,data):
    data=sorted(data,key=lambda k:datetime.datetime(k["year"],k["month"],k["day"]),reverse=True)
    with open(fileName,"w") as outfile:
            json.dump(data,outfile,indent=4,sort_keys=True)
            print("neue Daten gespeichert")



IDs=["46138"]
nextID="45334"


try:
    with open(dataFile,"a+") as infile:
        infile.seek(0)
        oldData=json.load(infile)
except json.JSONDecodeError:
    oldData=[]
    safeFile(dataFile,oldData)


for oData in oldData:
    oDate=datetime.datetime(oData["year"], oData["month"], oData["day"])
    oInzidenz=oData["inzidenz"]
    Dates.append(oDate)
    Inzidenzes.append(oInzidenz)
    print(oDate,oInzidenz)
#%%

while nextID not in IDs:
    IDs.append(nextID)
    fp = urllib.request.urlopen("https://www.halle.de/de/Verwaltung/Presseportal/Nachrichten/?NewsId="+nextID)
    mybytes = fp.read()
    
    mystr = mybytes.decode("utf8")
    fp.close()
    
    soup=BeautifulSoup(mystr,'html.parser')
    ps=soup.find(class_="cms_news").find_all("p")
    nextID=soup.find(class_="next")["href"][-5:]
    
    
    try:
        first=True
        for p in ps:
            dates=p.find_all(string=re.compile("2020"))
            if len(dates)==1 and dates[0][-2]==":":
                date=dates[0]
                
                date_tmp=date[:-2]
                if date_tmp[1]==".":
                    date_tmp="0"+date_tmp
                date_time_obj = datetime.datetime.strptime(date_tmp, '%d. %B %Y')
                #print(date_time_obj)
                if date_time_obj not in Dates:
                    
                    Dates.append(date_time_obj)
                    Inzidenzes.append(0)
                    tmp=date
                    
                    for i in range(50):
                        tmp=tmp.next
                        if "nzidenz" in tmp:
                            x=tmp.find("Einwohner:")+11
                            if x>10:
                                inzidenz=float(tmp[x:x+8].split(" ")[0].replace(",","."))
                                #print(inzidenz)
                                Inzidenzes[-1]=inzidenz
                                print(date)
                                print(inzidenz)
                                print(IDs[-1])
                
                    first=False
           
    except:
        print("Unexpected error:", sys.exc_info())
#var tmpX=new Date(tmpYear,tmpMonth-1,tmpDay,tmpHour,tmpMinute);
#%%
JSONArray=[]
for i in range(len(Inzidenzes)):
    tmpInzidenz=Inzidenzes[i]
    tmpYear=Dates[i].year
    tmpMonth=Dates[i].month
    tmpDay=Dates[i].day
    tmpHour=13
    tmpMinute=0
    if tmpInzidenz>0:
        JSONArray.append({"year":tmpYear,"month":tmpMonth,"day":tmpDay,"hour":tmpHour,"minute":tmpMinute,"inzidenz":tmpInzidenz})

safeFile(dataFile, JSONArray)

#print(Dates)
#print(Inzidenzes)
#plt.plot(Dates,Inzidenzes)
