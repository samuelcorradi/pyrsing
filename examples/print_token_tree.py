"""
Example usage of pyrsing to generate and print the token tree of an
expression.

This script creates a simple grammar, parses an expression, and
prints the hierarchical structure of the resulting tokens as a tree.
"""

from pyrsing.grammar import Grammar

if __name__=="__main__":
    g = Grammar({'logical_or':'OR'})
    r, i = g._parse_rule('(A AND (B <logical_or> C)) <logical_or> (D AND NOT E)')
    r.print_tree()
