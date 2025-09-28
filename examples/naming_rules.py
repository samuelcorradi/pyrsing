"""
Example usage of pyrsing to demonstrate calling rules with and without
alias.
"""

from pyrsing.grammar import Grammar

if __name__=="__main__":
    ###################################################################
    # example using a simple grammar
    ###################################################################
    g = Grammar({'machine_types':'BASIC|COMPLEX'})
    r, i = g._parse_rule('Machine type: <machine_types>')
    r.print_tree()
    ###################################################################
    # another example using alias
    ###################################################################
    g = Grammar({'machine_types':'BASIC|COMPLEX'})
    r, i = g._parse_rule('Machine type: <machine_types:complexity_types>')
    r.print_tree()