import time as tempo
'''
Importação da biblioteca "time", para acrescentar um delay com o "time.sleep('quantidade de segundos')".
Ela recebe um alias pois em seguida importamos um outro módulo com o nome "time".
'''
import subprocess
'''
Importação da biblioteca "subprocess" para enviar comandos a serem executados no prompt de comando.
'''
from datetime import datetime as dt
'''
Importação do módulo "datetime" da biblioteca "datetime", para permitir utilização de objetos do tipo "datetime".
Ele recebe um alias para facilitar a escrita de sua chamada.
'''
from datetime import timedelta as td
'''
Importação do módulo "timedelta" da biblioteca "datetime", para permitir outras operações com objetos do tipo "datetime".
Ele recebe um alias para facilitar a escrita de sua chamada.
'''
from datetime import date
'''
Importação do módulo "date" da biblioteca "datetime", para permitir retornar a data de um objeto "datetime".
'''
from datetime import time
'''
Importação do módulo "time" da biblioteca "datetime", para permitir retornar a hora de um objeto "datetime".
'''
from bs4 import BeautifulSoup as btfs
'''
Importação do módulo "BeautifulSoup" da biblioteca "bs4", para permitir a extração de dados de arquivos XML.
Ele recebe um alias pois em seguida importamos um outro módulo com o nome "time".
'''

endTimeValidacao = ''
'''
Inicializa uma variável global.
'''
ultimoEndTime = ''
'''
Inicializa uma variável global.
'''
def fim(horasArmazenadas, pordia, calendario):
    pordia.append(horasArmazenadas)
    print(pordia, len(pordia),calendario,len(calendario))
    for i in range(len(calendario)):
        print(calendario[i], pordia[i])
        return print("Finalizado")
    
def calculoHorasArmanazenadas(listaHoras, horasArmazenadas):
    listaHoras = listaHoras.split(":")
    #horasArmazenadas += (int(listaHoras[0])*3600)+(int(listaHoras[1])*60)+int(listaHoras[2])
    #return horasArmazenadas
    return horasArmazenadas + int(listaHoras[0])*3600)+(int(listaHoras[1])*60)+int(listaHoras[2]))

def criaObjDt(listaData):
    listaData = listaData.split("-")
    #objDtStCorrigido = dt(int(listaData[0]),int(listaData[1]),int(listaData[2]),0,0,0)
    #return objDtStCorrigido
    return dt(int(listaData[0]),int(listaData[1]),int(listaData[2]),0,0,0)

def retorna_date_time (timeStamp):
    timeStamp = timeStamp.replace("T"," ")
    '''
    Atualiza o valor da variável timeStamp, removendo o "T" da string.
    '''
    timeStamp = timeStamp.replace("Z","")
    '''
    Atualiza o valor da variável timeStamp, removendo o "Z" da string.
    '''
    timeStamp = timeStamp.replace("-"," ")
    '''
    Atualiza o valor da variável timeStamp, removendo os "-" da string.
    '''
    timeStamp = timeStamp.replace(":"," ")
    '''
    Atualiza o valor da variável timeStamp, removendo os ":" da string.
    '''
    listaObjDt = timeStamp.split()
    '''
    Divide a string timeStamp nos seus espaços vazios, transformando ela em uma lista e salvando na variável listaObjDt
    '''
    timeStamp = dt(int(listaObjDt[0]),int(listaObjDt[1]),int(listaObjDt[2]),int(listaObjDt[3]),int(listaObjDt[4]),int(listaObjDt[5]))
    '''
    Transforma a lista em um objeto datetime e salva ela na variável timeStamp.
    '''
    listaObjDt = []
    '''
    Libera a memória ocupada pela lista.
    '''
    return timeStamp
    '''
    Retorna o objeto datetime
    '''
def requisicao_post_teste(startTime ,endTimeFixo, calendario, i, pordia, horasArmazenadas):
    global endTimeValidacao
    '''
    Mapeia a variável global.
    '''
    global ultimoEndTime
    '''
    Mapeia a variável global.
    '''
    requisicao = 'curl -X POST -H "Content-type: text/xml" --digest -u admin:jf@2024Emive -d "<CMSearchDescription xmlns="http://www.hikvision.com/ver20/XMLSchema"><searchID>D9834571-7965-4D46-9524-000000000004</searchID><trackList><trackID>101</trackID></trackList><timeSpanList><timeSpan><startTime>'+str(startTime)+'</startTime><endTime>'+str(endTimeFixo)+'</endTime></timeSpan></timeSpanList><maxResults>'+str(i)+'</maxResults><searchResultPostion>0</searchResultPostion><metadataList><metadataDescriptor>recordType.meta.hikvision.com/timing</metadataDescriptor></metadataList></CMSearchDescription>" "http://10.183.67.13:80/ISAPI/ContentMgmt/search/"'
    '''
    Concatena o texto e algumas variáveis para montar o comando curl a ser executado.
    São adicionados o "startTime" obtido após os tratamentos abaixo,
    o "endTimeFixo", que é a data atual e
    a quantidade de objetos a serem requisitados, definidos por "i".
    '''
    retornoRequisicaoPost = subprocess.check_output(requisicao, shell=True, text=True)
    '''
    Passa a variável "requisicao" para ser executada pela biblioteca subprocess e salva o retorno da execução
    na variável "retornoRequisicaoPost".
    '''
    requisicaoParser = btfs(retornoRequisicaoPost, 'lxml-xml')
    '''
    Passa a variável "retornoRequisicaoPost" pra ser tratada pelo parser XML.
    '''
    for timeSpanTag in requisicaoParser.find_all('timeSpan'):
        '''
        Executa os seguintes comandos para cada timeSpan encontrado pelo parser.
        Cada timeSpan é um bloco de gravação.
        '''
        itemStEt = timeSpanTag.get_text()
        '''
        Extrai o texto contido dentro de timeSpan e salva na sting "itemStEt".
        Mais especificamente, extrai os textos contidos nas tags startTime e endTime.
        Os textos em questão são o início e fim do bloco de gravação atual encontrado.
        '''
        objDtSt = retorna_date_time(itemStEt[:21])
        '''
        Extrai do texto obtido o inicio do bloco de gravação e envia para a função para obter um objeto datetime.
        Em seguida, salva o objeto retornado pela função na variável "objDtSt".
        '''
        objDtEt = retorna_date_time(itemStEt[21:])
        '''
        Extrai do texto obtido o fim do bloco de gravação e envia para a função para obter um objeto datetime.
        Em seguida, salva o objeto retornado pela função na variável "objDtEt". 
        '''
        proximoStartTime = str(itemStEt[22:])
        '''
        Salva a parte do texto correspondente ao fim do bloco de gravação numa variável.
        '''
        proximoStartTime = str(proximoStartTime[:20])
        '''
        Atualiza o valor da variável timeStamp, removendo espaços vazios e quebras de linha.
        '''
        try:
            if calendario[-1] != objDtEt.date():
                calendario.append(objDtEt.date())
            '''
            Tentativa de comparação da última data adicionada à lista "calendario".
            Caso a lista não esteja vazia ( tenha pelo menos uma data adicionada nela ),
            é feita comparação entre a última data armazenada e a data atual.
            Se as datas forem diferentes, a nova data é adicionada na lista.
            Caso não sejam, nada acontece.
            '''
        except IndexError:
            calendario.append(objDtSt.date())
        '''
        Quando a lista está vazia ( na primeira execução do laço for ) a comparação retorna um erro do tipo "IndexError", nesse caso: index out of range.
        É retornado o seguinte erro pois o if tenta puxar a o elemento na última posição de uma lista vazia.
        No caso de erro, a data atual simplesmente é adicionada na lista.
        '''
        comparacaoDatasStEt = objDtEt.date() == objDtSt.date()
        comparacaoDatasStUET = objDtSt.date() == ultimoEndTime.date()
        #comparacaoDatasEtETV = objDtEt.date() == endTimeValidacao.date()
        
        
        if comparacaoDatasStEt == True and comparacaoDatasStUET == False and len(calendario) == 1:
            horasArmazenadas += calculoHorasArmanazenadas(str(objDtEt - objDtSt), horasArmazenadas)

        elif comparacaoDatasStEt == True and comparacaoDatasStUET == True:
            horasArmazenadas += calculoHorasArmanazenadas(str(objDtEt - objDtSt), horasArmazenadas)

        elif objDtEt.date() != objDtSt.date() and objDtSt.date() == ultimoEndTime.date():
            objDtEtCorrigido = criaObjDt(str(objDtSt.date())
            horasArmazenadas += calculoHorasArmanazenadas(str(objDtEtCorrigido - objDtSt), horasArmazenadas)
            pordia.append(horasArmazenadas)
            objDtStCorrigido = criaObjDt(str(objDtEt.date())
            horasArmazenadas += calculoHorasArmanazenadas(str(objDtEt - objDtStCorrigido), 0)

        elif objDtEt.date() == objDtSt.date() and objDtSt.date() != ultimoEndTime.date():
            pordia.append(horasArmazenadas)
            horasArmazenadas = calculoHorasArmanazenadas(str(objDtEt - objDtSt), 0)
        
        if objDtEt.date() == endTimeValidacao.date():
            testeFim = str(endTimeValidacao - objDtEt)
            testeFim = testeFim.split(":")
            try:
                validacaoFim = (int(testeFim[0])*3600)+(int(testeFim[1])*60)+int(testeFim[2])
                if validacaoFim < 5:
                    fim(horasArmazenadas, pordia, calendario)
            except ValueError:
                fim(horasArmazenadas, pordia, calendario)
        ultimoEndTime = objDtEt
            
    requisicao_post_teste(proximoStartTime, endTimeFixo, calendario, 64, pordia, horasArmazenadas)

def trata_lista(listaTimeStamp, listaSaida):
    if len(listaTimeStamp) == 0 :
        for itemListaSaida in listaSaida:
            with open('saida.txt','a') as texto:
                texto.write(itemListaSaida)
                texto.close()
            with open('saida.txt','r') as texto:
                print(texto.read())
                texto.close()
    else:
        input('começa a tratar')
        infosGravacao = listaTimeStamp.pop(0)
        infosGrvacao.split(' ')
        dataGravacao = infosGravacao.pop(0)
        print(dataGravacao)
        
        for itemListaTimeSpan in listaTimeSpan:
            '''
            tamanho = len(listaSaida)
            if tamanho > 0:
                for itemListaTextosTimeSpan in listaTextosTimeSpan:
                    if itemListaTextosTimeSpan != listaSaida[-1]:
                        listaSaida.append(itemListaTextosTimeSpan)
            else:
                for itemListaTextosTimeSpan in listaTextosTimeSpan:
                    listaSaida.append(itemListaTextosTimeSpan)
            '''
        trata_xml(listaTextoXML, listaSaida)
        
def main():
    with open('saida.txt','w') as texto:
        texto.write('')
        texto.close()
    dtAt = dt.now()
    stTm = dtAt - td(days=61)
    stTm = stTm.strftime('%Y-%m-%dT%H:%M:%SZ')
    endTm = dtAt.strftime('%Y-%m-%dT%H:%M:%SZ')
    global endTimeValidacao
    global ultimoEndTime
    endTimeValidacao = retorna_date_time(endTm)
    ultimoEndTime = endTimeValidacao
    requisicao_post_teste(stTm, endTm, [], 64, [], 0)


if __name__ == '__main__':
    main()
