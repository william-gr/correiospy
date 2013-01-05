from decimal import Decimal
import logging

from suds.client import Client

log = logging.getLogger('correiospy.base')


class Correios(object):

    PAC = 41106
    SEDEX = 40010
    SEDEX_10 = 40215
    SEDEX_HOJE = 40290
    ESEDEX = 81019
    OTE = 44105
    NORMAL = 41017
    SEDEX_A_COBRAR = 40045

    FORMATO_CAIXA = 1
    FORMATO_ROLO = 2
    FORMATO_ENVELOPE = 3

    def __init__(self, webservice=None):
        if webservice is not None:
            self._webservice = webservice
        else:
            self._webservice = (
                "http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx?WSDL"
                )

    def frete(
        self,
        tipo=None,
        origem=None,
        destino=None,
        peso=None,
        formato=FORMATO_CAIXA,
        comprimento='0',
        altura='0',
        largura='0',
        diametro='0',
        mao_propria=False,
        aviso_recebimento=False
    ):
        mao_propria = 'S' if mao_propria is True else 'N'
        aviso_recebimento = 'S' if aviso_recebimento is True else 'N'

        client = Client(self._webservice)
        calc = client.service.CalcPreco(
            '',
            '',
            tipo,
            origem,
            destino,
            peso,
            Correios.FORMATO_CAIXA,
            comprimento,
            altura,
            largura,
            diametro,
            mao_propria,
            '0',
            aviso_recebimento)
        for servico in calc.Servicos:
            servico = servico[1][0]
            if servico.Erro is not None:
                raise ValueError(servico.MsgErro)
            return Decimal(servico.Valor.replace(',', '.'))
