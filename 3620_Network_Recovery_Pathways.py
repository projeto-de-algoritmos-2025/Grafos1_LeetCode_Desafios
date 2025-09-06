''' 
3620. Network Recovery Pathways: https://leetcode.com/problems/network-recovery-pathways/description/
Exercício resolvido por Ester Flores e Eduardo Schuindt

Esse exercício foi resolvido utilizando BFS, Ordenação Topológica e Busca Binária
'''

import collections

class Solution: 
    def findMaxPathScore(self, edges: list[list[int]], online: list[bool], k: int) -> int: 
        # Determina o número total de nós com base na lista de status 'online'.
        numeroDeNos = len(online)
        
        # Passo 1: Construção do Grafo e Preparação para Ordenação Topológica 

        # listaDeAdjacencia: Armazena o grafo. Mapeia um nó de origem para uma lista de tuplas (destino, custo).
        listaDeAdjacencia = collections.defaultdict(list)
        # grauDeEntrada: Array para armazenar o número de arestas que chegam em cada nó. Essencial para a ordenação topológica.
        grauDeEntrada = [0] * numeroDeNos
        # custoMaximoDaAresta: Usado para definir o limite superior da busca binária.
        custoMaximoDaAresta = 0

        # Itera sobre todas as arestas para construir o grafo.
        for noOrigem, noDestino, custoAresta in edges:
            # Ignora a aresta se o nó de origem ou o de destino estiverem offline.
            if not online[noOrigem] or not online[noDestino]:
                continue
            
            # Adiciona a aresta ao grafo, apenas se os nós estiverem online.
            listaDeAdjacencia[noOrigem].append((noDestino, custoAresta))
            # Incrementa o grau de entrada do nó de destino.
            grauDeEntrada[noDestino] += 1
            # Atualiza o custo máximo encontrado até agora.
            custoMaximoDaAresta = max(custoMaximoDaAresta, custoAresta)

        # Passo 2: Ordenação Topológica
        
        # fila: Fila usada para a ordenação. Começa com os nós que não têm arestas de entrada.
        fila = collections.deque()
        for indiceNo in range(numeroDeNos):
            # Se um nó tem grau de entrada 0, ele é um ponto de partida no grafo.
            if grauDeEntrada[indiceNo] == 0:
                fila.append(indiceNo)
        
        # ordemTopologica: Lista que armazenará a ordem linear dos nós.
        ordemTopologica = []
        while fila:
            # Pega o próximo nó da fila.
            noAtual = fila.popleft()
            ordemTopologica.append(noAtual)
            
            # Para cada vizinho do nó atual
            for noVizinho, _ in listaDeAdjacencia[noAtual]:
                # Remove a aresta do nó atual para o vizinho, diminuindo o grau de entrada.
                grauDeEntrada[noVizinho] -= 1
                # Se o vizinho agora não tem mais arestas de entrada, ele está pronto para ser processado.
                if grauDeEntrada[noVizinho] == 0:
                    fila.append(noVizinho)

        # Passo 3: Função Verificadora para a Busca Binária
        
        # Esta função verifica se é POSSÍVEL encontrar um caminho do nó 0 ao último nó com um score mínimo pontuacaoMinimaSuposta e custo total <= k.
        def verificarPossibilidade(pontuacaoMinimaSuposta: int) -> bool:
            # distancias: Armazena o menor custo para chegar a cada nó a partir do nó 0.
            distancias = [float('inf')] * numeroDeNos
            distancias[0] = 0  # O custo para chegar ao início é 0.

            # Itera sobre os nós na ordem topológica. Isso garante que, ao visitar um nó, se já tenha encontrado o caminho mais curto para ele.
            for noAtual in ordemTopologica:
                # Se o nó atual é inalcançável, pula.
                if distancias[noAtual] == float('inf'):
                    continue
                
                # Otimização: se o custo para chegar aqui já excede k, não há como continuar.
                if distancias[noAtual] > k:
                    continue
                
                # Itera sobre os vizinhos do nó atual.
                for noVizinho, custo in listaDeAdjacencia[noAtual]:
                    # A condição principal: só considera a aresta se seu custo
                    # for maior ou igual à pontuação que esta testando.
                    if custo >= pontuacaoMinimaSuposta:
                        # atualiza a distância para o vizinho se encontrar um caminho mais curto.
                        distancias[noVizinho] = min(distancias[noVizinho], distancias[noAtual] + custo)
            
            # Retorna True se o custo para chegar ao nó final for menor ou igual a k.
            return distancias[numeroDeNos - 1] <= k

        # Passo 4: Busca Binária na Resposta
        
        resposta = -1  # Valor padrão caso nenhum caminho seja encontrado.
        # O score pode variar de 0 até o custo máximo de uma aresta.
        limiteInferior, limiteSuperior = 0, custoMaximoDaAresta
        
        while limiteInferior <= limiteSuperior:
            # Pega o ponto médio do intervalo de busca.
            pontoMedio = (limiteInferior + limiteSuperior) // 2
            
            # Verifica se um caminho com score mínimo pontoMedio é possível.
            if verificarPossibilidade(pontoMedio):
                # Se for possível, pontoMedio é uma resposta válida.
                # Guarda e tenta um valor ainda maior.
                resposta = pontoMedio
                limiteInferior = pontoMedio + 1
            else:
                # Se não for possível, o score pontoMedio é muito alto.
                # Precisa tentar um valor menor.
                limiteSuperior = pontoMedio - 1
                
        # Retorna a melhor resposta encontrada.
        return resposta