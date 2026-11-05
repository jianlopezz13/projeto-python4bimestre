import json

# OS COMENTARIOS NAO FOI PEGO NA IA TROPA :) , É APENAS PARA AJUDAR VCS S2

class QuizMaster:
    def __init__(self, arquivo="perguntas.json"):
        # PASSO 1: O Servidor instancia o QuizMaster e carrega as perguntas do JSON na memória
        with open(arquivo, 'r', encoding='utf-8') as f:
            self.perguntas = json.load(f)
        
        # Dicionário para guardar a pontuação de cada jogador { "Nome": pontos }
        self.pontuacoes = {}

    def total_perguntas(self):
        # O Servidor usa isto para saber até onde o loop de perguntas vai
        return len(self.perguntas)

    def obter_pergunta(self, idx):
        # PASSO 2: O Servidor pede a pergunta pelo índice e envia o texto e as opções para os Clientes
        if idx < len(self.perguntas):
            return self.perguntas[idx]
        return None

    def verificar_resposta(self, idx, resposta):
        # PASSO 3: Quando o Cliente responde (ex: "a", " B "), esta função valida o acerto
        pergunta = self.obter_pergunta(idx)
        if pergunta and resposta:
            # Pega só a primeira letra da resposta correta salva no JSON (ex: 'A')
            letra_certa = pergunta["resposta_correta"][0].upper()
            
            # Limpa espaços em branco e ignora maiúsculas/minúsculas do jogador
            return resposta.strip().upper() == letra_certa
        return False

    def obter_explicacao(self, idx):
        # PASSO 4: O Servidor chama esta função para enviar a explicação completa a todos os Clientes
        pergunta = self.obter_pergunta(idx)
        if pergunta:
            return pergunta["resposta_correta"]
        return ""

    def adicionar_jogador(self, nome):
        # PASSO 5: A Thread de conexão de cada Cliente registra o nome do jogador no início do jogo
        if nome not in self.pontuacoes:
            self.pontuacoes[nome] = 0

    def somar_ponto(self, nome):
        # PASSO 6: Se a resposta estiver certa, a Thread do Servidor soma +1 ponto ao jogador
        if nome in self.pontuacoes:
            self.pontuacoes[nome] += 1