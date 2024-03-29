
import random

from collections import deque
from viewer import MazeViewer
from math import inf, sqrt
from Celula import Celula
from PriorityQueue import PriorityQueue

def gera_labirinto(n_linhas, n_colunas, inicio, goal):
    # cria labirinto vazio
    labirinto = [[0] * n_colunas for _ in range(n_linhas)]

    # adiciona celulas ocupadas em locais aleatorios de
    # forma que 25% do labirinto esteja ocupado
    numero_de_obstaculos = int(0.50 * n_linhas * n_colunas)
    for _ in range(numero_de_obstaculos):
        linha = random.randint(0, n_linhas-1)
        coluna = random.randint(0, n_colunas-1)
        labirinto[linha][coluna] = 1

    # remove eventuais obstaculos adicionados na posicao
    # inicial e no goal
    labirinto[inicio.y][inicio.x] = 0
    labirinto[goal.y][goal.x] = 0

    return labirinto

def distancia(celula_1, celula_2):
    dx = celula_1.x - celula_2.x
    dy = celula_1.y - celula_2.y
    return sqrt(dx ** 2 + dy ** 2)


def esta_contido(lista, celula):
    for elemento in lista:
        if (elemento.y == celula.y) and (elemento.x == celula.x):
            return True
    return False


def custo_caminho(caminho):
    if len(caminho) == 0:
        return inf

    custo_total = 0
    for i in range(1, len(caminho)):
        custo_total += distancia(caminho[i].anterior, caminho[i])

    return custo_total


def obtem_caminho(goal):
    caminho = []

    celula_atual = goal
    while celula_atual is not None:
        caminho.append(celula_atual)
        celula_atual = celula_atual.anterior

    # o caminho foi gerado do final para o
    # comeco, entao precisamos inverter.
    caminho.reverse()

    return caminho


def celulas_vizinhas_livres(celula_atual, labirinto) -> list[Celula]:
    # generate neighbors of the current state
    vizinhos = [
        Celula(y=celula_atual.y-1, x=celula_atual.x-1, anterior=celula_atual),
        Celula(y=celula_atual.y+0, x=celula_atual.x-1, anterior=celula_atual),
        Celula(y=celula_atual.y+1, x=celula_atual.x-1, anterior=celula_atual),
        Celula(y=celula_atual.y-1, x=celula_atual.x+0, anterior=celula_atual),
        Celula(y=celula_atual.y+1, x=celula_atual.x+0, anterior=celula_atual),
        Celula(y=celula_atual.y+1, x=celula_atual.x+1, anterior=celula_atual),
        Celula(y=celula_atual.y+0, x=celula_atual.x+1, anterior=celula_atual),
        Celula(y=celula_atual.y-1, x=celula_atual.x+1, anterior=celula_atual),
    ]

    # seleciona as celulas livres
    vizinhos_livres = []
    for v in vizinhos:
        # verifica se a celula esta dentro dos limites do labirinto
        if (v.y < 0) or (v.x < 0) or (v.y >= len(labirinto)) or (v.x >= len(labirinto[0])):
            continue
        # verifica se a celula esta livre de obstaculos.
        if labirinto[v.y][v.x] == 0:
            vizinhos_livres.append(v)

    return vizinhos_livres


def breadth_first_search(labirinto, inicio, goal, viewer):
    # nos gerados e que podem ser expandidos (vermelhos)
    fronteira = deque()
    # nos ja expandidos (amarelos)
    expandidos = set()

    # adiciona o no inicial na fronteira
    fronteira.append(inicio)

    # variavel para armazenar o goal quando ele for encontrado.
    goal_encontrado = None

    # Repete enquanto nos nao encontramos o goal e ainda
    # existem para serem expandidos na fronteira. Se
    # acabarem os nos da fronteira antes do goal ser encontrado,
    # entao ele nao eh alcancavel.
    while (len(fronteira) > 0) and (goal_encontrado is None):

        # seleciona o no mais antigo para ser expandido
        no_atual = fronteira.popleft()

        # busca os vizinhos do no
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        # para cada vizinho verifica se eh o goal e adiciona na
        # fronteira se ainda nao foi expandido e nao esta na fronteira
        for v in vizinhos:
            if v.y == goal.y and v.x == goal.x:
                goal_encontrado = v
                # encerra o loop interno
                break
            else:
                if (not esta_contido(expandidos, v)) and (not esta_contido(fronteira, v)):
                    fronteira.append(v)

        expandidos.add(no_atual)

        viewer.update(generated=fronteira,
                      expanded=expandidos)
        #viewer.pause()


    caminho = obtem_caminho(goal_encontrado)
    custo   = custo_caminho(caminho)

    return caminho, custo, expandidos


def depth_first_search(labirinto, inicio, goal, viewer):
    # nos gerados e que podem ser expandidos (vermelhos)
    fronteira = deque()
    # nos ja expandidos (amarelos)
    expandidos = set()

    # adiciona o no inicial na fronteira
    fronteira.append(inicio)

    # variavel para armazenar o goal quando ele for encontrado.
    goal_encontrado = None

    # Repete enquanto nos nao encontramos o goal e ainda
    # existem para serem expandidos na fronteira. Se
    # acabarem os nos da fronteira antes do goal ser encontrado,
    # entao ele nao eh alcancavel.
    while (len(fronteira) > 0) and (goal_encontrado is None):

        # seleciona o no mais antigo para ser expandido
        no_atual = fronteira.pop()

        # busca os vizinhos do no
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        # para cada vizinho verifica se eh o goal e adiciona na
        # fronteira se ainda nao foi expandido e nao esta na fronteira
        for v in vizinhos:
            if v.y == goal.y and v.x == goal.x:
                goal_encontrado = v
                # encerra o loop interno
                break
            else:
                if (not esta_contido(expandidos, v)) and (not esta_contido(fronteira, v)):
                    fronteira.append(v)

        expandidos.add(no_atual)

        viewer.update(generated=fronteira,
                      expanded=expandidos)
        #viewer.pause()


    caminho = obtem_caminho(goal_encontrado)
    custo   = custo_caminho(caminho)

    return caminho, custo, expandidos

# Distância euclidiana entre 2 pontos
# Dado 2 pontos (x1, y1) e (x2, y2), a distância euclidiana entre eles é raiz_quadrada((x2-x1)² + (y2-y1)²)
# O (x1, y1) é o nó atual e o (x2, y2) é o nó objetivo (goal)
def heuristic(current: Celula, goal: Celula):
    result_x = (goal.x - current.x)**2
    result_y = (goal.y - current.y)**2
    return sqrt(result_x + result_y)

def is_goal(cell: Celula, goal: Celula):
    return cell.x == goal.x and cell.y == goal.y


# A * sem a hurísitca
def ucs(labirinto, inicio, goal, viewer: MazeViewer):
    pq = PriorityQueue((inicio, 0))
    # came_from = dict()
    cost_so_far = dict()
    cost_so_far[inicio] = 0
    expanded = set()

    goal_encontrado = None

    while not pq.is_empty():
        # Para o UCS, eu pŕetendo remover o nó de menor
        cell, _ = pq.get_highest_prior()

        if is_goal(cell, goal):
            goal_encontrado = cell
            break

        neighbors = celulas_vizinhas_livres(cell, labirinto)

        for v in neighbors:
            new_cost = cost_so_far[cell] + 1
            if v not in cost_so_far or new_cost < cost_so_far[v]:
                if (not esta_contido(expanded, v)) and (not pq.exists_in_queue(v)):
                # Aqui eu nunca testo se a célula já existe na fila e nem na fronteira, talvez o erro de parada subita seja por causa disso.
                    cost_so_far[v] = new_cost
                    prior = new_cost
                    pq.ordered_insert((v, prior))
                    v.anterior = cell
        
        expanded.add(cell)
        print(pq.get_priority_list())
        viewer.update(generated=pq.return_ordered_list_cell(), expanded=expanded)

    caminho = obtem_caminho(goal_encontrado)
    custo   = custo_caminho(caminho)

    return caminho, custo, expanded

# A*: https://www.redblobgames.com/pathfinding/a-star/introduction.html
def a_star_search(labirinto, inicio, goal, viewer: MazeViewer):
    pq = PriorityQueue((inicio, 0))
    # came_from = dict()
    cost_so_far = dict()
    cost_so_far[inicio] = 0
    expanded = set()

    goal_encontrado = None

    while not pq.is_empty():
        cell, _ = pq.get_lowest_prior()

        if is_goal(cell, goal):
            goal_encontrado = cell
            break

        neighbors = celulas_vizinhas_livres(cell, labirinto)

        for v in neighbors:
            new_cost = cost_so_far[cell] + 1
            if v not in cost_so_far or new_cost < cost_so_far[v]:
                if (not esta_contido(expanded, v)) and (not pq.exists_in_queue(v)):
                # Aqui eu nunca testo se a célula já existe na fila e nem na fronteira, talvez o erro de parada subita seja por causa disso.
                    cost_so_far[v] = new_cost
                    prior = new_cost + heuristic(v, goal)
                    pq.ordered_insert((v, prior))
                    v.anterior = cell
        
        expanded.add(cell)
        print(pq.get_priority_list())
        # viewer.update(generated=pq.return_ordered_list_cell(), expanded=expanded)

    caminho = obtem_caminho(goal_encontrado)
    custo   = custo_caminho(caminho)

    return caminho, custo, expanded


#-------------------------------


def main():
    # while True:
    #SEED = 42  # coloque None no lugar do 42 para deixar aleatorio
    #random.seed(SEED)
    N_LINHAS  = 20
    N_COLUNAS = 30
    INICIO = Celula(y=0, x=0, anterior=None)
    GOAL   = Celula(y=N_LINHAS-1, x=N_COLUNAS-1, anterior=None)


    """
    O labirinto sera representado por uma matriz (lista de listas)
    em que uma posicao tem 0 se ela eh livre e 1 se ela esta ocupada.
    """
    labirinto = gera_labirinto(N_LINHAS, N_COLUNAS, INICIO, GOAL)

    viewer = MazeViewer(labirinto, INICIO, GOAL,
                        step_time_miliseconds=20, zoom=40)

    #----------------------------------------
    # BFS Search
    #----------------------------------------
    viewer._figname = "DFS"
    caminho, custo_total, expandidos = \
            a_star_search(labirinto, INICIO, GOAL, viewer)

    if len(caminho) == 0:
        print("Goal é inalcançavel neste labirinto.")

    print(
        f"BFS:"
        f"\tCusto total do caminho: {custo_total}.\n"
        f"\tNumero de passos: {len(caminho)-1}.\n"
        f"\tNumero total de nos expandidos: {len(expandidos)}.\n\n"

    )

    viewer.update(path=caminho)
    viewer.pause()


    #----------------------------------------
    # DFS Search
    #----------------------------------------

    #----------------------------------------
    # A-Star Search
    #----------------------------------------

    #----------------------------------------
    # Uniform Cost Search (Obs: opcional)
    #----------------------------------------




print("OK! Pressione alguma tecla pra finalizar...")
input()


if __name__ == "__main__":
    main()
