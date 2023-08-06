import unittest
from typing import Dict

from ame import Apoio

# region Dados de entrada

entrada_apoios = {1: [True, True, True],
                  2: [False, True, True],
                  3: [True, False, True],
                  4: [True, True, False],
                  5: [True, False, False],
                  6: [False, True, False],
                  7: [False, False, True],
                  8: [False, False, False]}


def criar_apoios() -> Dict[int, Apoio]:
    apoios = {}
    for i, ap in enumerate(entrada_apoios):
        apoios[i + 1] = Apoio(*entrada_apoios[i + 1])
    return apoios


result_metodos = {'apoio_livre': {1: True,
                                  2: False,
                                  3: False,
                                  4: False,
                                  5: False,
                                  6: False,
                                  7: False,
                                  8: False}}

erros = [[str(True), True, True, TypeError, f'O tipo de dado "{str(str)}" não é válido para representar a '
                                            f'deslocabilidade do grau de liberdade dx!'],
         [True, str(True), True, TypeError, f'O tipo de dado "{str(str)}" não é válido para representar a '
                                            f'deslocabilidade do grau de liberdade dy!'],
         [True, True, str(True), TypeError, f'O tipo de dado "{str(str)}" não é válido para representar a '
                                            f'deslocabilidade do grau de liberdade rz!']]


# endregion

class TestApoio(unittest.TestCase):
    def test_eq(self):
        for i in entrada_apoios:
            for j in entrada_apoios:
                ap1 = Apoio(*entrada_apoios[i])
                ap2 = Apoio(*entrada_apoios[j])

                if i == j:
                    self.assertTrue(ap1 == ap2)
                else:
                    self.assertFalse(ap1 == ap2)

    def test_apoio_livre(self):
        apoios = {}
        for i, ap in enumerate(entrada_apoios):
            apoios[i + 1] = Apoio(*entrada_apoios[i + 1])

        r = result_metodos['apoio_livre']

        for i in r:
            self.assertIs(apoios[i].apoio_livre(), r[i])

    def test_erros_entrada(self):
        for i in erros:
            with self.assertRaisesRegex(i[3], i[4]):
                Apoio(*i[:3:])


if __name__ == '__main__':
    unittest.main()
