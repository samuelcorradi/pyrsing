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
        if self.literal_buffer:
            stack[-1].childrens.append(self.literal_buffer)
            self.literal_buffer = ''

    @staticmethod
    def find_or_in_stack(stack:list)->Or:
        for i, val in enumerate(stack):
            if isinstance(val, Or):
                return val
        return None

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
                or_token = Grammar.find_or_in_stack(stack)
                if not or_token:
                    or_token = Or()
                    root_for_option = Token()
                    root_for_option.childrens = root.childrens
                    or_token.childrens.append(root_for_option)
                    root.childrens = [or_token]
                    stack.append(or_token)
                tk = Token()
                tk.parent = or_token
                stack.append(tk)
                or_token.childrens.append(tk)
            # groups
            elif char in '[(':
                self._literal_buffer_flush(stack)
                grp=Group()
                opt_token, ii = self._parse_rule(rule_str[i+1:], root=grp)
                i += ii
                #tk = stack[-1]
                root.childrens.append(grp)
                if char=='[':
                    opt_token.optional = True
            # close group
            elif char in ')]':
                if i<len(rule_str)-1 and rule_str[i+1] in '+*':
                    root.repeat=True
                    if char=='*':
                        root.optional = True
                    i+=1
                i+=1
                break
                #self._literal_buffer_flush(stack)
                #stack.pop()
            elif char in '<':
                new_token = None
                self._literal_buffer_flush(stack)
                if char=='<':
                    match = re.match(r'<([^>]+)>', rule_str[i:])
                    token_name = match.group(1)
                    # Simplificação: ignorando a sintaxe '!' por enquanto
                    if ':' in token_name: token_name = token_name.split(':')[0]
                    new_token, aa=self._parse_rule(self.grammar[token_name])
                    i += match.end() - 1
                if new_token:
                    stack[-1].childrens.append(new_token)
            else:
                self.literal_buffer += char
            i += 1
        # adiciona o que sobrou no buffer
        self._literal_buffer_flush(stack)
        if len(root.childrens)==1 \
            and (isinstance(root.childrens[0], Group) \
                 or isinstance(root.childrens[0], Or)):
            return root.childrens[0], i
        return root, i