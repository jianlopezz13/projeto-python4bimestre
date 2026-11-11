from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
import random
app = FastAPI()


codigo = (random.randint(1000,10000)) 



def obter_perguntas():
    with open("../web/perguntas.json", "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)  
    

salas = {
    "sala": [],
    "status": [],
    "codigo":[codigo]
}

@app.get("/jogo", response_class=HTMLResponse)
def oi():
    html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz de Lógica</title>
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        #quiz-container {
            background: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            max-width: 600px;
            width: 100%;
        }
        h2 {
            color: #333;
            font-size: 1.2rem;
            margin-bottom: 20px;
            line-height: 1.5;
        }
        .option {
            display: block;
            margin: 10px 0;
            padding: 12px 15px;
            background: #e9ecef;
            border: 2px solid transparent;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            text-align: left;
            font-size: 1rem;
            transition: all 0.2s ease;
        }
        .option:hover:not(:disabled) {
            background: #dee2e6;
        }
        .option:disabled {
            cursor: not-allowed;
            opacity: 0.8;
        }
        .correct {
            background: #d4edda !important;
            border-color: #c3e6cb !important;
            color: #155724;
        }
        .wrong {
            background: #f8d7da !important;
            border-color: #f5c6cb !important;
            color: #721c24;
        }
        #feedback {
            margin: 20px 0;
            font-weight: 500;
            font-size: 0.95rem;
            min-height: 45px;
            line-height: 1.4;
        }
        #next-btn {
            background: #007bff;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            display: none;
            font-size: 1rem;
            font-weight: bold;
            width: 100%;
            transition: background 0.2s;
        }
        #next-btn:hover {
            background: #0056b3;
        }
        #progress {
            text-align: right;
            font-size: 0.85rem;
            color: #6c757d;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>

    <div id="quiz-container">
        <div id="progress"></div>
        <h2 id="question">Carregando perguntas...</h2>
        <div id="options"></div>
        <div id="feedback"></div>
        <button id="next-btn">Próxima Pergunta</button>
    </div>

    <script>
        let quizData = [];
        let currentQuestionIndex = 0;
        let score = 0;

        const questionEl = document.getElementById('question');
        const optionsEl = document.getElementById('options');
        const feedbackEl = document.getElementById('feedback');
        const nextBtn = document.getElementById('next-btn');
        const progressEl = document.getElementById('progress');

        // Busca o JSON externo
        async function carregarDados() {
            try {
                // Certifique-se de que o arquivo perguntas.json está na mesma pasta que este index.html
                const response = await fetch('/perguntas');
                if (!response.ok) throw new Error('Falha ao carregar o arquivo');
                
                quizData = await response.json();
                loadQuestion();
            } catch (error) {
                questionEl.innerHTML = `<span style="color:red;">Erro ao carregar as perguntas. Certifique-se de estar rodando um servidor local (Live Server) e que o arquivo 'perguntas.json' existe.</span>`;
                console.error(error);
            }
        }

        function loadQuestion() {
            feedbackEl.textContent = '';
            nextBtn.style.display = 'none';
            optionsEl.innerHTML = '';
            
            progressEl.textContent = `Pergunta ${currentQuestionIndex + 1} de ${quizData.length}`;
            
            const currentData = quizData[currentQuestionIndex];
            questionEl.textContent = currentData.pergunta;

            currentData.opcoes.forEach(opcao => {
                const btn = document.createElement('button');
                btn.textContent = opcao;
                btn.classList.add('option');
                btn.onclick = () => selectAnswer(btn, opcao, currentData.resposta_correta);
                optionsEl.appendChild(btn);
            });
        }

        function selectAnswer(selectedBtn, selectedText, correctFullAnswer) {
            const isCorrect = correctFullAnswer.startsWith(selectedText);
            const allButtons = document.querySelectorAll('.option');

            allButtons.forEach(btn => {
                btn.disabled = true;
                if (correctFullAnswer.startsWith(btn.textContent)) {
                    btn.classList.add('correct');
                }
            });

            if (isCorrect) {
                score++;
                feedbackEl.style.color = '#155724';
                feedbackEl.textContent = "Acertou! 🎉 " + correctFullAnswer;
            } else {
                selectedBtn.classList.add('wrong');
                feedbackEl.style.color = '#721c24';
                feedbackEl.textContent = "Errou! ❌ A explicação é: " + correctFullAnswer;
            }

            nextBtn.style.display = 'block';
            if (currentQuestionIndex === quizData.length - 1) {
                nextBtn.textContent = 'Ver Resultado Final';
            }
        }

        nextBtn.addEventListener('click', () => {
            currentQuestionIndex++;
            if (currentQuestionIndex < quizData.length) {
                loadQuestion();
            } else {
                showResults();
            }
        });

        function showResults() {
            progressEl.textContent = 'Fim de Jogo!';
            questionEl.innerHTML = `Você acertou <strong>${score}</strong> de <strong>${quizData.length}</strong> perguntas.`;
            optionsEl.innerHTML = '';
            feedbackEl.textContent = '';
            nextBtn.style.display = 'block';
            nextBtn.textContent = 'Jogar Novamente';
            nextBtn.onclick = () => {
                currentQuestionIndex = 0;
                score = 0;
                nextBtn.onclick = null;
                nextBtn.textContent = 'Próxima Pergunta';
                loadQuestion();
            };
        }

        // Inicia buscando o JSON
        carregarDados();
    </script>
</body>
</html>
   
    """

    return HTMLResponse(content=html_content)
