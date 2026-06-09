import subprocess as cmd
import json

comandoGetGroups = 'curl --insecure --request POST --url \'https://127.0.0.1:3010/zabbix/api_jsonrpc.php\' --header \'authorization: Bearer {$API_KEY}\' --header \'Content-Type: application/json-rpc\' --data \'{\"jsonrpc\":\"2.0\",\"method\":\"hostgroup.get\",\"params\":{\"output\":[\"groupid\",\"name\"]},\"id\":10}\''


#print(comandoGetGroups)

resultado = json.loads(cmd.check_output(comandoGetGroups, shell=True, text=True))
grupos = resultado["result"]
idRequisicao = 10
print('\n')
for grupo in grupos:
    print(grupo["name"]+':', grupo["groupid"])
input("\nAqui os grupos registrados, aperte enter para prosseguir: ")
for item in grupos:
    #print(item["name"], item["groupid"])
    comandoGetHostsPorGrupo = 'curl --insecure --request POST --url \'https://127.0.0.1:3010/zabbix/api_jsonrpc.php\' --header \'authorization: Bearer {$API_KEY}\' --header \'Content-Type: application/json-rpc\' --data \'{"jsonrpc":"2.0","method":"host.get","params":{"output":["hostid","host","name"],"groupids":"'+item["groupid"]+'"},"id":'+str(idRequisicao)+'}\''
    idRequisicao += 1
    #print(comandoGetHostsPorGrupo)
    resultado = json.loads(cmd.check_output(comandoGetHostsPorGrupo, shell=True, text=False))
    listaHosts = resultado["result"]
    print("\nGrupo atual: ", item["name"])
    resposta = input('\nDeseja renomear os hosts desse grupo ? ("s" ou "n") : ')
    if resposta == 's':
        resposta = input('Deseja usar o prefixo ' + item["name"] + ' ou informar um novo? ("s" ou o novo prefixo) : ')
        if resposta == "s":
            prefixo = item["name"] +'@'
        else:
            prefixo = resposta + '@'
        for host in listaHosts:
            nomeAtual = host["name"]
            print("\n id host: ", host["hostid"], "\n nome host: ", nomeAtual)
            nomeAtual = nomeAtual.replace(' ','_')
            nomeAtual = nomeAtual.replace('-','_')
            nomeAtual = nomeAtual.replace(prefixo,'')
            nomeAtual = nomeAtual.replace('___','_')
            nomeAtual = nomeAtual.replace('__','_')
            novoNome = prefixo + nomeAtual
            print('novo nome ', novoNome)
            comandoUpdateNomeHost = 'curl --insecure --request POST --url \'https://127.0.0.1:3010/zabbix/api_jsonrpc.php\' --header \'authorization: Bearer {$API_KEY}\' --header \'Content-Type: application/json-rpc\' --data \'{"jsonrpc":"2.0", "method":"host.update", "params":{"hostid":"' + host["hostid"] + '","name":"' + novoNome + '"}}\''
            #print(comandoUpdateNomeHost)
            #input("Aperte enter pra renomear: ")
            cmd.check_output(comandoUpdateNomeHost, shell=True, text=True)
    else:
        print("Grupo inalterado")
    input("Aperte enter!")
