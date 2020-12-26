from pylatex.base_classes import Environment

class Bibliogr(Environment):
    """
    A class representing custom bibliography environment.

    This class represents a custom LaTeX environment named
    ``thebibliography``.
    """

    _latex_name = 'thebibliography'
    