'''Módulo com as funções utilizadas para armazenar e manipular os dados'''

import discord

import os
import json

PATH_CONFIG = './dados/config.json'
PATH_APOIO = './dados/apoiadores.json'

def FirstRun():
    '''Checa se arquivos necessários para o funcionamento do bot existem e os cria'''

    if not os.path.exists('./toke.py'):
        with open('toke.py', 'w', encoding="UTF-8") as file:
            file.write('token = "seu token aqui, não retire as aspas"')

    if not os.path.exists('./audios'):
        os.mkdir('./audios')

    if not os.path.exists('./dados'):
        os.mkdir('./dados')    

    if not os.path.exists(PATH_APOIO):
        with open(PATH_APOIO, 'w') as file:
            file.write('{\n}')
    
    if not os.path.exists(PATH_CONFIG):
        with open(PATH_CONFIG, 'w') as file:
            file.write('{\n}')


def DefaultConfigs(client: discord.Client):
    '''Checa se todos os servidores que o bot está, tem uma configuração no banco de dados, se algum
    não tiver, então coloca as configurações padrão.
    
    Configurações padrão: 
        - chats de mensagem: todos 
        - idioma da voz: pt_br

    '''

    with open(PATH_CONFIG, 'r') as fileread:
        dados = json.load(fileread)
    dados:dict
    
    for server in client.guilds: 
        if str(server.id) not in dados.keys():
            default = {server.id:{
                "canais":"todos",
                "idioma":"pt",
                "usuarios":[]}
                }
            dados.update(default)
            with open(PATH_CONFIG,'w') as fileWrite:
                json.dump(dados,fileWrite, indent=4)

def UpdateChannels(guildID:int, channels: str | list[str] = "todos"):
    '''
    Atualiza os valores dos canais na configuração do servidor

    Parâmetros:
        - guildID: ID do servidor
        - channels: canais em que o bot funcionará, valor padrão é "todos", mas pode ser uma lista de string com o id dos canais
    '''

    with open(PATH_CONFIG) as fileRead:
        jsonFile:dict = json.load(fileRead)

    jsonFile[str(guildID)]["canais"] = channels

    with open(PATH_CONFIG, 'w') as fileWrite:
        json.dump(jsonFile,fileWrite, indent=4)
