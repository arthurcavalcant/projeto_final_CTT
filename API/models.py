from dataclasses import dataclass
from datetime import date

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


@dataclass
class Pessoa(db.Model):
    id_pessoa: int
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
    id_pessoa = db.Column(db.INTEGER, db.ForeignKey('pessoa.id_pessoa', ondelete='CASCADE', onupdate='CASCADE'),
                          nullable=False)


@dataclass
class Cliente(db.Model):
    id_cliente: int
    id_pessoa: int

    id_cliente = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    id_pessoa = db.Column(db.INTEGER, db.ForeignKey('pessoa.id_pessoa', ondelete='CASCADE', onupdate='CASCADE'),
                          nullable=False,
                          unique=True)


@dataclass
class Vendedor(db.Model):
    id_vendedor: int
    id_pessoa: int

    id_vendedor = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    id_pessoa = db.Column(db.INTEGER, db.ForeignKey('pessoa.id_pessoa', ondelete='CASCADE', onupdate='CASCADE'),
                          nullable=False)


@dataclass
class Imovel(db.Model):
    id_imovel: int
    id_proprietario: int
    tipo_imovel: str
    rua: str
    numero: int
    andar: int
    bloco: str
    cep: str
    cidade: str
    uf: str
    data_posse_proprietario: date

    id_imovel = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    id_proprietario = db.Column(db.INTEGER, db.ForeignKey('proprietario.id_proprietario', ondelete='CASCADE',
                                                          onupdate='CASCADE'), nullable=False)
    tipo_imovel = db.Column(db.Enum('apartamento', 'casa', 'kitnet', name='tipo_imovel'), nullable=False)
    rua = db.Column(db.VARCHAR(70), nullable=False)
    numero = db.Column(db.INTEGER, nullable=False)
    andar = db.Column(db.INTEGER, nullable=True)
    bloco = db.Column(db.VARCHAR(25), nullable=True)
    cep = db.Column(db.CHAR(8), nullable=False)
    cidade = db.Column(db.VARCHAR(50), nullable=False)
    uf = db.Column(db.CHAR(2), nullable=False)
    data_posse_proprietario = db.Column(db.DATE, nullable=False)


@dataclass
class Banco(db.Model):
    id_banco: int
    codigo_banco: int
    nome: str

    id_banco = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    codigo_banco = db.Column(db.INTEGER, nullable=False, unique=True)
    nome = db.Column(db.VARCHAR(255), nullable=False)


@dataclass
class Venda(db.Model):
    id_venda: int
    id_imovel: int
    id_proprietario: int
    id_cliente: int
    id_vendedor: int
    valor: float
    tipo_venda: str

    id_venda = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    id_imovel = db.Column(db.INTEGER, db.ForeignKey('imovel.id_imovel', ondelete='CASCADE', onupdate='CASCADE'),
                          nullable=False)
    id_proprietario = db.Column(db.INTEGER,
                                db.ForeignKey('proprietario.id_proprietario', ondelete='CASCADE', onupdate='CASCADE'),
                                nullable=False)
    id_cliente = db.Column(db.INTEGER, db.ForeignKey('cliente.id_cliente', ondelete='CASCADE', onupdate='CASCADE'),
                           nullable=False)
    id_vendedor = db.Column(db.INTEGER, db.ForeignKey('vendedor.id_vendedor', ondelete='CASCADE', onupdate='CASCADE'),
                            nullable=False)
    valor = db.Column(db.FLOAT, nullable=False)
    tipo_venda = db.Column(db.Enum('à vista', 'financiamento', name='tipo_venda'), nullable=False)


@dataclass
class Financiamento(db.Model):
    id_financiamento: int
    id_venda: int
    id_banco: int
    parcelas: int
    entrada_porcentagem: int

    id_financiamento = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    id_venda = db.Column(db.INTEGER, db.ForeignKey('venda.id_venda', ondelete='CASCADE', onupdate='CASCADE'),
                         nullable=False)
    id_banco = db.Column(db.INTEGER, db.ForeignKey('banco.id_banco', ondelete='CASCADE', onupdate='CASCADE'),
                         nullable=False)
    parcelas = db.Column(db.INTEGER, nullable=False)
    entrada_porcentagem = db.Column(db.INTEGER, nullable=False)


@dataclass
class GastoPreVenda(db.Model):
    id_gasto_pre_venda: int
    id_venda: int
    nome: str
    valor: float

    id_gasto_pre_venda = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    id_venda = db.Column(db.INTEGER, db.ForeignKey('venda.id_venda', ondelete='CASCADE', onupdate='CASCADE'),
                         nullable=False)
    nome = db.Column(db.VARCHAR(255), nullable=False)
    valor = db.Column(db.NUMERIC, nullable=False)
