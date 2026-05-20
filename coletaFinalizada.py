import time as tempo
import subprocess
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import date
from datetime import time
from bs4 import BeautifulSoup as btfs

endTimeValidacao = ''
ultimoEndTime = ''
#numeroSoma = 1

def fim_canal(horasArmazenadas, pordia, calendario, listaExcecoes, channelId):
    pordia.append(horasArmazenadas)
    horasTotaisCanal = 0
    print("\n")
    for item in range(len(calendario)):
        teste = td(seconds = pordia[item])
        print("No dia ",calendario[item].strftime('%d-%m-%Y'), " este é o tempo total de gravações armazenadas: ", teste)
        horasTotaisCanal += pordia[item]
    print("\n")
    '''
    for excecao in listaExcecoes:
        print(excecao)
    '''
    tempoTotalArmazenado = str(td(seconds=horasTotaisCanal))
    tempoTotalArmazenado = tempoTotalArmazenado.replace('days','dias')
    print("\n")
    print("Tempo total de gravações armazenadas: ", tempoTotalArmazenado)
    print("Finalizada a consulta para o canal ", channelId.replace('01',''))
    #return exit()
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
def requisicao_post(startTime ,endTimeFixo, calendario, i, pordia, horasArmazenadas, listaExcecoes,trackIdChannel):
    global ultimoEndTime
    global endTimeValidacao
    searchIdCustomizado = 301030000000 + int(trackIdChannel)*1000 + len(calendario) + int(horasArmazenadas/1000)
    #global numeroSoma
    #searchIdCustomizado = trackIdChannel.replace('01','')
    #if len(searchIdCustomizado) == 1:
        #searchIdCustomizado = str(numeroSoma)+'0'+searchIdCustomizado
    #else:
        #searchIdCustomizado = str(numeroSoma)+searchIdCustomizado
    #requisicao = 'curl -X POST -H "Content-type: text/xml" --digest -u admin:jf@2024Emive -d "<CMSearchDescription xmlns="http://www.hikvision.com/ver20/XMLSchema"><searchID>D9834571-7965-4D46-9524-000000000'+searchIdCustomizado+'</searchID><trackList><trackID>'+trackIdChannel+'</trackID></trackList><timeSpanList><timeSpan><startTime>'+str(startTime)+'</startTime><endTime>'+str(endTimeFixo)+'</endTime></timeSpan></timeSpanList><maxResults>'+str(i)+'</maxResults><searchResultPostion>0</searchResultPostion><metadataList><metadataDescriptor>recordType.meta.hikvision.com/timing</metadataDescriptor></metadataList></CMSearchDescription>" "http://10.183.67.13:80/ISAPI/ContentMgmt/search/"'
    requisicao = 'curl -X POST -H "Content-type: text/xml" --digest -u usuario:senha -d "<CMSearchDescription xmlns="http://www.hikvision.com/ver20/XMLSchema"><searchID>D9834571-7965-4D46-9524-'+str(searchIdCustomizado)+'</searchID><trackList><trackID>'+trackIdChannel+'</trackID></trackList><timeSpanList><timeSpan><startTime>'+str(startTime)+'</startTime><endTime>'+str(endTimeFixo)+'</endTime></timeSpan></timeSpanList><maxResults>'+str(i)+'</maxResults><searchResultPostion>0</searchResultPostion><metadataList><metadataDescriptor>recordType.meta.hikvision.com/timing</metadataDescriptor></metadataList></CMSearchDescription>" "http://10.183.67.13:80/ISAPI/ContentMgmt/search/"'
    print(requisicao, "\n")
    #numeroSoma += 1
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
        '''  
        #-comparacaoStringsUETSt = True
        comparacaoStringsUETSt = str(objDtSt) == str(ultimoEndTime)
        #-print(ultimoEndTime)
        #-print(objDtSt)
        #-print(objDtEt)
        match comparacaoStringsUETSt:
            case False:
                
                print(objDtSt)
                print(ultimoEndTime)
                validacaoExcecoes = str(objDtSt - ultimoEndTime)
                print(validacaoExcecoes)
                validacaoExcecoes = validacaoExcecoes.split(':')
                print(validacaoExcecoes)
                validacaoExcecoes = (int(validacaoExcecoes[0])*3600)+(int(validacaoExcecoes[1])*60)+int(validacaoExcecoes[2])
                print(validacaoExcecoes)
                if validacaoExcecoes > 20:
                    listaExcecoes.append("Exceção de gravação entre "+str(ultimoEndTime.date().strftime('%d-%m-%Y'))+" "+str(ultimoEndTime.time())+" e "+str(objDtSt.date().strftime('%d-%m-%Y'))+" "+str(objDtSt.time()))
                
                listaExcecoes.append("Exceção de gravação entre "+str(ultimoEndTime.date().strftime('%d-%m-%Y'))+" "+str(ultimoEndTime.time())+" e "+str(objDtSt.date().strftime('%d-%m-%Y'))+" "+str(objDtSt.time()))
                #print("Exceções encontradas!\n", listaExcecoes[-1])
        '''
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
            #testeFim = str(endTimeValidacao - objDtEt)
            #-print(endTimeValidacao)
            #teste = str(endTimeValidacao.time())
            #teste = teste.split(":")
            #print(teste)
            #teste = teste[0]+teste[1]+teste[2]
            #-print(objDtEt)
            #teste2 = str(objDtEt.time())
            #teste2 = teste2.split(":")
            #print(teste2)
            #teste2 = teste2[0]+teste2[1]+teste2[2]
            diferencaEndTime = endTimeValidacao - objDtEt
            #a = input("Validacao")
            #-print(diferencaEndTime)
            #-print(len(str(diferencaEndTime)))
            if len(str(diferencaEndTime)) > 8:
                #-print("Finalização da recursividade.")
                print("\n")
                print("Time stamp da última gravação recebida ",objDtEt.strftime('%H:%M:%S %d-%m-%Y'))
                print("Time stamp de início das requisições",endTimeValidacao.strftime('%H:%M:%S %d-%m-%Y'))
                #a = input("Validacao")
                fim_canal(horasArmazenadas, pordia, calendario, listaExcecoes, trackIdChannel)
                return
            else:
                diferencaEndTime = str(diferencaEndTime).split(":")
                #print(diferencaEndTime)
                diferencaEndTime = (int(diferencaEndTime[0])*3600)+(int(diferencaEndTime[1])*60)+(int(diferencaEndTime[2]))
                #print(diferencaEndTime)
                if diferencaEndTime < (60*2):
                    print("Finalização da recursividade.")
                    print("\n")
                    print("Time stamp da última gravação recebida ",objDtEt.strftime('%H:%M:%S %d-%m-%Y'))
                    print("Time stamp de início das requisições",endTimeValidacao.strftime('%H:%M:%S %d-%m-%Y'))
                    #a = input("Validacao")
                    fim_canal(horasArmazenadas, pordia, calendario, listaExcecoes, trackIdChannel)
                    return
            #if :
                #a = input("Comparação ok!")
            '''
            if teste2 >= teste:
                print(endTimeValidacao,objDtEt)
                a = input("Pare")
                print("Finalização da recursividade.")
                print("\n")
                print("Time stamp da última gravação recebida ",objDtEt.strftime('%H:%M:%S %d-%m-%Y'))
                print("Time stamp do início da requisição",endTimeValidacao.strftime('%H:%M:%S %d-%m-%Y'))
                fim_canal(horasArmazenadas, pordia, calendario, listaExcecoes, trackIdChannel)
                return
            '''
            '''
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
                    fim_canal(horasArmazenadas, pordia, calendario, listaExcecoes, trackIdChannel)
                    return
            except ValueError:
                print("Finalização da recursividade.")
                print("\n")
                print("Time stamp da última gravação recebida ",objDtEt.strftime('%H:%M:%S %d-%m-%Y'))
                print("Time stamp do início da requisição",endTimeValidacao.strftime('%H:%M:%S %d-%m-%Y'))
                fim_canal(horasArmazenadas, pordia, calendario, listaExcecoes, trackIdChannel)
                return
            '''
        ultimoEndTime = objDtEt
            
    requisicao_post(proximoStartTime, endTimeFixo, calendario, 64, pordia, horasArmazenadas, listaExcecoes,trackIdChannel)

def requisicao_get():
    requisicao = 'curl -X GET --digest -u usuario:senha "http://10.183.67.13:80/ISAPI/Streaming/channels/"'
    '''
    Retorna os canais ativos do dispositivo.
    Canais offline são desconsiderados.
    '''
    #print(requisicao, "\n")
    #print(requisicao)
    retornoRequisicaoGet = subprocess.check_output(requisicao, shell=True, text=True)
    requisicaoParser = btfs(retornoRequisicaoGet, 'lxml-xml')
    listaIds = []
    for channelId in requisicaoParser.find_all('id'):
        #print(channelId)
        teste = channelId.get_text()
        #print(teste)
        #print(teste[-1])
        if str(teste[-1]) == "1":
            listaIds.append(str(teste))
            #print(teste)
    #for ids in listaIds:
    #if len(listaIds) < 0:
    return listaIds
        
def main():
    with open('saida.txt','w') as texto:
        texto.write('')
        texto.close()
    trackIdChannels = requisicao_get()
    dtAt = dt.now()
    stTm = dtAt - td(days=61)
    #stTm = dtAt - td(days=31)
    #stTm = dtAt - td(days=15)
    #stTm = dtAt - td(days=7)
    stTm = stTm.strftime('%Y-%m-%dT%H:%M:%SZ')
    endTm = dtAt.strftime('%Y-%m-%dT%H:%M:%SZ')
    global endTimeValidacao
    endTimeValidacao = retorna_date_time(endTm)
    #requisicao_post(stTm, endTm, [], 64, [], 0, [], str(101))
    #'''
    #-print(len(trackIdChannels)+1)
    #-print(trackIdChannels)
    #-a = input("Pare")
    for channelId in trackIdChannels:
        print("Iniciando a consulta para o canal ", channelId.replace('01',''))
        requisicao_post(stTm, endTm, [], 64, [], 0, [],channelId)
        #global numeroSoma
        #numeroSoma = 1
        #return
    #'''
    return print("Consulta finalizada para todos os ",len(trackIdChannels)+1," canais online!")

if __name__ == '__main__':
    main()
