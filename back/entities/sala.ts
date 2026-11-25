import { Usuario } from "./user";


export class Sala{
    private idSala: number;
    public codigo: string;
    public status: string;
    public jogadores: number[];

    constructor(idSala:number, codigo:string, status:string, jogadores: number[]){
        this.idSala = idSala;
        this.codigo = codigo;
        this.status = status;
        this.jogadores = jogadores;


    }




    public adicionarJogador(idJogador:number,idSala:number, codigo:string):void{
        if(!codigo){
            throw new Error
        }
        this.jogadores.push(idJogador)
    }

        public removerJogador(id: number): void {
    this.jogadores = this.jogadores.filter(
        jogador => jogador !== id
    );
}
    
        public iniciarPartida(): void {
    if (this.status !== "waiting") {
        throw new Error("a sala nao esta abeta para novos jogadores");
    }

    if (this.jogadores.length !== 2) {
        throw new Error("a sala precisa de dois jogadores");
    }

    this.status = "playing";
}
        
        
    }
        
        
    
        
    