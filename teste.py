import time
import random
import math


class adjacencyMatrix:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = [[0]*self.vertices for i in range(self.vertices)]

    def add_edge(self, u, v):
        self.graph[u - 1][v - 1] = 1
        self.graph[v - 1][u - 1] = 1

    def show_matrix(self):
        matrix = []
        for i in range(self.vertices):
            matrix.append(self.graph[i])
        return matrix



#IMPORTANTE: VER MANUAL DE USO DA CLASSE NO FINAL DO ARQUIVO!!!!
class Grafo:

    def __init__(self, grafo_txt, escolha):
        
        self.arestas = []
        self.vetor = []
        self.matrix = []
        self.nArestas = 0
        self.representacao = escolha 

        #LEITURA DO ARQUIVO
        with open(grafo_txt, 'r') as file:
            #LEITURA DA QUANTIDADE DE VÉRTICES
            self.nVertices = int((file.readline().rstrip('\n')))

            self.grau = [0] * (self.nVertices + 1)

            #AQUI A LEITURA SE DIVIDE EM DOIS CASOS DEPENDENDO DA ESCOLHA DO USUÁRIO DE ESTRUTURA

            #CASO O USUÁRIO ESCOLHA A MATRIZ
            if (self.representacao == '1'):

                while(True):
                    arestaPrimitiva = file.readline().rstrip('\n')
                    if arestaPrimitiva:
                        self.nArestas += 1
                        ap = []
                        for v in arestaPrimitiva.split():
                            ap.append(int(v))
                        aresta = (ap[0], ap[1])
                        self.grau[ap[0]] += 1
                        self.grau[ap[1]] += 1
                        self.arestas.append(aresta)
                    else:
                        break

                g = adjacencyMatrix(self.nVertices)
                for i in range(len(self.arestas)):
                    arestas = self.arestas[i]
                    g.add_edge(arestas[0], arestas[1])
                self.matrix = g.show_matrix()

            #CASO O USUÁRIO ESCOLHA O VETOR
            else:           
                self.vetor = [[]] * (self.nVertices+1)
                while(True): 
                    arestaPrimitiva = file.readline().rstrip('\n')
                    if arestaPrimitiva:
                        self.nArestas += 1
                        ap = []
                        for v in arestaPrimitiva.split():
                            ap.append(int(v))
                        self.grau[ap[0]] += 1
                        self.grau[ap[1]] += 1

                        self.vetor[ap[0]] = sorted(self.vetor[ap[0]] + [ap[1]])
                        self.vetor[ap[1]] = sorted(self.vetor[ap[1]] + [ap[0]]) 
                    else:
                        break
        
        self.grau = sorted(self.grau)
        if self.nVertices % 2 == 0:
            self.grauMediano = (self.grau[int(self.nVertices/2)] + self.grau[int(self.nVertices/2) + 1]) / 2
        else:
            self.grauMediano = (self.grau[int(self.nVertices/2 + 0.5)])
        self.grauMedio = 0
        for g in self.grau:
            self.grauMedio += g
        self.grauMedio = self.grauMedio / self.nVertices

        with open("arquivoSaida.txt", "w") as file:
            file.write("Numero de vertices: " + str(self.nVertices) + "\n")
            file.write("Numero de arestas: " + str(self.nArestas) + "\n")
            file.write("Grau minimo: " + str(self.grau[1]) + "\n")
            file.write("Grau maximo: " + str(self.grau[self.nVertices]) + "\n")
            file.write("Grau medio: " + str(self.grauMedio) + "\n")
            file.write("Grau mediano: " + str(self.grauMediano) + "\n")


    def bfs(self, raiz):

        fila = []
        vertices = [-1] * (self.nVertices + 1)
        nivel = [-1] * (self.nVertices + 1)
        pai = [-1] * (self.nVertices + 1)

        vertices[raiz] = 0
        pai[raiz] = 0
        nivel[raiz] = 0
        fila.append(raiz)

        if (self.representacao == "1"):
            while(len(fila) != 0):
                x = fila[0] - 1
                w = self.matrix[x]
                fila.pop(0)
                for j in range(self.nVertices):
                    if (w[j] == 1 and vertices[j+1] == -1):
                        vertices[j+1] = 0
                        fila.append(j+1)
                        pai[j+1] = x+1
                        nivel[j+1] = nivel[x+1] + 1

        else:
            while(len(fila) != 0):
                x = fila[0]
                w = self.vetor[x]
                fila.pop(0)
                for j in w:
                    if(vertices[j] == -1):
                        vertices[j] = 0
                        fila.append(j)
                        pai[j] = x
                        nivel[j] = nivel[x] + 1

        return (nivel, pai)



    def bfsFile(self, raiz):
        x = self.bfs(raiz)
        with open("bfs.txt", "w") as file:
            file.write("VERTICE / PAI / NIVEL \n")
            for i in range(1, self.nVertices+1):
                file.write(str(i) + " / " + str(x[1][i]) + " / " + str(x[0][i]) + "\n")
            file.write("OS VERTICES COM NIVEL E PAI -1 NAO PERTENCEM A ESSA COMPONENTE CONEXA \n")
            file.write("O VERTICE COM NIVEL 0 E PAI 0 = RAIZ")



    def dfs(self, raiz):

        pilha = []
        vertices = [-1] * (self.nVertices + 1)
        nivel = [-1] * (self.nVertices + 1)
        pai = [-1] * (self.nVertices + 1)

        pai[raiz] = 0
        nivel[raiz] = 0
        pilha.append(raiz)

        vpuv = [-1] * (self.nVertices + 1)

        if (self.representacao == "1"):
            while(len(pilha) != 0):
                x = pilha[0] - 1
                if(pai[x+1]) == -1:
                    pai[x+1] = vpuv[x+1]
                    nivel[x+1] = nivel[vpuv[x+1]] + 1
                pilha.pop(0)
                if (vertices[x+1] != 0):
                    vertices[x+1] = 0
                    temp = []
                    for j in range(self.nVertices):
                        if self.matrix[x][j] == 1:
                            temp.append(j+1)
                            vpuv[j+1] = x+1
                    pilha = temp + pilha           

        else:
            while(len(pilha) != 0):
                x = pilha[0]
                if(pai[x]) == -1:
                    pai[x] = vpuv[x]
                    nivel[x] = nivel[vpuv[x]] + 1
                pilha.pop(0)
                if (vertices[x] != 0):
                    vertices[x] = 0
                    w = self.vetor[x]
                    temp = []
                    for j in w:
                        temp.append(j)
                        vpuv[j] = x
                    pilha = temp + pilha
        
        return (nivel, pai)

    
    
    def dfsFile(self, raiz):
        x = self.dfs(raiz)
        with open("dfs.txt", "w") as file:
            file.write("VERTICE / PAI / NIVEL \n")
            for i in range(1, self.nVertices+1):
                file.write(str(i) + " / " + str(x[1][i]) + " / " + str(x[0][i]) + "\n")
            file.write("OS VERTICES COM NIVEL E PAI -1 NAO PERTENCEM A ESSA COMPONENTE CONEXA \n")
            file.write("O VERTICE COM NIVEL 0 E PAI 0 = RAIZ")




    def distancia(self, u, v):
        nivel = self.bfs(u)[0]
        return nivel[v]

    

    def diametro(self):
        dia = [0, [0,0]]
        for i in range(1, self.nVertices+1):
            for j in range(i, self.nVertices+1):
                if (i != j):
                    d = self.distancia(i, j)
                    if d > dia[0]:
                        dia[0] = d
                        dia[1][0] = i
                        dia[1][1] = j
        print(dia[0])

    
    def diametroAprox(self):
        dia = [0, [0,0]]
        for i in range(1, int(math.log(self.nVertices, 2))):
            k = random.randint(1, self.nVertices)
            j = random.randint(1, self.nVertices)
            if (k != j):
                d = self.distancia(k, j)
                if d > dia[0]:
                    dia[0] = d
                    dia[1][0] = k
                    dia[1][1] = j
        print(dia[0])



    def componentesConexas(self):

        nComponentesConexas = 0
        componentes = []
        vertices = [-1] * (self.nVertices + 1)

        for v in range(1, self.nVertices + 1):
            if (vertices[v] == -1):
                nivel = self.bfs(v)[0]
                nComponentesConexas += 1
                nVerticesCC = 0
                cc = []
                for n in range(1, self.nVertices + 1):
                    if (nivel[n] != -1):
                        vertices[n] = 0
                        cc.append(n)
                        nVerticesCC += 1
                componentes.append((cc, nVerticesCC))
        
        return (nComponentesConexas, componentes)
    
#ABAIXO, DEVE-SE POR O CAMINHO PARA O ARQUIVO TXT QUE CONTEM OS GRAFOS ENTRE AS ASPAS COMO PRIMEIRO PARAMETRO. NÂO SE DEVE RETIRAR O r ANTES DAS ASPAS
#O SEGUNDO PARAMETRO DEVE SER SOMENTE "1" PARA USAR A REPRESENTAÇÂO DE MATRIZ OU "2" PARA USAR O VETOR. AMBOS DEVEM ESTAR ENTRE ASPAS!!!

g = Grafo(r"C:\Users\Bernardo\Documents\ufrj_2021_2\Trab1_TeoGraf\grafo_2.txt", 2)
x = g.componentesConexas()
print("Número de componentes conexas: " + str(x[0]))
for i in x[1]:
    print("Número de vértices da componentes conexa a seguir: " + str(i[1]))
    print("Componente conexa: " + str(i[0]))
    print()

