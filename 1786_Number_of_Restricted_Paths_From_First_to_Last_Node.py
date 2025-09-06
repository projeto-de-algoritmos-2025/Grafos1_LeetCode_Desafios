''' 
1786. Number of Restricted Paths From First to Last Node: https://leetcode.com/problems/number-of-restricted-paths-from-first-to-last-node/description/
Exercício resolvido por Ester Flores e Eduardo Schuindt

Esse exercício foi resolvido utilizando DFS, Grafos direcionados acíclicos. Ordenação topológica e
Algoritmo de Dijkstra
'''

# Importações da biblioteca padrão 
from collections import defaultdict
from heapq import heappop, heappush
from functools import cache
from typing import List
from math import inf


class Solution: 
    def countRestrictedPaths(self, n: int, edges: List[List[int]]) -> int:  
        #Transforma uma lista simples de arestas em uma estrutura de dados chamada lista de adjacência.
        grafo = defaultdict(list)
        for u, v, peso in edges:
            grafo[u].append((v, peso))
            grafo[v].append((u, peso))
      
        # Calcula as distâncias mais curtas de todos os nós até o nó 'n' usando o algoritmo de Dijkstra
        distancia = [inf] * (n + 1)
        distancia[n] = 0
        fila_de_prioridade = [(0, n)]  # Formato: (distância, nó)
      
        while fila_de_prioridade:
            distancia_atual, no_atual = heappop(fila_de_prioridade)
          
            if distancia_atual > distancia[no_atual]:
                continue
          
            # Atualiza as distâncias para os vizinhos
            for vizinho, peso_aresta in grafo[no_atual]:
                nova_distancia = distancia[no_atual] + peso_aresta
                if distancia[vizinho] > nova_distancia:
                    distancia[vizinho] = nova_distancia
                    heappush(fila_de_prioridade, (nova_distancia, vizinho))
      
        # Define o módulo para evitar que o resultado fique muito grande
        MODULO = 10**9 + 7
      
        # Usa DFS (Busca em Profundidade) com memorização para contar os caminhos restritos
        @cache
        def contar_caminhos(no: int) -> int:
            if no == n:
                return 1
          
            contagem_de_caminhos = 0
            for proximo_no, _ in grafo[no]:
                # A condição do "caminho restrito":
                # Segue apenas pelas arestas onde a distância até 'n' diminui estritamente
                if distancia[no] > distancia[proximo_no]:
                    contagem_de_caminhos = (contagem_de_caminhos + contar_caminhos(proximo_no)) % MODULO
          
            return contagem_de_caminhos
      
        # O nome do parâmetro 'n' aqui é o que foi passado para o método principal
        # e não deve ser confundido com o nome da variável interna.
        return contar_caminhos(1)
