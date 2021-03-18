CREATE DATABASE sistema_imobiliario;

CREATE TYPE estado_civil AS ENUM('solteira', 'casada', 'divorciada', 'viúva', 'união estável');

CREATE TABLE pessoa(
	id_pessoa SERIAL PRIMARY KEY,
	nome VARCHAR(255) NOT NULL, 
	cpf CHAR(11) UNIQUE NOT NULL,
	rg CHAR(7) UNIQUE NOT NULL,
	data_nascimento DATE NOT NULL,
	estado_civil_pessoa estado_civil NOT NULL,
	profissao VARCHAR(50) NOT NULL
);

CREATE TABLE proprietario(
	id_proprietario SERIAL PRIMARY KEY,
	id_pessoa INTEGER UNIQUE NOT NULL REFERENCES pessoa(id_pessoa) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE vendedor(
	id_vendedor SERIAL PRIMARY KEY,
	id_pessoa INTEGER UNIQUE NOT NULL REFERENCES pessoa(id_pessoa) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE cliente(
	id_cliente SERIAL PRIMARY KEY,
	id_pessoa INTEGER UNIQUE NOT NULL REFERENCES pessoa(id_pessoa) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TYPE tipo_imovel AS ENUM('casa', 'apartamento', 'kitnet');

CREATE TABLE imovel(
	id_imovel SERIAL PRIMARY KEY,
	id_proprietario INTEGER NOT NULL REFERENCES proprietario(id_proprietario) ON DELETE CASCADE ON UPDATE CASCADE,
	tipo_imovel tipo_imovel NOT NULL,
	rua VARCHAR(70) NOT NULL,
	numero INTEGER NOT NULL,
	andar INTEGER,
	bloco VARCHAR(25),
	cep CHAR(8) NOT NULL,
	cidade VARCHAR(50) NOT NULL,
	uf CHAR(2) NOT NULL,
	data_posse_proprietario DATE NOT NULL
);

CREATE TABLE banco(
	id_banco SERIAL PRIMARY KEY,
	codigo_banco INTEGER NOT NULL UNIQUE,
	nome VARCHAR(255) NOT NULL
);

/*DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;*/

CREATE TYPE tipo_venda AS ENUM('à vista', 'financiamento');

CREATE TABLE venda(
	id_venda SERIAL PRIMARY KEY,
	id_imovel INTEGER NOT NULL REFERENCES imovel(id_imovel) ON DELETE CASCADE ON UPDATE CASCADE,
	id_proprietario INTEGER NOT NULL REFERENCES proprietario(id_proprietario) ON DELETE CASCADE ON UPDATE CASCADE,
	id_cliente INTEGER NOT NULL REFERENCES cliente(id_cliente) ON DELETE CASCADE ON UPDATE CASCADE,
	id_vendedor INTEGER NOT NULL REFERENCES vendedor(id_vendedor) ON DELETE CASCADE ON UPDATE CASCADE,
	valor NUMERIC NOT NULL,
	tipo_venda tipo_venda NOT NULL
);

CREATE TABLE financiamento(
	id_financiamento SERIAL PRIMARY KEY,
	id_venda INTEGER REFERENCES venda(id_venda) ON DELETE CASCADE ON UPDATE CASCADE,
	id_banco INTEGER REFERENCES banco(id_banco) ON DELETE CASCADE ON UPDATE CASCADE,
	parcelas INTEGER NOT NULL,
	entrada_porcentagem INTEGER NOT NULL
);

CREATE TABLE gasto_pre_venda(
	id_gasto_pre_venda SERIAL PRIMARY KEY,
	id_venda INTEGER NOT NULL REFERENCES venda(id_venda) ON DELETE CASCADE ON UPDATE CASCADE,
	nome VARCHAR(255) NOT NULL,
	gasto_total NUMERIC NOT NULL
);

