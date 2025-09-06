''' 
1568. Minimum Number of Days to Disconnect Island: https://leetcode.com/problems/minimum-number-of-days-to-disconnect-island/description/
Exercício resolvido por Ester Flores e Eduardo Schuindt

Na nossa abordagem usamos como referência o algoritmo flood fill para contar o número de ilhas no grid com BFS.
'''

from typing import List
from collections import deque

class Solution:
    def minDays(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])

        '''
        Função para contar o número de ilhas no grid.
        Uma ilha é definida como um grupo de 1s conectados na horizontal ou na vertical.
        '''
        def count_islands() -> int:

            # Definimos uma matriz para marcar as células visitadas
            visited = [[False] * n for _ in range(m)]

            '''
            Função BFS para explorar toda uma ilha a partir de uma célula inicial.
            Nessa etapa usamos como referência o algoritmo flood fill.
            '''
            def bfs(sr: int, sc: int) -> None:
                
                '''
                Definimos uma fila para percorrer as células da ilha (BFS)
                E definimos a célula inicial como visitada.
                '''
                q = deque([(sr, sc)])
                visited[sr][sc] = True
                
                while q:

                    '''    
                    Pegamos a célula atual da fila.
                    E verificamos suas 4 direções (cima, baixo, esquerda, direita).
                    '''
                    r, c = q.popleft()
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nr, nc = r + dr, c + dc

                        # Verificamos se a nova célula está dentro dos limites do grid.
                        if 0 <= nr < m and 0 <= nc < n:

                            # Se a nova célula é parte da ilha e não foi visitada, adicionamos à fila.
                            if not visited[nr][nc] and grid[nr][nc] == 1:
                                visited[nr][nc] = True
                                q.append((nr, nc))
            '''
            Contamos o número de ilhas no grid.
            Se encontrarmos uma terra não visitada, iniciamos uma BFS a partir dela.
            '''
            islands = 0
            for i in range(m):
                for j in range(n):
                    if grid[i][j] == 1 and not visited[i][j]:
                        islands += 1
                        if islands > 1:           
                            return islands
                        bfs(i, j)
            return islands

        '''
        1º Caso: Se o grid já não tem ilhas ou tem mais de uma ilha, retornamos 0, ou seja, está desconectado.
        '''
        if count_islands() != 1:
            return 0

        '''
        2º Caso: Tentamos remover cada célula de terra e verificamos se desconecta a ilha.
        '''
        for i in range(m):
            for j in range(n):

                # Se a célula é terra, tentamos removê-la.
                if grid[i][j] == 1:
                    grid[i][j] = 0      
                    
                    # Se ao remover a célula desconecta a ilha, retornamos 1, ou seja, conseguimos transformar em água em 1 dia.        
                    if count_islands() != 1:    
                        grid[i][j] = 1          
                        return 1
                    grid[i][j] = 1             
        '''
        3º Caso: Se nenhum dos casos anteriores se aplicar, retornamos 2, ou seja, em no máximo 2 dias conseguimos desconectar a ilha.
        '''
        return 2
