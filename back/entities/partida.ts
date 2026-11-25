export class Partida {
    private idPartida: number;
    public idSala: number;
    public status: string;
    public vencedorId: number | null;

    constructor(idPartida: number, idSala: number, status: string, vencedorId: number | null) {
        this.idPartida = idPartida;
        this.idSala = idSala;
        this.status = status;
        this.vencedorId = vencedorId;
    }

    public finalizarPartida(vencedorId: number): void {
        if (this.status !== "playing") {
            throw new Error("A partida não está acontecendo");
        }

        this.vencedorId = vencedorId;
        this.status = "finished";
    }
}