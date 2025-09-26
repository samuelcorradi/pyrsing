import re
from pyrsing.tokens import Or, Group
from pyrsing import Token

class Grammar:
    """
    """
    def __init__(self, grammar:dict):
        self.grammar = grammar
        self.root = Token()
        self.rules = dict()
        self.literal_buffer = ''

    def _literal_buffer_flush(self, stack:list):
        if self.literal_buffer and stack:
            stack[-1].childrens.append(self.literal_buffer)
            self.literal_buffer = ''

    def _parse_rule(self, rule_str:str, root:Token=None):
        i=0
        if root is None:
            root = Token()
        stack = [root]
        while(i<len(rule_str)):
            char = rule_str[i]
            # or
            if char=='!':
                if i>0:
                    raise Exception("Somente na posicao 0 que pode ser indicada a negacao.")
                stack[-1].negation = True
            elif char == '|':
                self._literal_buffer_flush(stack)
                if not isinstance(stack[-1], Or):
                    or_token = Or()
                    root_for_option = Token()
                    root_for_option.childrens = stack[-1].childrens
                    or_token.childrens.append(root_for_option)
                    stack[-1].childrens = [or_token]
                    stack.append(or_token)
                tk = Token()
                tk.parent = or_token
                stack.append(tk)
                or_token.childrens.append(tk)
            # groups
            elif char in '[(':
                self._literal_buffer_flush(stack)
                tk = stack[-1]
                grp=Group()
                grp, ii = self._parse_rule(rule_str[i+1:], root=grp)
                i += ii
                tk.childrens.append(grp)
                if char=='[':
                    grp.optional = True
            # close group
            elif char in ')]':
                if i<len(rule_str)-1 and rule_str[i+1] in '+*':
                    root.repeat=True
                    if char=='*':
                        root.optional = True
                    i+=1
                i+=1
                break
            elif char in '<':
                new_token = None
                self._literal_buffer_flush(stack)
                if char=='<':
                    match = re.match(r'<([^>]+)>', rule_str[i:])
                    token_name = match.group(1)
                    new_token, _=self._parse_rule(self.grammar[token_name])
                    i += match.end() - 1
                if new_token:
                    stack[-1].childrens.append(new_token)
            else:
                self.literal_buffer += char
            i += 1
        # adds what's left in the buffer
        self._literal_buffer_flush(stack)
        return root, i