import { db } from '../banco/db';

async function testarBanco() {
    const [resultado] = await db.query('SELECT 1');
    console.log(resultado);
}

testarBanco();