create database if not exists quiz;
use quiz;

create table usuarios (
  id int auto_increment primary key,
  nome varchar(100) not null,
  email varchar(150) not null unique,
  senha varchar(255) not null
);

create table salas (
  id int auto_increment primary key,
  codigo varchar(6) not null unique,
  status enum('waiting', 'playing', 'finished') default 'waiting'
);

create table sala_jogadores (
  idsala int not null,
  idusuario int not null,
  primary key (idsala, idusuario),
  foreign key (idsala) references salas(id),
  foreign key (idusuario) references usuarios(id)
);

create table partidas (
  id int auto_increment primary key,
  idsala int not null,
  status enum('playing', 'finished') default 'playing',
  vencedorid int null,
  foreign key (idsala) references salas(id),
  foreign key (vencedorid) references usuarios(id)
);

create table perguntas (
  id int auto_increment primary key,
  enunciado text not null,
  respostacorreta int not null
);

create table alternativas (
  id int auto_increment primary key,
  idpergunta int not null,
  texto varchar(255) not null,
  numero int not null,
  foreign key (idpergunta) references perguntas(id),
  unique (idpergunta, numero)
);

create table respostas (
  id int auto_increment primary key,
  idpartida int not null,
  idusuario int not null,
  idpergunta int not null,
  alternativaescolhida int not null,
  acertou boolean not null,
  foreign key (idpartida) references partidas(id),
  foreign key (idusuario) references usuarios(id),
  foreign key (idpergunta) references perguntas(id),
  foreign key (idpergunta, alternativaescolhida) references alternativas(idpergunta, numero),
  unique (idpartida, idusuario, idpergunta)
);

insert into usuarios (nome, email, senha) values
('ana', 'ana@quiz.test', 'exemplo'),
('bruno', 'bruno@gmail.com', 'exemplo'),
('carla', 'carla@gmail.com', 'exemplo'),
('diego', 'diego@gmail.com', 'exemplo');

insert into salas (codigo, status) values
('ab1234', 'finished'),
('cd5678', 'waiting'),
('ef9012', 'playing');

insert into sala_jogadores (idsala, idusuario) values
(1, 1),
(1, 2),
(2, 3),
(3, 1),
(3, 4);

insert into partidas (idsala, status, vencedorid) values
(1, 'finished', 1),
(3, 'playing', null);

insert into perguntas (enunciado, respostacorreta) values
('qual é a capital do brasil?', 2),
('quanto é 6 x 6?', 3),
('qual planeta é conhecido como planeta vermelho?', 1),
('qual linguagem é executada pelo node.js?', 4),
('quantos lados tem um hexágono?', 2);

insert into alternativas (idpergunta, texto, numero) values
(1, 'rio de janeiro', 1),
(1, 'brasília', 2),
(1, 'são paulo', 3),
(1, 'salvador', 4),
(2, '11', 1),
(2, '25', 2),
(2, '30', 3),
(2, '35', 4),
(3, 'marte', 1),
(3, 'vênus', 2),
(3, 'júpiter', 3),
(3, 'saturno', 4),
(4, 'python', 1),
(4, 'java', 2),
(4, 'c#', 3),
(4, 'javascript', 4),
(5, '5', 1),
(5, '6', 2),
(5, '7', 3),
(5, '8', 4);

insert into respostas (idpartida, idusuario, idpergunta, alternativaescolhida, acertou) values
(1, 1, 1, 2, true),
(1, 2, 1, 1, false),
(1, 1, 2, 3, true),
(1, 2, 2, 3, true);