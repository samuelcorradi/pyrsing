class NotMatchException(Exception):
    pass

class NoAlternativesException(NotMatchException):
    pass

class GrammarSyntaxException(Exception):
    pass