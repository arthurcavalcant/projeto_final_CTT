CREATE DATABASE sistema_imobiliario;

CREATE TYPE estado_civil AS ENUM('solteira', 'casada', 'divorciada', 'viúva', 'união estável');

CREATE TABLE pessoa(
	id_pessoa SERIAL PRIMARY KEY,
	nome VARCHAR(255) NOT NULL, 
	cpf VARCHAR(11) UNIQUE NOT NULL,
	rg VARCHAR(7) UNIQUE NOT NULL,
	data_nascimento DATE NOT NULL,
	estado_civil_pessoa estado_civil NOT NULL,
	profissao VARCHAR(50) NOT NULL
);

CREATE TABLE proprietario(
	id_proprietario SERIAL PRIMARY KEY,
	id_pessoa INTEGER NOT NULL REFERENCES pessoa(id_pessoa)
);

CREATE TABLE vendedor(
	id_vendedor SERIAL PRIMARY KEY,
	id_pessoa INTEGER NOT NULL REFERENCES pessoa(id_pessoa)
);

CREATE TABLE cliente(
	id_cliente SERIAL PRIMARY KEY,
	id_pessoa INTEGER NOT NULL REFERENCES pessoa(id_pessoa)
);

CREATE TYPE tipo_imovel AS ENUM('casa', 'apartamento', 'kitnet');

CREATE TABLE imovel(
	id_imovel SERIAL PRIMARY KEY,
	id_proprietario INTEGER NOT NULL REFERENCES proprietario(id_proprietario),
	tipo_imovel tipo_imovel NOT NULL,
	rua VARCHAR(70) NOT NULL,
	numero INTEGER NOT NULL,
	andar INTEGER,
	bloco VARCHAR(25),
	cep NUMERIC NOT NULL,
	cidade VARCHAR(50) NOT NULL,
	uf VARCHAR(2) NOT NULL,
	data_posse_proprietario DATE NOT NULL
);

CREATE TABLE banco(
	id_banco SERIAL PRIMARY KEY,
	codigo_banco INTEGER NOT NULL,
	nome VARCHAR(255) NOT NULL
);

CREATE TYPE tipo_compra AS ENUM('à vista', 'financiamento');

CREATE TABLE compra(
	id_compra SERIAL PRIMARY KEY,
	id_imovel INTEGER NOT NULL REFERENCES imovel(id_imovel),
	id_proprietario INTEGER NOT NULL REFERENCES proprietario(id_proprietario),
	id_cliente INTEGER NOT NULL REFERENCES cliente(id_cliente),
	id_vendedor INTEGER NOT NULL REFERENCES vendedor(id_vendedor),
	valor_final NUMERIC NOT NULL,
	tipo_compra tipo_compra NOT NULL
);

CREATE TABLE financiamento(
	id_financiamento SERIAL PRIMARY KEY,
	id_compra INTEGER REFERENCES compra(id_compra),
	id_banco INTEGER REFERENCES banco(id_banco),
	parcelas INTEGER NOT NULL,
	entrada_porcentagem INTEGER NOT NULL
);

CREATE TABLE gasto_pre_venda(
	id_gasto_pre_venda SERIAL PRIMARY KEY,
	id_compra INTEGER NOT NULL REFERENCES compra(id_compra),
	nome VARCHAR(255) NOT NULL,
	gasto_total NUMERIC NOT NULL
);

