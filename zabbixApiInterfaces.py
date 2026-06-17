import requests as req
import json
import warnings

warnings.filterwarnings('ignore')

url = "https://192.168.108.89:3010/zabbix/api_jsonrpc.php"

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer 4851d0cb9ff55b45e20b977970d58878f1f77c26147f6fbd1bd3cac24a209446'
}

payload = json.dumps({
  "jsonrpc": "2.0",
  "method": "hostgroup.get",
  "params": {
    "output": [
      "groupid",
      "name"
    ]
  },
  "id": 1
})

retorno = req.request("POST", url, headers=headers, data=payload, verify=False)

retorno = retorno.text
#Extrai o texto retornado pela requisição
retorno = json.loads(retorno)
#Trata o texto com um parser
listaGrupos = retorno["result"]
#Do texto tratado, é extraído o valor da chave 'result'.
#O valor em questão é uma lista de dicionários

for item in listaGrupos:
    print("\ngroupName: ",item["name"],"\ngroupID: ",item["groupid"])

payload = json.dumps({
  "jsonrpc": "2.0",
  "method": "host.get",
  "params": {
    "output": [
      "hostid",
      "host",
      "name"
    ],
    "selectInterfaces":["type"],
    "groupids":"38"
  },
  "id": 2
})

retorno = req.request("POST", url, headers=headers, data=payload, verify=False)

retorno = retorno.text
#Extrai o texto retornado pela requisição
retorno = json.loads(retorno)
#Trata o texto com um parser
listaHosts = retorno["result"]
#Do texto tratado, é extraído o valor da chave 'result'.
#O valor em questão é uma lista de dicionários
for item in listaHosts:
    name = str(item["name"])
    name = name.replace("EXPOMINAS@",'')
    #print("\nhostId: ",item["hostid"],"\nhost: ",item["host"],"\nhostName: ",name,"\ninterfaces: ",item["interfaces"])
    if len(item["interfaces"]) == 1 and name != str(item["host"]):
        #print("A ser alterado: ",item["hostid"])
        payload = json.dumps({
                "jsonrpc": "2.0",
                "method": "hostinterface.create",
                "params": {
                    "hostid": item["hostid"],
                    "main": "1",
                    "type": "2",
                    "useip": "1",
                    "ip": item["host"],
                    "dns": "",
                    "port": "161",
                    "details": {
                        "version": "2",
                        "bulk": "1",
                        "community": "{$SNMP_COMMUNITY}",
                        "max_repetitions": "10"
                        }},
                "id": 3
                })
        retorno = req.request("POST", url, headers=headers, data=payload, verify=False)
    elif len(item["interfaces"]) == 1 and name == str(item["host"]):
        print("\nHost não identificado: ", item["hostid"])    
    else:
        listaInterfaces = item["interfaces"]
        if str(listaInterfaces[-1]["type"]) == "2":
            print("\nHost já tem interface SNMP: ", item["hostid"])
        else:
            print("A ser alterado", item["hostid"])
            payload = json.dumps({
                "jsonrpc": "2.0",
                "method": "hostinterface.create",
                "params": {
                    "hostid": item["hostid"],
                    "main": "1",
                    "type": "2",
                    "useip": "1",
                    "ip": item["host"],
                    "dns": "",
                    "port": "161",
                    "details": {
                        "version": "2",
                        "bulk": "1",
                        "community": "{$SNMP_COMMUNITY}",
                        "max_repetitions": "10"
                        }},
                "id": 3
                })
