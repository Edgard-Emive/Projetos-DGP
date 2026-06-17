import requests as req
from requests.auth import HTTPDigestAuth as digAuth

with open ('hosts.txt', 'r') as arquivo:
    listaDeHosts = arquivo.read()

listaDeHosts = listaDeHosts.split(',')

headers = {
  'Content-Type': 'application/xml'
}

payloadPrefixo= "<?xml version=\"1.0\" encoding=\"UTF-8\"?> <SNMP version=\"2.0\" xmlns=\"http://www.hikvision.com/ver20/XMLSchema\"> <SNMPv1c version=\"2.0\" xmlns=\"http://www.hikvision.com/ver20/XMLSchema\"> <notificationEnabled>true</notificationEnabled> <SNMPTrapReceiverList version=\"2.0\" xmlns=\"http://www.hikvision.com/ver20/XMLSchema\"> <SNMPTrapReceiver version=\"2.0\" xmlns=\"http://www.hikvision.com/ver20/XMLSchema\"> <id>1</id> <ReceiverAddress> <addressingFormatType>ipaddress</addressingFormatType> <ipAddress>172.31.88.107</ipAddress> <portNo>162</portNo> </ReceiverAddress> <notificationType>trap</notificationType> <communityString>public</communityString> </SNMPTrapReceiver> </SNMPTrapReceiverList> <enabled>false</enabled> <writeCommunity>private</writeCommunity> <readCommunity>public</readCommunity> </SNMPv1c> <SNMPv2c version=\"2.0\" xmlns=\"http://www.hikvision.com/ver20/XMLSchema\"> <notificationEnabled>true</notificationEnabled> <SNMPTrapReceiverList version=\"2.0\" xmlns=\"http://www.hikvision.com/ver20/XMLSchema\"> <SNMPTrapReceiver version=\"2.0\" xmlns=\"http://www.hikvision.com/ver20/XMLSchema\"> <id>1</id> <ReceiverAddress> <addressingFormatType>ipaddress</addressingFormatType> <ipAddress>"

payloadSufixo = "</ipAddress> <portNo>162</portNo> </ReceiverAddress> <notificationType>trap</notificationType> <communityString>public</communityString> </SNMPTrapReceiver> </SNMPTrapReceiverList> <enabled>true</enabled> <writeCommunity>private</writeCommunity> <readCommunity>public</readCommunity> </SNMPv2c> <SNMPAdvanced version=\"2.0\" xmlns=\"http://www.hikvision.com/ver20/XMLSchema\"> <localEngineID>e0ca3cb6482a</localEngineID> <SNMPUserList> <SNMPUser version=\"2.0\" xmlns=\"http://www.hikvision.com/ver20/XMLSchema\"> <id>1</id> <userName></userName> <remoteEngineID></remoteEngineID> <snmpAuthenticationMethod>none</snmpAuthenticationMethod> <snmpPrivacyMethod>none</snmpPrivacyMethod> </SNMPUser> <SNMPUser version=\"2.0\" xmlns=\"http://www.hikvision.com/ver20/XMLSchema\"> <id>2</id> <userName></userName> <remoteEngineID></remoteEngineID> <snmpAuthenticationMethod>none</snmpAuthenticationMethod> <snmpPrivacyMethod>none</snmpPrivacyMethod> </SNMPUser> </SNMPUserList> <enabled>false</enabled> </SNMPAdvanced> <listenPort>161</listenPort> </SNMP> "

for host in listaDeHosts:
    urlSNMP = 'http://'+host+'/ISAPI/System/Network/snmp'
    urlINFO = 'http://'+host+'/ISAPI/System/deviceinfo'
    payload = payloadPrefixo + host + payloadSufixo
    try:
        retornoGET = req.request("GET", urlSNMP, auth=digAuth('usuario','senha'))
        if str(retornoGET) == '<Response [200]>':
            print('Requisição de infos SNMP bem sucedida, para o host: ',host,' !'"\n")
        else:
            print('Função não suportada pelo host: ',host,' !'"\n")
        print(retornoGET,"\n")
        print(retornoGET.text,"\n")
    except:
        print('Requisição de infos SNMP recusada pelo host: ',host,' !',"\n")
        retornoGET = '<Response [403]>'
        try:
            retornoGET = req.request("GET", urlINFO, auth=digAuth('usuario','senha'))
            print(retornoGET.text,"\n")
        except:
            print('O dispositivo ',host,' não suporta ISAPI!',"\n",'Necessário validar o host: ',host,"\n")
            retornoGET = '<Response [403]>'
        
    if str(retornoGET) == '<Response [200]>':
        try:
            retornoPUT = req.request("PUT", urlSNMP, headers=headers, data=payload, auth=digAuth('usuario','senha'))
            if str(retornoPUT) == '<Response [200]>':
                print('SNMP habiilitado para o host: ',host,"\n")
        except:
            print('Deu ruim com ',host,"\n")
        
print('Finalizado!')

