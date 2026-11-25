import express from "express";
import http from "http";
import { Server } from "socket.io";
import path from "path";
import crypto from "crypto";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const server = http.createServer(app);
const io = new Server(server);

const PORT = 3000;
const TEMPO_PERGUNTA = 20000;

app.use(express.static(path.join(__dirname, "../front")));

const salas = new Map();

const perguntas = [
  {
    pergunta: "Quanto é 5 x 5?",
    opcoes: ["10", "20", "25", "30"],
    resposta: 2
  },
  {
    pergunta: "Qual é a capital do Brasil?",
    opcoes: ["Rio de Janeiro", "Brasília", "São Paulo", "Salvador"],
    resposta: 1
  },
  {
    pergunta: "Qual é o maior planeta do sistema solar?",
    opcoes: ["Terra", "Marte", "Júpiter", "Saturno"],
    resposta: 2
  },
  {
    pergunta: "Quantos lados tem um hexágono?",
    opcoes: ["4", "5", "6", "8"],
    resposta: 2
  },
  {
    pergunta: "Qual é o resultado de 100 / 4?",
    opcoes: ["20", "25", "30", "40"],
    resposta: 1
  }
];

function gerarCodigo() {
  let codigo;

  do {
    codigo = crypto.randomBytes(3).toString("hex").toUpperCase();
  } while (salas.has(codigo));

  return codigo;
}

function buscarSala(socket) {
  for (const sala of salas.values()) {
    if (sala.jogadores.has(socket.id)) {
      return sala;
    }
  }

  return null;
}

function atualizarSala(sala) {
  io.to(sala.codigo).emit("jogadores", {
    codigo: sala.codigo,
    jogadores: Array.from(sala.jogadores.values()),
    anfitriao: sala.anfitriao,
    status: sala.status
  });
}

function enviarPergunta(sala) {
  if (sala.timer) {
    clearTimeout(sala.timer);
  }

  if (sala.perguntaAtual >= perguntas.length) {
    finalizarPartida(sala);
    return;
  }

  sala.respondidos.clear();
  sala.inicioPergunta = Date.now();

  const pergunta = perguntas[sala.perguntaAtual];

  io.to(sala.codigo).emit("nova-pergunta", {
    numero: sala.perguntaAtual + 1,
    total: perguntas.length,
    pergunta: pergunta.pergunta,
    opcoes: pergunta.opcoes,
    tempo: TEMPO_PERGUNTA
  });

  sala.timer = setTimeout(() => {
    revelarResposta(sala);
  }, TEMPO_PERGUNTA);
}

function revelarResposta(sala) {
  if (sala.status !== "jogando") return;

  if (sala.timer) {
    clearTimeout(sala.timer);
    sala.timer = null;
  }

  const pergunta = perguntas[sala.perguntaAtual];

  io.to(sala.codigo).emit("resultado-pergunta", {
    resposta: pergunta.resposta,
    jogadores: Array.from(sala.jogadores.values())
      .sort((a, b) => b.pontos - a.pontos)
  });

  sala.perguntaAtual++;

  setTimeout(() => {
    if (salas.has(sala.codigo) && sala.status === "jogando") {
      enviarPergunta(sala);
    }
  }, 3000);
}

function finalizarPartida(sala) {
  sala.status = "finalizada";

  if (sala.timer) {
    clearTimeout(sala.timer);
    sala.timer = null;
  }

  const ranking = Array.from(sala.jogadores.values())
    .sort((a, b) => b.pontos - a.pontos);

  io.to(sala.codigo).emit("fim-partida", {
    ranking
  });
}

io.on("connection", (socket) => {
  console.log("Jogador conectado:", socket.id);

  socket.on("criar-sala", (nome, callback) => {
    if (typeof nome !== "string" || !nome.trim()) {
      return callback?.({ erro: "Digite um nome válido." });
    }

    const codigo = gerarCodigo();

    const sala = {
      codigo,
      anfitriao: socket.id,
      jogadores: new Map(),
      status: "aguardando",
      perguntaAtual: 0,
      respondidos: new Set(),
      inicioPergunta: null,
      timer: null
    };

    sala.jogadores.set(socket.id, {
      id: socket.id,
      nome: nome.trim().slice(0, 20),
      pontos: 0
    });

    salas.set(codigo, sala);
    socket.join(codigo);

    callback?.({
      sucesso: true,
      codigo
    });

    atualizarSala(sala);
  });

  socket.on("entrar-sala", (dados, callback) => {
    if (
      !dados ||
      typeof dados.codigo !== "string" ||
      typeof dados.nome !== "string" ||
      !dados.nome.trim()
    ) {
      return callback?.({ erro: "Dados inválidos." });
    }

    const codigo = dados.codigo.trim().toUpperCase();
    const sala = salas.get(codigo);

    if (!sala) {
      return callback?.({ erro: "Sala não encontrada." });
    }

    if (sala.status !== "aguardando") {
      return callback?.({ erro: "A partida já começou." });
    }

    if (sala.jogadores.size >= 10) {
      return callback?.({ erro: "Sala cheia." });
    }

    sala.jogadores.set(socket.id, {
      id: socket.id,
      nome: dados.nome.trim().slice(0, 20),
      pontos: 0
    });

    socket.join(codigo);

    callback?.({
      sucesso: true,
      codigo
    });

    atualizarSala(sala);
  });

  socket.on("iniciar-partida", (callback) => {
    const sala = buscarSala(socket);

    if (!sala) {
      return callback?.({ erro: "Você não está em uma sala." });
    }

    if (sala.anfitriao !== socket.id) {
      return callback?.({ erro: "Somente o anfitrião pode iniciar." });
    }

    if (sala.status !== "aguardando") {
      return callback?.({ erro: "A partida já começou." });
    }

    if (sala.jogadores.size < 2) {
      return callback?.({
        erro: "É necessário ter pelo menos 2 jogadores."
      });
    }

    sala.status = "jogando";
    sala.perguntaAtual = 0;

    for (const jogador of sala.jogadores.values()) {
      jogador.pontos = 0;
    }

    callback?.({ sucesso: true });

    atualizarSala(sala);
    enviarPergunta(sala);
  });

  socket.on("responder", (indice, callback) => {
    const sala = buscarSala(socket);

    if (!sala || sala.status !== "jogando") {
      return callback?.({ erro: "Partida indisponível." });
    }

    if (!Number.isInteger(indice) || indice < 0 || indice > 3) {
      return callback?.({ erro: "Resposta inválida." });
    }

    if (sala.respondidos.has(socket.id)) {
      return callback?.({ erro: "Você já respondeu." });
    }

    const jogador = sala.jogadores.get(socket.id);
    const pergunta = perguntas[sala.perguntaAtual];

    if (!jogador || !pergunta) {
      return callback?.({ erro: "Resposta indisponível." });
    }

    sala.respondidos.add(socket.id);

    const tempo = Date.now() - sala.inicioPergunta;
    const acertou = indice === pergunta.resposta;

    if (acertou && tempo <= TEMPO_PERGUNTA) {
      jogador.pontos += 1000 +
        Math.floor((TEMPO_PERGUNTA - tempo) / 1000) * 10;
    }

    callback?.({
      sucesso: true,
      acertou
    });

    io.to(sala.codigo).emit("progresso-respostas", {
      respondidos: sala.respondidos.size,
      total: sala.jogadores.size
    });

    if (sala.respondidos.size === sala.jogadores.size) {
      revelarResposta(sala);
    }
  });

  socket.on("sair-sala", () => {
    sairDaSala(socket);
  });

  socket.on("disconnect", () => {
    sairDaSala(socket);
    console.log("Jogador desconectado:", socket.id);
  });
});

function sairDaSala(socket) {
  const sala = buscarSala(socket);

  if (!sala) return;

  sala.jogadores.delete(socket.id);
  sala.respondidos.delete(socket.id);
  socket.leave(sala.codigo);

  if (sala.jogadores.size === 0) {
    if (sala.timer) clearTimeout(sala.timer);
    salas.delete(sala.codigo);
    return;
  }

  if (sala.anfitriao === socket.id) {
    sala.anfitriao = sala.jogadores.keys().next().value;
  }

  atualizarSala(sala);

  if (
    sala.status === "jogando" &&
    sala.respondidos.size === sala.jogadores.size
  ) {
    revelarResposta(sala);
  }
}

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "../front/login.html"));
});

server.listen(PORT, () => {
  console.log(`Servidor rodando em http://localhost:${PORT}`);
});