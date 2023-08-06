import unittest
from pathlib import Path
from typing import Dict

import ame.tests.exemplos.dados_exemplos as entrada
from ame import Estrutura


def estruturas() -> Dict[str, Estrutura]:
    ests = {}
    for i in entrada.arquivos:
        arq = str(Path(__file__).parent.parent.parent.parent.joinpath(f'exemplos\\{i}.ame'))
        ests[i] = Estrutura(arq)
    return ests


e = estruturas()
r = entrada.resultados


class TestEstrutura(unittest.TestCase):

    def test_leitura_nos(self):
        for i in e:
            self.assertEqual(e[i].nos, entrada.nos[i])

    def test_leitura_materiais(self):
        for i in e:
            self.assertEqual(e[i].materiais, entrada.materiais[i])

    def test_leitura_secoes(self):
        for i in e:
            self.assertEqual(e[i].secoes, entrada.secoes[i])

    def test_leitura_elementos(self):
        for i in e:
            self.assertEqual(e[i].elementos, entrada.elementos[i])

    def test_graus_liberdade_por_no(self):
        for i in e:
            self.assertEqual(r[i]['graus_liberdade_por_no'], e[i].graus_liberdade_por_no())

    def test_graus_liberdade_impedidos(self):
        for i in e:
            self.assertEqual(r[i]['graus_liberdade_impedidos'], e[i].graus_liberdade_impedidos())

    def test_graus_liberdade_livres(self):
        for i in e:
            self.assertEqual(r[i]['graus_liberdade_livres'], e[i].graus_liberdade_livres())

    def test_graus_liberdade(self):
        for i in e:
            self.assertEqual(r[i]['graus_liberdade'], e[i].graus_liberdade())

    def test_matriz_rigidez(self):
        for i in e:
            self.assertEqual(r[i]['matriz_rigidez'], e[i].matriz_rigidez(False).tolist())
            self.assertEqual(r[i]['matriz_rigidez'], e[i].matriz_rigidez().toarray().tolist())

    def test_forcas_nodais_aplicadas(self):
        for i in e:
            self.assertEqual(r[i]['forcas_nodais_aplicadas'], e[i].forcas_nodais_aplicadas().tolist())

    def test_forcas_nodais_totais(self):
        for i in e:
            self.assertEqual(r[i]['forcas_nodais_totais'], e[i].forcas_nodais_totais().tolist())

    def test_deslocamentos(self):
        for i in e:
            self.assertEqual(r[i]['deslocamentos'], e[i].deslocamentos().tolist())

    def test_nos_apoiados(self):
        for i in e:
            self.assertEqual(r[i]['nos_apoiados'], e[i].nos_apoiados())

    def test_nos_carregados(self):
        for i in e:
            self.assertEqual(r[i]['nos_carregados'], e[i].nos_carregados())

    def test_elementos_carregados(self):
        for i in e:
            self.assertEqual(r[i]['elementos_carregados'], e[i].elementos_carregados())


if __name__ == '__main__':
    unittest.main()
