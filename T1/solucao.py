import heapq

class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    #Constructor
    def __init__(self, estado, pai, acao, custo):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

    def __lt__(self, other):
        """
        Definicao do operador '<' para objetos da classe, necessario no metodo heappush()
        """
        if self.custo <= other.custo:
            return self
        else:
            other.custo

def swap(string, indice1, indice2):
   lista = list(string)
   lista[indice1], lista[indice2] = lista[indice2], lista[indice1]
   return ''.join(lista)

def sucessor(estado):
    """
    Recebe um estado (string) e retorna uma lista de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    # lista de sucessores
    sucessores = []
    #posição do underline no estado
    posicao_ = estado.rfind('_')
    #4 testes para eliminar posições impossíveis
    #if 0,1,2 não acima
    if posicao_>2:
        sucessores.append(('acima', swap(estado, posicao_,posicao_-3)))
    #if 6,7,8 não abaixo
    if posicao_<6:
        sucessores.append(('abaixo',swap(estado, posicao_,posicao_+3)))
    #if 0,3,6 não esquerda
    if posicao_ != 0 and posicao_ != 3 and posicao_ != 6:
        sucessores.append(('esquerda',swap(estado, posicao_,posicao_-1)))
    #if 2,5,8 não direita
    if posicao_ != 2 and posicao_ != 5 and posicao_ != 8:
        sucessores.append(('direita',swap(estado, posicao_,posicao_+1)))

    return sucessores


def expande(nodo):
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um iterable de nodos.
    Cada nodo do iterable contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    sucessores = sucessor(nodo.estado)
    lista = []

    for s in sucessores:
        direcao,estad = s
        novo = Nodo(estad,nodo,direcao,nodo.custo+1)
        lista.append(novo)

    return lista




def bfs(estado):
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    X = {}
    Fron = [Nodo(estado,None,None,0)]

    #loop
    while len(Fron)>0:
        v = Fron.pop(0)

        if v.estado == '12345678_':
            #retorna caminho
            caminho = []
            while v.pai != None:
                caminho.insert(0,v.acao)
                v = v.pai
            return caminho

        if v.estado not in X:
            #X.update({v.estado,v})
            X[v.estado] = v
            Fron.extend(expande(v))

    return None




def dfs(estado):
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    X = {}
    Fron = [Nodo(estado, None, None, 0)]

    # loop
    while len(Fron) > 0:
        v = Fron.pop()

        if v.estado == '12345678_':
            # retorna caminho
            caminho = []
            while v.pai != None:
                caminho.insert(0, v.acao)
                v = v.pai
            return caminho

        if v.estado not in X:
            # X.update({v.estado,v})
            X[v.estado] = v
            Fron.extend(expande(v))

    return None


def astar_hamming(estado):
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    def hamming_distance(estado):
        objetivo = '12345678_'
        soma = 0
        # calculo da distancia hamming
        # https://en.wikipedia.org/wiki/Hamming_distance
        for i in range(len(estado)):
            if estado[i] != objetivo[i]:
                soma += 1
        return soma

    X = {}
    Fron = [Nodo(estado, None, None, hamming_distance(estado))]   
    heapq.heapify(Fron)

    while len(Fron) > 0:
        v = heapq.heappop(Fron)
        if v.estado == '12345678_':
            #retorna caminho
            caminho = []
            while v.pai != None:
                caminho.insert(0,v.acao)
                v = v.pai
            return caminho
        if v.estado not in X:
            X[v.estado] = v
            for nodo in expande(v):
                if nodo.estado not in X:
                    nodo.custo += hamming_distance(nodo.estado)
                    heapq.heappush(Fron, nodo)
    return None


def astar_manhattan(estado):
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    
    def manhattan_distance(estado):
        objetivo = '12345678_'
        soma = 0
        for i, num in enumerate(estado):
            if not num == objetivo[i]:
                # coordenadas dos dois pontos
                coord_atual = (int(i/3), i%3)
                i_obj = objetivo.find(estado[i])
                coord_obj = (int(i_obj/3), i_obj%3)
                # calculo da distancia manhattan
                # https://en.wikipedia.org/wiki/Taxicab_geometry
                soma += abs(coord_atual[0] - coord_obj[0]) + abs(coord_atual[1] - coord_obj[1])
        return soma

    X = {}
    Fron = [Nodo(estado, None, None, manhattan_distance(estado))]   
    heapq.heapify(Fron)

    while len(Fron) > 0:
        v = heapq.heappop(Fron)
        if v.estado == '12345678_':
            #retorna caminho
            caminho = []
            while v.pai != None:
                caminho.insert(0,v.acao)
                v = v.pai
            return caminho
        if v.estado not in X:
            X[v.estado] = v
            for nodo in expande(v):
                if nodo.estado not in X:
                    nodo.custo += manhattan_distance(nodo.estado)
                    heapq.heappush(Fron, nodo)
    return None
