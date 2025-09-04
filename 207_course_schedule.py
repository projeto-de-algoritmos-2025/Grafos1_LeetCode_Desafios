''' 
207.Course Schedule: https://leetcode.com/problems/course-schedule/description/
Exercício resolvido por Ester Flores e Eduardo Schuindt

Esse exercício pode ser resolvido utilizando BFS com ordenação topológica ou DFS.
A nossa solução foi pensada utilizando BFS, já que o exercício pede que seja verificado 
se todos os cursos foram feitos ou não.
COMPLEXIDADE = O(V + E). V = número de vértices (numCourses); E = número de arestas (prerequisites).
'''

from collections import deque
from typing import List

class Solution:
    '''
    O método canFinish recebe o número de cursos e a lista de pré-requisitos.
    Ele retorna um booleano. Se é possível concluir todos os cursos (true). Se não (false).
    Se não é possível concluir todos os cursos, então há um ciclo de dependências.
    '''
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        '''
        Aqui definimos o problema como um grafo direcionado, usando lista de adjacência.
        Onde cada curso é um nó e cada pré-requisito é uma aresta direcionada [ai, bi].
        '''
        adjacency_graph = [[] for _ in range(numCourses)]

        # Lista para rastrear o grau de entrada; quantos pré-requisitos cada curso tem.
        grau_entrada = [0] * numCourses

        '''
        Construção do grafo usando a lista de pré-requisitos.
        Para cada par [ai, bi], adicionamos uma aresta de prerequisite_course (bi) para dependent_course (ai).
        Também incrementamos o grau de entrada do dependent_course (ai).
        '''
        for dependent_course, prerequisite_course in prerequisites:
            adjacency_graph[prerequisite_course].append(dependent_course)
            grau_entrada[dependent_course] += 1

        # Fila para cursos prontos para serem feitos, ou seja, que possuem grau de entrada 0, sem pré-requisitos.
        ready_courses_queue = deque()
        for i in range(numCourses):
            if grau_entrada[i] == 0:
                ready_courses_queue.append(i)
        completed_courses_count = 0

        '''
        Processamento dos cursos na fila. 
        Aqui usamos uma abordagem BFS e algoritmo de Kahn para ordenação topológica.
        '''
        while ready_courses_queue:
            '''
            Remove o curso da frente da fila, ou seja, que já pode ser feito (grau de entrada = 0).
            E marca esse curso como concluído.
            '''
            current_course = ready_courses_queue.popleft()
            completed_courses_count += 1

            '''
            Nesse ponto, percorremos todos os cursos dependentes do curso atual.
            Para cada curso dependente, reduzimos seu grau de entrada em 1.
            Se o grau de entrada de um curso dependente se tornar 0, significa que todos os seus pré-requisitos foram concluídos.
            Então, adicionamos esse curso à fila de cursos prontos para serem feitos.
            '''
            for next_course in adjacency_graph[current_course]:
                grau_entrada[proximo_curso] -= 1
                if grau_entrada[next_course] == 0:
                    ready_courses_queue.append(next_course)
        
        '''
        Aqui verificamos se todos os cursos foram concluídos. 
        Se sim retornamos true, caso contrário false. 
        E nesse último caso, significa que há um ciclo de dependências, ou seja, o curso está bloqueado.
        '''
        return completed_courses_count == numCourses