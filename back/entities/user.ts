export class Usuario{
    private senha: string;
    private idUsuario: number;
    public nome: string;
    constructor(idUsuario:number, nome:string, senha:string,){
        this.nome = nome;
        this.senha = senha;
        this.idUsuario = idUsuario

    }

   public getNome():string{
        return this.nome;

    }

 
    public getidUsuario():number{
        return this.idUsuario;

    }
    public alterarNome(nome:string):void{
        if(!nome || !nome.trim()){
            throw new Error("nao existe esse usuario")
        }

        this.nome = nome;
         
    }


}