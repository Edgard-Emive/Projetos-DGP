import time as tempo
import subprocess
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import date
from datetime import time
from bs4 import BeautifulSoup as btfs
endTimeValidacao = ''
ultimoEndTime = ''
def fim(horasArmazenadas, pordia, calendario, listaExcecoes):
    pordia.append(horasArmazenadas)
    print("\n")
    for item in range(len(calendario)):
        teste = td(seconds = pordia[item])
        print("No dia ",calendario[item].strftime('%d-%m-%Y'), " este é o tempo total de gravações armazenadas: ", teste)
    print("\n")
    for excecao in listaExcecoes:
        print(excecao)
    print("\n")
    print("Finalizado")
    exit()
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
def requisicao_post_teste(startTime ,endTimeFixo, calendario, i, pordia, horasArmazenadas, listaExcecoes):
    global ultimoEndTime
    global endTimeValidacao
    requisicao = 'curl -X POST -H "Content-type: text/xml" --digest -u admin:jf@2024Emive -d "<CMSearchDescription xmlns="http://www.hikvision.com/ver20/XMLSchema"><searchID>D9834571-7965-4D46-9524-000000000004</searchID><trackList><trackID>101</trackID></trackList><timeSpanList><timeSpan><startTime>'+str(startTime)+'</startTime><endTime>'+str(endTimeFixo)+'</endTime></timeSpan></timeSpanList><maxResults>'+str(i)+'</maxResults><searchResultPostion>0</searchResultPostion><metadataList><metadataDescriptor>recordType.meta.hikvision.com/timing</metadataDescriptor></metadataList></CMSearchDescription>" "http://10.183.67.13:80/ISAPI/ContentMgmt/search/"'
    print(requisicao)
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
        comparacaoStringsUETSt = str(objDtSt) == str(ultimoEndTime)
        print(ultimoEndTime)
        print(objDtSt)
        print(objDtEt)
        match comparacaoStringsUETSt:
            case False:
                listaExcecoes.append("Exceção de gravação entre "+str(ultimoEndTime.date().strftime('%d-%m-%Y'))+" "+str(ultimoEndTime.time())+" e "+str(objDtSt.date().strftime('%d-%m-%Y'))+" "+str(objDtSt.time()))
                print("Exceções encontradas!\n", listaExcecoes[-1])
        if comparacaoDatasStEt == True and comparacaoDatasStUET == True:
            print("Entrou IF")
            horasArmazenadas = calculoHorasArmanazenadas(str(objDtEt - objDtSt), horasArmazenadas)
        elif comparacaoDatasStEt == False and comparacaoDatasStUET == True:
            print("Entrou primeiro ELIF")
            objDtEtCorrigido = criaObjDt(str(objDtSt.date()),"fim")
            horasArmazenadas = calculoHorasArmanazenadas(str(objDtEtCorrigido - objDtSt), horasArmazenadas)
            pordia.append(horasArmazenadas)
            print(objDtSt,horasArmazenadas)
            objDtStCorrigido = criaObjDt(str(objDtEt.date()),"inicio")
            horasArmazenadas = calculoHorasArmanazenadas(str(objDtEt - objDtStCorrigido), 0)
            print(objDtEt,horasArmazenadas)
        elif comparacaoDatasStEt == True and comparacaoDatasStUET == False:
            print("Entrou segundo ELIF")
            pordia.append(horasArmazenadas)
            horasArmazenadas = calculoHorasArmanazenadas(str(objDtEt - objDtSt), 0)
            print(objDtSt,horasArmazenadas)
        if objDtEt.date() == endTimeValidacao.date():
            print("Entrou validação final")
            testeFim = str(endTimeValidacao - objDtEt)
            print(testeFim)
            testeFim = testeFim.split(":")
            try:
                validacaoFim = (int(testeFim[0])*3600)+(int(testeFim[1])*60)+int(testeFim[2])
                print(validacaoFim)
                if validacaoFim < 90:
                    print("Finalização da recursividade.")
                    print("\n")
                    print("Time stamp da última gravação recebida ",objDtEt.strftime('%H:%M:%S %d-%m-%Y'))
                    print("Time stamp do início da requisição",endTimeValidacao.strftime('%H:%M:%S %d-%m-%Y'))
                    fim(horasArmazenadas, pordia, calendario, listaExcecoes)
            except ValueError:
                print("Finalização da recursividade.")
                print("\n")
                print("Time stamp da última gravação recebida ",objDtEt.strftime('%H:%M:%S %d-%m-%Y'))
                print("Time stamp do início da requisição",endTimeValidacao.strftime('%H:%M:%S %d-%m-%Y'))
                fim(horasArmazenadas, pordia, calendario, listaExcecoes)
        ultimoEndTime = objDtEt
    requisicao_post_teste(proximoStartTime, endTimeFixo, calendario, 64, pordia, horasArmazenadas, listaExcecoes)   
def main():
    with open('saida.txt','w') as texto:
        texto.write('')
        texto.close()
    dtAt = dt.now()
    stTm = dtAt - td(days=61)
    #stTm = dtAt - td(days=31)
    #stTm = dtAt - td(days=15)
    #stTm = dtAt - td(days=7)
    stTm = stTm.strftime('%Y-%m-%dT%H:%M:%SZ')
    endTm = dtAt.strftime('%Y-%m-%dT%H:%M:%SZ')
    global endTimeValidacao
    endTimeValidacao = retorna_date_time(endTm)
    requisicao_post_teste(stTm, endTm, [], 64, [], 0, [])
if __name__ == '__main__':
    main()