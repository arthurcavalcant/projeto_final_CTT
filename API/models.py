from dataclasses import dataclass
from datetime import date

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


@dataclass
class Pessoa(db.Model):
    id_pessoa: str
    nome: str
    cpf: str
    rg: str
    data_nascimento: date
    estado_civil_pessoa: str
    profissao: str

    id_pessoa = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    nome = db.Column(db.VARCHAR(255), nullable=False)
    cpf = db.Column(db.CHAR(11), unique=True, nullable=False)
    rg = db.Column(db.CHAR(7), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    estado_civil_pessoa = db.Column(db.Enum('solteira', 'casada', 'viúva', 'divorciada', 'união estável',
                                            name='estado_civil'), nullable=False)
    profissao = db.Column(db.VARCHAR(50), nullable=False)


@dataclass
class Proprietario(db.Model):
    id_proprietario: int
    id_pessoa: int

    id_proprietario = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    id_pessoa = db.Column(db.INTEGER, db.ForeignKey('pessoa.id_pessoa'), nullable=False)


@dataclass
class Cliente(db.Model):
    id_cliente: int
    id_pessoa: int

    id_cliente = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    id_pessoa = db.Column(db.INTEGER, db.ForeignKey('pessoa.id_pessoa', ondelete='CASCADE'), nullable=False, unique=True)


class Vendedor(db.Model):
    id_vendedor: int
    id_pessoa: int

    id_vendedor = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    id_pessoa = db.Column(db.INTEGER, db.ForeignKey('pessoa.id_pessoa'), nullable=False)


class Imovel(db.Model):
    id_imovel: int
    id_proprietario: int
    tipo_imovel: str
    rua: str
    numero: int
    bloco: str
    cep: str
    cidade: str
    uf: str
    data_posse_proprietario: date

    id_imovel = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    id_proprietario = db.Column(db.INTEGER, db.ForeignKey('proprietario.id_proprietario'), nullable=False)
    tipo_imovel = db.Column(db.Enum('apartamento', 'casa', 'kitnet', name='tipo_imovel'), nullable=False)
    rua = db.Column(db.VARCHAR(70), nullable=False)
    numero = db.Column(db.INTEGER, nullable=False)
    andar = db.Column(db.INTEGER, nullable=True)
    bloco = db.Column(db.VARCHAR(25), nullable=True)
    cep = db.Column(db.CHAR(8), nullable=True)
    cidade = db.Column(db.VARCHAR(50), nullable=False)
    uf = db.Column(db.CHAR(2), nullable=False)
    data_posse_proprietario = db.Column(db.DATE, nullable=False)


class Banco(db.Model):
    id_banco: int
    codigo_banco: int
    nome: str

    id_banco = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    codigo_banco = db.Column(db.INTEGER, nullable=False)
    nome = db.Column(db.VARCHAR(255), nullable=False)


class Compra(db.Model):
    id_compra: int
    id_imovel: int
    id_proprietario: int
    id_cliente: int
    id_vendedor: int
    valor: float
    tipo_compra: str

    id_compra = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    id_imovel = db.Column(db.INTEGER, db.ForeignKey('imovel.id_imovel'), nullable=False)
    id_proprietario = db.Column(db.INTEGER, db.ForeignKey('proprietario.id_proprietario'), nullable=False)
    id_cliente = db.Column(db.INTEGER, db.ForeignKey('cliente.id_cliente'), nullable=False)
    id_vendedor = db.Column(db.INTEGER, db.ForeignKey('vendedor.id_pvendedor'), nullable=False)
    valor = db.Column(db.NUMERIC, nullable=False)
    tipo_compra = db.Column(db.Enum('à vista', 'financiamento', name='tipo_compra'), nullable=False)


class Financiamento(db.Model):
    id_financiamento: int
    id_compra: int
    id_banco: int
    parcelas: int
    entrada_porcentagem: int

    id_financiamento = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    id_compra = db.Column(db.INTEGER, db.ForeignKey('compra.id_compra'), nullable=False)
    id_banco = db.Column(db.INTEGER, db.ForeignKey('banco.id_banco'), nullable=False)
    parcelas = db.Column(db.INTEGER, nullable=False)
    entrada_porcentagem = db.Column(db.INTEGER, nullable=False)


class GastoPreVenda(db.Model):
    id_gasto_pre_venda: int
    id_compra: int
    nome: str
    valor: float

    id_gasto_pre_venda = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    id_compra = db.Column(db.INTEGER, db.ForeignKey('compra.id_compra'), nullable=False)
    nome = db.Column(db.VARCHAR(255), nullable=False)
    valor = db.Column(db.NUMERIC, nullable=False)
