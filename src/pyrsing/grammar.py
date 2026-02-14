import re
from typing import Optional
from pyrsing import ASTNode
from pyrsing.exception import GrammarSyntaxException
from pyrsing.nodes import (
        SequenceNode,
        OrNode,
        TerminalNode,
        AnyNode,
        RepetitionNode
    )

class Grammar:
    """
    """
    def __init__(self, rules:Optional[dict]=None):
        self.rules = rules if rules is not None else {}
        self.root:SequenceNode = SequenceNode('__root__')
        self.literal_buffer = ''
        self.scaped = False
        self._rule_cache = {}
        self._processing = set()

    def _literal_buffer_flush(self, stack:list):
        if self.literal_buffer and stack:
            scaped = False
            parent = stack[-1]
            for char in self.literal_buffer:
                if scaped:
                    scaped = False
                    lit_node = TerminalNode(char)
                    lit_node.parent = parent
                    parent.children.append(lit_node)
                    continue
                elif char == '\\':
                    scaped = True
                    continue
                elif char == '!':
                    if not scaped:
                        raise Exception("Negation can only be indicated at position 0. Use escape '\\!' to include it as literal.")
                    lit_node = TerminalNode(char)
                    lit_node.parent = parent
                    parent.children.append(lit_node)
                elif char == '.':
                    lit_node = AnyNode()
                    parent.children.append(lit_node)
                elif char in '[]()|!<>{}':
                    raise Exception(f"Literal buffer contains special character '{char}'. Use escape '\\{char}' to include it as literal.")
                else:
                    lit_node = TerminalNode(char)
                    lit_node.parent = parent
                    parent.children.append(lit_node)
            self.literal_buffer = ''

    def _find_or_in_stack(self, stack:list):
        """
        Procura o node OrNode na pilha.
        Se encontrar um SequenceNode antes, retorna None.
        Retorna None se não encontrar.
        """
        for tk in reversed(stack):
            if isinstance(tk, OrNode):
                return tk
        return None

    def ast_builder(self)->ASTNode:
        # rest
        self.root = SequenceNode('__root__')
        self.literal_buffer = ''
        self.scaped = False
        self._rule_cache = {}
        self._processing = set()

        rule_str = self.rules.get('__root__', '')
        if not rule_str:
            raise Exception("Root rule '__root__' not found in grammar.")
        seq, _ = self._parse_rule(rule_str, self.root)
        # self.root.children = seq.children
        return self.root

    def _parse_rule(self
        , rule_str:str
        , parent_node:Optional[ASTNode]=None)->tuple[ASTNode,int]:
        i=0
        if parent_node is None:
            parent_node = self.root
        stack = [parent_node]
        while(i<len(rule_str)):
            char = rule_str[i]
            if self.scaped:
                self.scaped = False
                self.literal_buffer += char
            # negation
            elif char=='!' and i==0:
                    stack[-1].is_negation = True
            # repetition
            elif char in ['*', '+']:
                self._literal_buffer_flush(stack)
                parent = stack[-1]
                if not parent.children:
                     # Attempting to repeat nothing or the sequence itself currently being built?
                     # Treating as syntax error or ignoring for now.
                     raise GrammarSyntaxException(f"Repetition '{char}' used without a preceding element.")
                
                target_node = parent.children.pop()
                min_times = 0 if char == '*' else 1
                rep_node = RepetitionNode(target_node, min_times=min_times)
                # rep_node.parent = parent
                parent.children.append(rep_node)
                
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
                if not m:
                    raise GrammarSyntaxException("Error in grammar definition syntax. The character '{' was found, and the expected format is {<number of repetitions>}.")
                parent = stack[-1]
                if not parent.children:
                     raise GrammarSyntaxException(f"Repetition '{{}}' used without a preceding element.")
                target_node = parent.children.pop()
                num_rep_val = int(m[0])
                i += len(m[0])+1
                # {n} means exactly n times, so min=n, max=n
                rep_node = RepetitionNode(target_node, min_times=num_rep_val, max_times=num_rep_val)
                parent.children.append(rep_node)
            # groups
            elif char in '[(':
                self._literal_buffer_flush(stack)
                tk = stack[-1]
                grp=SequenceNode()
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
                mask = r'<[^>]+(\:[^>]+)?>'
                match = re.match(mask, rule_str[i:])
                if not match:
                    raise Exception(f"Syntax error on rule '{rule_str[i:]}' at position {i}.")
                token_name, alias = SequenceNode.parse_rule_name(match.group(0))
                if token_name not in self.rules:
                    raise Exception(f"Production rule '{token_name}' not found in grammar.")
                node_name = None
                # only set the SequenceNode name when an alias is provided.
                if alias is not None:
                    alias_name = alias[1:]
                    # if alias is present but empty ("<rule:>"), use the original token_name as grouping key
                    node_name = token_name if alias_name == '' else alias_name

                # Cache: check if this rule was already built or is being built
                cached_node = self._rule_cache.get(token_name, None)

                if cached_node is not None:
                    # Rule already processed (or being processed right now).
                    # Create a new SequenceNode with the requested alias
                    # and share the children from the canonical cached node.
                    new_token = SequenceNode(node_name)
                    new_token.children = cached_node.children
                else:
                    # First time seeing this rule.
                    # Create a canonical node, register it in the cache
                    # BEFORE processing, so recursive references find it.
                    canonical_node = SequenceNode(token_name)
                    self._rule_cache[token_name] = canonical_node
                    self._processing.add(token_name)
                    self._parse_rule(self.rules[token_name], canonical_node)
                    self._processing.discard(token_name)

                    # Build the node the caller asked for (with alias or not)
                    new_token = SequenceNode(node_name)
                    new_token.children = canonical_node.children

                i += match.end() - 1
                if new_token:
                    stack[-1].children.append(new_token)
            else:
                if char=="\\":
                    self.scaped = True
                self.literal_buffer += char
            i += 1
        # adds what's left in the buffer
        self._literal_buffer_flush(stack)
        return parent_node, i