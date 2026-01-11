import re
from typing import Optional
from pyrsing import ASTNode
from pyrsing.nodes import (
        SequenceNode,
        ProductionRuleNode,
        OrNode,
        GroupNode,
        TerminalNode,
        AnyNode
    )

class Grammar:
    """
    """
    def __init__(self, rules:dict):
        self.rules = rules
        self.root:ProductionRuleNode = None
        self.literal_buffer = ''

    def _literal_buffer_flush(self, stack:list):
        if self.literal_buffer and stack:
            scaped = False
            for char in self.literal_buffer:
                if scaped:
                    scaped = False
                    lit_node = TerminalNode(char)
                    stack[-1].children.append(lit_node)
                    continue
                elif char == '\\':
                    scaped = True
                    continue
                elif char == '.':
                    lit_node = AnyNode()
                    stack[-1].children.append(lit_node)
                elif char in '[]()|!<>{}':
                    raise Exception(f"Literal buffer contains special character '{char}'. Use escape '\\{char}' to include it as literal.")
                else:
                    lit_node = TerminalNode(char)
                    stack[-1].children.append(lit_node)
            self.literal_buffer = ''

    def _find_or_in_stack(self, stack:list):
        """
        Procura o node OrNode na pilha.
        Se encontrar um GroupNode antes, retorna None.
        Retorna None se não encontrar.
        """
        for tk in reversed(stack):
            if isinstance(tk, GroupNode):
                return None
            elif isinstance(tk, OrNode):
                return tk
        return None

    def ast_builder(self)->ASTNode:
        rule_str = self.rules.get('__root__', '')
        if not rule_str:
            raise Exception("Root rule '__root__' not found in grammar.")
        self.root = ProductionRuleNode('__root__')
        seq, _ = self._parse_rule(rule_str, self.root)
        # self.root.children = seq.children
        return self.root

    def _parse_rule(self, rule_str:str, parent_node:Optional[ASTNode]=None):
        i=0
        if parent_node is None:
            parent_node = SequenceNode()
        stack = [parent_node]
        while(i<len(rule_str)):
            char = rule_str[i]
            # negation
            if char=='!':
                if i>0:
                    raise Exception("Negation can only be indicated at position 0.")
                stack[-1].is_negation = True
            # repetition
            elif char in ['*', '+']:
                self._literal_buffer_flush(stack)
                last_node = stack[-1].children[-1]
                last_node.is_repeat = True
                last_node.is_optional = True if char=='*' else False
            # or
            elif char == '|':
                self._literal_buffer_flush(stack)
                or_token = self._find_or_in_stack(stack)
                if not or_token:
                    or_token = OrNode()
                    root_for_option = SequenceNode()
                    root_for_option.parent = or_token
                    root_for_option.children = stack[-1].children
                    or_token.children.append(root_for_option)
                    stack[-1].children = [or_token]
                    stack.append(or_token)
                tk = SequenceNode()
                tk.parent = or_token
                stack.append(tk)
                or_token.children.append(tk)
            # repetition indicating quantity
            elif char in '{':
                self._literal_buffer_flush(stack)
                m = re.findall(r'\{([0-9]+)\}', rule_str[i:])
                if m:
                    last_node = stack[-1].children[-1]
                    num_rep:str = m[0]
                    i+=len(num_rep)+1
                    last_node.num_repeat = int(num_rep)
                    last_node.is_repeat = True
                    last_node.is_optional = False
            # groups
            elif char in '[(':
                self._literal_buffer_flush(stack)
                tk = stack[-1]
                grp=GroupNode()
                grp, ii = self._parse_rule(rule_str[i+1:], parent_node=grp)
                i += ii
                tk.children.append(grp)
                if char=='[':
                    grp.is_optional = True
            # close group
            elif char in ')]':
                i+=1
                break
            # role
            elif char in '<':
                new_token = None
                self._literal_buffer_flush(stack)
                if char=='<':
                    mask = r'<[^>]+>'
                    match = re.match(mask, rule_str[i:])
                    if not match:
                        raise Exception(f"Syntax error on rule '{rule_str[i:]}' at position {i}.")
                    token_name, alias = ProductionRuleNode.parse_rule_name(match.group(0))
                    if token_name not in self.rules:
                        raise Exception(f"Production rule '{token_name}' not found in grammar.")
                    new_token = ProductionRuleNode(alias[1:] if alias else token_name)
                    seq, _ = self._parse_rule(self.rules[token_name], new_token)
                    i += match.end() - 1
                if new_token:
                    stack[-1].children.append(new_token)
            else:
                self.literal_buffer += char
            i += 1
        # adds what's left in the buffer
        self._literal_buffer_flush(stack)
        return parent_node, i