import time as tempo
import subprocess
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import date
from datetime import time
from bs4 import BeautifulSoup as btfs

endTimeValidacao = ''
ultimoEndTime = ''

def fim_canal(horasArmazenadas, pordia, calendario, channelId):
    pordia.append(horasArmazenadas)
    horasTotaisCanal = 0
    print("\n")
    for item in range(len(calendario)):
        teste = td(seconds = pordia[item])
        print("No dia ",calendario[item].strftime('%d-%m-%Y'), " este é o tempo total de gravações armazenadas: ", teste)
        horasTotaisCanal += pordia[item]
    tempoTotalArmazenado = str(td(seconds=horasTotaisCanal))
    tempoTotalArmazenado = tempoTotalArmazenado.replace('days','dias')
    print("\n")
    print("Tempo total de gravações armazenadas: ", tempoTotalArmazenado)
    print("Finalizada a consulta para o canal ", channelId.replace('01',''))
    return

def calculoHorasArmanazenadas(listaHoras, horasArmazenadas):
    listaHoras = listaHoras.split(":")
    return (horasArmazenadas + (int(listaHoras[0])*3600)+(int(listaHoras[1])*60)+int(listaHoras[2]))

def criaObjDt(listaData, periodo):
    listaData = listaData.split("-")
    if periodo == "fim":
        return dt(int(listaData[0]),int(listaData[1]),int(listaData[2]),23,59,59)
    elif periodo == "inicio":
        return dt(int(listaData[0]),int(listaData[1]),int(listaData[2]),0,0,0)

def retorna_date_time (timeStamp):
    timeStamp = timeStamp.replace("T"," ")
    timeStamp = timeStamp.replace("Z","")
    timeStamp = timeStamp.replace("-"," ")
    timeStamp = timeStamp.replace(":"," ")
    listaObjDt = timeStamp.split()
    timeStamp = dt(int(listaObjDt[0]),int(listaObjDt[1]),int(listaObjDt[2]),int(listaObjDt[3]),int(listaObjDt[4]),int(listaObjDt[5]))
    listaObjDt = []
    return timeStamp

def requisicao_post(startTime ,endTimeFixo, calendario, i, pordia, horasArmazenadas,trackIdChannel):
    global ultimoEndTime
    global endTimeValidacao
    searchIdCustomizado = 301030000000 + int(trackIdChannel)*1000 + len(calendario) + int(horasArmazenadas/1000)
    requisicao = 'curl -X POST -H "Content-type: text/xml" --digest -u admin:jf@2024Emive -d "<CMSearchDescription xmlns="http://www.hikvision.com/ver20/XMLSchema"><searchID>D9834571-7965-4D46-9524-'+str(searchIdCustomizado)+'</searchID><trackList><trackID>'+trackIdChannel+'</trackID></trackList><timeSpanList><timeSpan><startTime>'+str(startTime)+'</startTime><endTime>'+str(endTimeFixo)+'</endTime></timeSpan></timeSpanList><maxResults>'+str(i)+'</maxResults><searchResultPostion>0</searchResultPostion><metadataList><metadataDescriptor>recordType.meta.hikvision.com/timing</metadataDescriptor></metadataList></CMSearchDescription>" "http://10.183.67.13:80/ISAPI/ContentMgmt/search/"'
    #-print(requisicao, "\n")
    retornoRequisicaoPost = subprocess.check_output(requisicao, shell=True, text=True)
    requisicaoParser = btfs(retornoRequisicaoPost, 'lxml-xml')
    proximoStartTime = ''
    for timeSpanTag in requisicaoParser.find_all('timeSpan'):
        itemStEt = timeSpanTag.get_text()
        objDtSt = retorna_date_time(itemStEt[:21])
        objDtEt = retorna_date_time(itemStEt[21:])
        proximoStartTime = str(itemStEt[22:])
        proximoStartTime = str(proximoStartTime[:20])
        comparacaoDatasStEt = objDtEt.date() == objDtSt.date()
        try:
            if calendario[-1] != objDtEt.date():
                calendario.append(objDtEt.date())
        except IndexError:
            calendario.append(objDtSt.date())
            if comparacaoDatasStEt == True:
                ultimoEndTime = objDtSt
            else:
                ultimoEndTime = objDtEt
        comparacaoDatasStUET = objDtSt.date() == ultimoEndTime.date()
        if comparacaoDatasStEt == True and comparacaoDatasStUET == True:
            #-print("Entrou IF")
            horasArmazenadas = calculoHorasArmanazenadas(str(objDtEt - objDtSt), horasArmazenadas)
        elif comparacaoDatasStEt == False and comparacaoDatasStUET == True:
            #-print("Entrou primeiro ELIF")
            objDtEtCorrigido = criaObjDt(str(objDtSt.date()),"fim")
            horasArmazenadas = calculoHorasArmanazenadas(str(objDtEtCorrigido - objDtSt), horasArmazenadas)
            pordia.append(horasArmazenadas)
            #-print(objDtSt,horasArmazenadas)
            objDtStCorrigido = criaObjDt(str(objDtEt.date()),"inicio")
            horasArmazenadas = calculoHorasArmanazenadas(str(objDtEt - objDtStCorrigido), 0)
            #-print(objDtEt,horasArmazenadas)
        elif comparacaoDatasStEt == True and comparacaoDatasStUET == False:
            #-print("Entrou segundo ELIF")
            pordia.append(horasArmazenadas)
            horasArmazenadas = calculoHorasArmanazenadas(str(objDtEt - objDtSt), 0)
            #-print(objDtSt,horasArmazenadas)
        if objDtEt.date() == endTimeValidacao.date():
            #-print("Entrou validação final")
            #-print(endTimeValidacao)
            #-print(objDtEt)
            diferencaEndTime = endTimeValidacao - objDtEt
            #-print(diferencaEndTime)
            #-print(len(str(diferencaEndTime)))
            if len(str(diferencaEndTime)) > 8:
                #-print("Finalização da recursividade.")
                print("\n")
                print("Time stamp da última gravação recebida ",objDtEt.strftime('%H:%M:%S %d-%m-%Y'))
                print("Time stamp de início das requisições",endTimeValidacao.strftime('%H:%M:%S %d-%m-%Y'))
                fim_canal(horasArmazenadas, pordia, calendario, listaExcecoes, trackIdChannel)
                return
            else:
                diferencaEndTime = str(diferencaEndTime).split(":")
                diferencaEndTime = (int(diferencaEndTime[0])*3600)+(int(diferencaEndTime[1])*60)+(int(diferencaEndTime[2]))
                if diferencaEndTime < (60*2):
                    print("Finalização da recursividade.")
                    print("\n")
                    print("Time stamp da última gravação recebida ",objDtEt.strftime('%H:%M:%S %d-%m-%Y'))
                    print("Time stamp de início das requisições",endTimeValidacao.strftime('%H:%M:%S %d-%m-%Y'))
                    fim_canal(horasArmazenadas, pordia, calendario, listaExcecoes, trackIdChannel)
                    return
        ultimoEndTime = objDtEt
    requisicao_post(proximoStartTime, endTimeFixo, calendario, 64, pordia, horasArmazenadas, trackIdChannel)

def requisicao_get():
    requisicao = 'curl -X GET --digest -u admin:jf@2024Emive "http://10.183.67.13:80/ISAPI/Streaming/channels/"'
    retornoRequisicaoGet = subprocess.check_output(requisicao, shell=True, text=True)
    requisicaoParser = btfs(retornoRequisicaoGet, 'lxml-xml')
    listaIds = []
    for channelId in requisicaoParser.find_all('id'):
        teste = channelId.get_text()
        if str(teste[-1]) == "1":
            listaIds.append(str(teste))
    return listaIds
        
def main():
    with open('saida.txt','w') as texto:
        texto.write('')
        texto.close()
    trackIdChannels = requisicao_get()
    dtAt = dt.now()
    stTm = dtAt - td(days=61)
    stTm = stTm.strftime('%Y-%m-%dT%H:%M:%SZ')
    endTm = dtAt.strftime('%Y-%m-%dT%H:%M:%SZ')
    global endTimeValidacao
    endTimeValidacao = retorna_date_time(endTm)
    for channelId in trackIdChannels:
        print("Iniciando a consulta para o canal ", channelId.replace('01',''))
        requisicao_post(stTm, endTm, [], 64, [], 0, channelId)
    return print("Consulta finalizada para todos os ",len(trackIdChannels)+1," canais online!")

if __name__ == '__main__':
    main()
