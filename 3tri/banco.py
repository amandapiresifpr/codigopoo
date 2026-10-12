import datetime
from peewee import *

db = SqliteDatabase("ranking.db")


class BaseModel(Model):
    class Meta:
        database = db


class Pontuacao(BaseModel):
    nome_jogador = CharField()
    pontos = IntegerField()
    tempo_partida = FloatField()
    data_hora = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"{self.nome_jogador} - {self.pontos} pts ({self.tempo_partida:.1f}s)"


def inicializar_banco():
    db.connect(reuse_if_open=True)
    db.create_tables([Pontuacao])
