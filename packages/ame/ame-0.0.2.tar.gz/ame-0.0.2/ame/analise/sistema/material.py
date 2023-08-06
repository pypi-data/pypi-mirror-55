from ame.analise.sistema.elemento_numerado import ElementoNumerado


class Material(ElementoNumerado):
    """Classe que implementa as propriedades de um material genérico."""

    def __init__(self, identificacao: int, mod_elastic: float, poisson: float,
                 coef_dilat_termica: float = 1e-4):
        """Construtor.

        Args:
            mod_elastic: Módulo de elasticidade.
            poisson: Coeficiente de Poison.
            coef_dilat_termica: Coeficiente de dilatação térmica.

        Examples:
            >>> import ame
            >>> m1 = ame.Material(1, 200e9, 0.2)
            >>> m2 = ame.Material(2, 25e9, 0.3)

            >>> m1 == m2
            False
            >>> m1 == ame.Material(1, 200e9, 0.2, 1e-4)
            True

            >>> m1.modulo_cisalhamento()
            83333333333.33334
            >>> m2.modulo_cisalhamento()
            9615384615.384615
        """
        super().__init__(identificacao)
        self.mod_elastic = mod_elastic
        self.poisson = poisson
        self.coef_dilat_termica = coef_dilat_termica

    def __eq__(self, other):
        """Condição de igualdade entre as intâncias da classe.

        Args:
            other(Material): Instância da classe material.
        """
        return bool(self.identificacao == other.identificacao and self.poisson == other.poisson and
                    self.mod_elastic == other.mod_elastic and self.coef_dilat_termica == other.coef_dilat_termica)

    def __repr__(self):
        return f'Material {self.identificacao}:\n' \
               f'\tPoisson: {self.poisson}\n' \
               f'\tE: {self.mod_elastic:.2e}Pa\n' \
               f'\tG: {self.modulo_cisalhamento():.2e}Pa\n' \
               f'\tAlpha: {self.coef_dilat_termica:.2e}°C^-1\n'

    # region Propriedades
    @property
    def poisson(self) -> float:
        """Coeficiente de Poisson.

        Raises:
            TypeError:
                Se o tipo de dado não for float.
            ValueError:
                Se valu não obedecer os limites 0.5 >= value > 0.
        """
        return self._poisson

    @poisson.setter
    def poisson(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError(f'O tipo de dado "{type(value)}" não é válido para representar o Coeficiente de Poisson!')
        elif not 0.5 >= value > 0:
            raise ValueError('O valor do Coeficiente de Poisson deve ser maior que 0 e no máximo 0.5!')
        else:
            self._poisson = value

    @property
    def mod_elastic(self) -> float:
        """Módulo de elasticidade do material.

        Raises:
            TypeError:
                Se o tipo de dado não for float.
            ValueError:
                Se value não for maior que 0.
        """
        return self._mod_elastic

    @mod_elastic.setter
    def mod_elastic(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError(f'O tipo de dado "{type(value)}" não é válido para representar o módulo de elasticidade!')
        elif not value > 0:
            raise ValueError('O valor do módulo de elasticidade deve ser maior que 0!')
        else:
            self._mod_elastic = value

    @property
    def coef_dilat_termica(self) -> float:
        """Coeficiente de dilatação térmica.

        Raises:
            TypeError:
                Se o tipo de dado não for float.
            ValueError:
                Se value não for maior que 0.
        """
        return self._coef_dilat_termica

    @coef_dilat_termica.setter
    def coef_dilat_termica(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError(f'O tipo de dado "{type(value)}" não é válido para representar o coeficiente de dilatação '
                            f'térmica!')
        elif not value > 0:
            raise ValueError(f'O valor do coeficiente de dilatação térmica deve ser maior que 0!')
        else:
            self._coef_dilat_termica = value

    # endregion

    def modulo_cisalhamento(self) -> float:
        """Retorna o módulo de elasticidade transversal do material (módulo de cisalhamento)."""
        return self.mod_elastic / (2 * (1 + self.poisson))
