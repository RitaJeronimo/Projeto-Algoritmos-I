import re

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'


RED   = "\033[1;31m"
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"


ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'
DESENHAR = 'g'

class Compromisso:

    def __init__(self, desc, data='', hora='', pri='', contexto='', projeto=''):
        self.desc = desc
        self.data = data
        self.hora = hora
        self.pri = pri
        self.contexto = contexto
        self.projeto = projeto


def adicionar(desc, data, hora, pri, contexto, projeto):
    compromisso = Compromisso(desc, data, hora, pri, contexto, projeto)
    novaAtividade = ''
    extras = []
    if compromisso.desc == '':
        raise RuntimeError('Cada compromisso deve ter obrigatoriamente uma descrição.')
    else:
        extras.append(compromisso.data)
        extras.append(compromisso.hora)
        extras.append(compromisso.pri)
        extras.append(compromisso.contexto)
        extras.append(compromisso.projeto)
        for indice, i in enumerate(extras):
            if indice == 2:
                if i != '':
                    novaAtividade = novaAtividade + i + ' ' + compromisso.desc + ' '
                else:
                    novaAtividade = novaAtividade + compromisso.desc + ' '
            else:
                if i != '':
                    novaAtividade = novaAtividade + i + ' '

    # Escreve no TODO_FILE.

    try:
        fp = open(TODO_FILE, 'a')
        fp.write(novaAtividade + "\n")
    except IOError as err:
        print("Não foi possível escrever para o arquivo " + TODO_FILE)
        print(err)
        return False
    finally:
        fp.close()

    return novaAtividade


def soDigitos(numero):
    if type(numero) != str:
        return False
    for x in numero:
        if x < '0' or x > '9':
            return False
    return True


def prioridadeValida(pri: str):
    if len(pri) != 3:
        return False
    if pri[0] != '(':
        return False
    if pri[2] != ')':
        return False
    if (pri[1] >= 'A' and pri[1] <= 'Z') or (pri[1] >= 'a' and pri[1] <= 'z'):
        return True
    else:
        return False


def horaValida(horaMin: str):
    if len(horaMin) != 4 or not soDigitos(horaMin):
        return False
    else:
        h = int(horaMin[0] + horaMin[1])
        m = int(horaMin[2] + horaMin[3])
        if h < 00 or h > 23:
            return False
        if m < 00 or m > 59:
            return False
        else:
            return True


def dataValida(data: str):
    if len(data) != 8 or not soDigitos(data):
        return False
    dia = data[0] + data[1]
    mes = data[2] + data[3]
    ano = data[4] + data[5] + data[6] + data[6]
    if dia < '01' or dia > '31' or mes < '01' or mes > '12' or len(ano) != 4:
        return False
    else:
        if dia <= '31' and (
                mes == '01' or mes == '03' or mes == '05' or mes == '07' or mes == '08' or mes == '10' or mes == '12'):
            return True
        elif dia <= '30' and (mes == '04' or mes == '06' or mes == '09' or mes == '11'):
            return True
        elif dia <= '29' and mes == '02':
            return True
        else:
            return False


def projetoValido(proj: str):
    if len(proj) >= 2 and proj[0] == '+':
        return True
    return False


def contextoValido(cont: str):
    if len(cont) >= 2 and cont[0] == '@':
        return True
    return False


def organizar(linhas):
    data = ''
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
    itens = []
    for l in linhas:
        try:
            data = re.findall(pattern='(\d{8})\s+', string=l)[0]
            l = re.sub(pattern='(\d{8})\s+', repl='', string=l)
        except:
            pass
        try:
            hora = re.findall(pattern='\W*(\d{4})\s+', string=l)[0]
            l = re.sub(pattern='\W*(\d{4})\s+', repl='', string=l)
        except:
            pass
        try:
            pri = re.findall(pattern='(\(\w\))', string=l)[0]
            l = re.sub(pattern='(\(\w\))', repl='', string=l)
        except:
            pass
        try:
            contexto = re.findall(pattern='(\@[\w\d]*)', string=l)[0]
            l = re.sub(pattern='(\@[\w\d]*)', repl='', string=l)
        except:
            pass
        try:
            projeto = re.findall(pattern='(\+[\w\d]*)', string=l)[0]
            l = re.sub(pattern='(\+[\w\d]*)', repl='', string=l)
        except:
            pass
        desc = l.strip()
        if desc == '':
            raise RuntimeError('Cada compromisso deve conter uma descrição.')
        c = Compromisso(desc=desc, data=data, hora=hora, pri=pri, contexto=contexto, projeto=projeto)
        itens.append(c)
    return itens


def listar():
    fp = open(TODO_FILE, 'r')
    lista = []
    texto = fp.readlines()
    for i in texto:
        texto = i.strip()
        lista = lista + organizar(texto)
    fp.close()

    for item in lista:
        if dataValida(item.data) == False:
            raise RuntimeError('Data inválida. Reescreva seu compromisso com uma data válida.')
        if horaValida(item.hora) == False:
            raise RuntimeError('Hora inválida. Reescreva seu compromisso com uma hora válida.')
        if prioridadeValida(item.pri) == False:
            raise RuntimeError('Prioridade inválida. Reescreva seu compromisso com uma prioridade válida.')
        if contextoValido(item.contexto) == False:
            raise RuntimeError('Contexto inválido. Reescreva seu compromisso com um contexto válido.')
        if projetoValido(item.projeto) == False:
            raise RuntimeError('Projeto inválido. Reescreva seu compromisso com um projeto válido.')
    return lista


def ordenacaoPri(lista_comp:[Compromisso]):
    lista_comp.sort(key=lambda a: a.pri)
    return lista_comp


def ordenacaoData(lista_comp:[Compromisso]):
    lista_comp.sort(key = lambda a: a.data)
    return lista_comp


def ordenandoHora(lista_comp:[Compromisso]):
    lista_comp.sort(key = lambda a: a.hora)
    return lista_comp


def listarSemFormatacao(desc, data, hora, pri, contexto, projeto):
    compromisso = Compromisso(desc, data, hora, pri, contexto, projeto)
    novaAtividade = ''
    extras = []
    if compromisso.desc == '':
        raise RuntimeError('Cada compromisso deve ter obrigatoriamente uma descrição.')
    else:
        extras.append(compromisso.data)
        extras.append(compromisso.hora)
        extras.append(compromisso.pri)
        extras.append(compromisso.contexto)
        extras.append(compromisso.projeto)
        for indice, i in enumerate(extras):
            if indice == 2:
                if i != '':
                    novaAtividade = novaAtividade + i + ' ' + compromisso.desc + ' '
                else:
                    novaAtividade = novaAtividade + compromisso.desc + ' '
            else:
                if i != '':
                    novaAtividade = novaAtividade + i + ' '

        return novaAtividade


def processarComandos(comandos):
    if comandos[2] == ADICIONAR:
        comandos.pop(0)  # remover python
        comandos.pop(0)  # remover agenda.py
        comandos.pop(0)  # remover a
        if len(comandos) == 0:
            raise RuntimeError('Para que um compromisso seja adicionado, deve conter pelo menos uma descrição.')
        else:
            itemParaAdicionar = organizar([' '.join(comandos)])[0]
            if adicionar(itemParaAdicionar.desc, itemParaAdicionar.data, itemParaAdicionar.hora, itemParaAdicionar.pri,
                         itemParaAdicionar.contexto, itemParaAdicionar.projeto) == False:
                raise RuntimeError('O compromisso não pode ser adicionado.')
            else:
                return 'O compromisso pôde ser adicionado.'

    elif comandos[2] == LISTAR:
        comandos.pop(0)  # remover python
        comandos.pop(0)  # remover agenda.py
        comandos.pop(0)  # remover l

    elif comandos[2] == REMOVER:
        comandos.pop(0)  # remover python
        comandos.pop(0)  # remover agenda.py
        comandos.pop(0)  # remover r

    elif comandos[2] == FAZER:
        comandos.pop(0)  # remover python
        comandos.pop(0)  # remover agenda.py
        comandos.pop(0)  # remover f
        if fazer(numero) == False:
            raise RuntimeError('Compromisso inexistente'.)
        else:
            print('Compromisso feito')

    elif comandos[2] == PRIORIZAR:
        comandos.pop(0)  # remover python
        comandos.pop(0)  # remover agenda.py
        comandos.pop(0)  # remover p

    elif comandos[2] == DESENHAR:
        comandos.pop(0)  # remover python
        comandos.pop(0)  # remover agenda.py
        comandos.pop(0)  # remover g
        try:
            N = int(comando.pop(0))
        if N < 0:
            raise RuntimeError('Número negativo')

    else:
        raise RuntimeError('Comando inválido.')

