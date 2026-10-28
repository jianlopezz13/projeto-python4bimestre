

import random
from fastapi import FastAPI

app = FastAPI()

# Seu banco de dados de perguntas
banco_de_perguntas = [
    {
        "pergunta": "Qual é a capital do Brasil?",
        "opcoes": ["A) Rio de Janeiro", "B) Brasília", "C) São Paulo", "D) Salvador"],
        "resposta_correta": "B",
    },
    {
        "pergunta": "Quantos planetas existem no Sistema Solar?",
        "opcoes": ["A) 7", "B) 9", "C) 8", "D) 10"],
        "resposta_correta": "C",
    },
]


# Esta é a rota que você vai acessar no navegador
@app.get("/")
def entregar_quiz():
    # Criamos uma cópia para poder embaralhar
    perguntas_misturadas = banco_de_perguntas.copy()
    random.shuffle(perguntas_misturadas)

    # O 'return' envia os dados direto para o navegador. Sem print, sem input!
    return {"status": "sucesso", "perguntas": perguntas_misturadas}


import random
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

banco_de_perguntas = [
    {
        "pergunta": "Qual é a capital do Brasil?",
        "opcoes": ["Rio de Janeiro", "Brasília", "São Paulo", "Salvador"],
        "resposta_correta": "Brasília",
    },
    {
        "pergunta": "Quantos planetas existem no Sistema Solar?",
        "opcoes": ["7", "9", "8", "10"],
        "resposta_correta": "8",
    },
    {
        "pergunta": "Qual é o maior oceano da Terra?",
        "opcoes": ["Atlântico", "Índico", "Ártico", "Pacífico"],
        "resposta_correta": "Pacífico",
    },
]


# 1. API Route: Returns only the raw question data
@app.get("/api/quiz")
def obter_perguntas():
    lista_embaralhada = banco_de_perguntas.copy()
    random.shuffle(lista_embaralhada)
    return lista_embaralhada


# 2. HTML Route: Returns a beautiful visual page that plays the quiz!
@app.get("/", response_class=HTMLResponse)
def pagina_principal():
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Super Quiz FastAPI</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f9; text-align: center; padding: 50px; }
            .quiz-container { background: white; max-width: 500px; margin: 0 auto; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            button { display: block; width: 100%; margin: 10px 0; padding: 12px; font-size: 16px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background-color: #0056b3; }
            #resultado { font-weight: bold; margin-top: 20px; font-size: 18px; }
        </style>
    </head>
    <body>
        <div class="quiz-container">
            <h1>🎯 Meu Quiz FastAPI</h1>
            <div id="quiz-box">
                <p id="pergunta">Carregando pergunta...</p>
                <div id="opcoes"></div>
            </div>
            <p id="resultado"></p>
        </div>

        <script>
            let perguntas = [];
            let perguntaAtual = 0;
            let pontuacao = 0;

            // This JavaScript fetches data from your own FastAPI endpoint!
            async function carregarQuiz() {
                const response = await fetch('/api/quiz');
                perguntas = await response.json();
                mostrarPergunta();
            }

            function mostrarPergunta() {
                if (perguntaAtual >= perguntas.length) {
                    document.getElementById('quiz-box').innerHTML = `<h2>🏁 Fim de Jogo!</h2>`;
                    document.getElementById('resultado').innerText = `Sua pontuação final: ${pontuacao}/${perguntas.length}`;
                    return;
                }

                const item = perguntas[perguntaAtual];
                document.getElementById('pergunta').innerText = `Pergunta ${perguntaAtual + 1}: ${item.pergunta}`;
                
                const opcoesDiv = document.getElementById('opcoes');
                opcoesDiv.innerHTML = '';
                
                item.opcoes.forEach(opcao => {
                    const btn = document.createElement('button');
                    btn.innerText = opcao;
                    btn.onclick = () => verificarResposta(opcao, item.resposta_correta);
                    opcoesDiv.appendChild(btn);
                });
            }

            function verificarResposta(escolha, correta) {
                const resP = document.getElementById('resultado');
                if (escolha === correta) {
                    resP.innerText = "✨ Resposta CORRETA!";
                    resP.style.color = "green";
                    pontuacao++;
                } else {
                    resP.innerText = `❌ Errou! A certa era: ${correta}`;
                    resP.style.color = "red";
                }
                
                perguntaAtual++;
                setTimeout(() => {
                    resP.innerText = "";
                    mostrarPergunta();
                }, 1500);
            }

            carregarQuiz();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
