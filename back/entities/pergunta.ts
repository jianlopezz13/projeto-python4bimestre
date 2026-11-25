export class Pergunta {
    private idPergunta: number;
    public enunciado: string;
    public respostaCorreta: number;

    constructor(idPergunta: number, enunciado: string, respostaCorreta: number) {
        this.idPergunta = idPergunta;
        this.enunciado = enunciado;
        this.respostaCorreta = respostaCorreta;
    }

    public verificarResposta(alternativaEscolhida: number): boolean {
        return alternativaEscolhida === this.respostaCorreta;
    }
}