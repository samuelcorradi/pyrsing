import re

def remove_comments(sql:str):
    regex = r"""(?xs) # x = enable inline comments, s = enable DOT-ALL
    (?:--[^\r\n]*)      # comments
    |                 # or
    (?:\s*)             # brealines
    |                 # or
    ([^\r\n]*)      # 3 comandos
    """
    # regex = r"(--[^\r\n]*)|('(?:''|[^\r\n'])*')|(\b(?:SELECT|UPDATE|DELETE|INSERT)\b)|([A-Z][A-Z_]*)|."
    commands = []
    m = re.findall(regex, sql)
    for inst in m:
        if inst:
            commands.append(inst)
    return ' '.join(commands)

def split_commands(sql:str):
    splitted = re.split('\;', sql)
    return splitted

def parse_command(sql:str):
    commands = remove_comments(sql)
    #print("Imprimindo comandos:\n---------------------")
    #print(commands)
    regex = r"""(?:(SELECT)\s+(\*|.*)[\s]*
            (?:FROM[\s]+\(*([^\)]+)\)*)?\s*
            (?:[\s\)]*WHERE\s+(.*))?)
            """
    regex = r"^(?:(SELECT) (.*?)\s*(?:FROM +(.*?))?\s*(?: WHERE +(.*?))?)(?:\;.*)?$"
    match = re.findall(regex, commands) #, re.VERBOSE)
    #print("Match de SELECT:\n------------------")
    #print(match)
    cmds = []
    for m in match:
        obj = {}
        # source_cmds = parse_command(m[2])
        if m[0]=='SELECT':
            obj['type']='select'
            obj['expression']=parse_exp(m[1])
            obj['source']=parse_exp(m[2]) #m[2] if not source_cmds else source_cmds
            obj['filter']=parse_exp(m[3]) if m[3] else None
        cmds.append({'command':obj})
    return cmds

def get_groups(sql:str):
    open_char = ['(', '"', '\'']
    clos_char = [')', '"', '\'']
    groups = []
    open_pos = -1
    opened = 0
    ochar=''
    cchar=''
    parsed = ''
    group_id = ''
    for i, c in enumerate(sql):
        prev_not_scape = (i and sql[i-1]!="\\") or not i
        if not opened and prev_not_scape and c in open_char:
            # print("Encontrou a aberttura em {} na posicao {}.".format(c, i))
            #if not group_id:
            open_pos = i
            ochar = c
            cchar = clos_char[open_char.index(c)]
            #print("Definidor a abertura como {} e o fechamento como {}.".format(ochar, cchar))
            group_id = "--GROUP{}--".format(len(groups))
            #print("Abre o grupo de id {}.".format(group_id))
            parsed += group_id
            opened+=1
        elif opened and c==ochar and ochar!=cchar:
            #print("Eleva do nivel {} para o nivel {}.".format(opened, opened+1))
            opened+=1
        elif opened and c==cchar and prev_not_scape:
            #print("Reduz o nivel {} para o nivel {}.".format(opened, opened-1))
            opened-=1
            if not opened:
                #print("Fechamento de grupo {}".format(group_id))
                groups.append({'group_id':group_id, 'group':sql[open_pos:i+1], 'open_pos':open_pos, 'close_pos':i+1})
                open_pos = -1
                ochar=''
                cchar=''
                group_id = ''
            continue
        if not opened:
            parsed += c
    #print(parsed)
    # if opened>0: raise Exception("\nGrupo aberto com character '{}' na posição {} mas não foi fechado no comando '{}'".format(ochar, open_pos, sql))
    return {'groups':groups, 'parsed':parsed}

def parse_exp_parts(exp:str):
    #print("\nAnalise de grupos.\n-----------------")
    groups = get_groups(exp)
    #print(groups)
    exp2 = groups['parsed'] if groups else exp
    #print(exp2)
    parts = exp2.split(',')
    if groups:
        for g in groups['groups']:
            for i, p in enumerate(parts):
                parts[i] = p.replace(g['group_id'], g['group'])
    return parts

def split_exp_from_part(part:str):
    reg = r"((SELECT )|(\*)|(\[[^\]]+\])|(\'[^\']*\')|([a-zA-Z0-9]+\(.*\))|\((.*)\)|([\=\+\-])|([^\s\=\+\-]*))(?:\s+)?"
    match = re.findall(reg, part.strip())
    return match

def parse_exp(exp:str):
    exp = exp.strip()
    cmd = parse_command(exp)
    if cmd:
        #print("Achou um comando na expressao.")
        #print(cmd)
        return cmd
    exp_grp = []
    parts = parse_exp_parts(exp)
    #print("\nParser das partes de uma expressao:\n-----------------------------------")
    #print(parts)
    for part in parts:
        exp_elemts = []
        match = split_exp_from_part(part.strip())
        if match:
            for m in match:
                #print(m)
                if m[1]:
                    return parse_command(part)
                elif m[2]:
                    exp_elemts.append({'field':m[2]})
                elif m[3]:
                    exp_elemts.append({'field':m[3]})
                elif m[4]:
                    exp_elemts.append({'string':m[4]})
                elif m[5]:
                    exp_elemts.append({'function':m[5]})
                elif m[6]:
                    #print("Conteúdo encontrado de um grupo que vai passar por parse_exp()")
                    #print(m[6])
                    exp_elemts.append({'expression':parse_exp(m[6])})
                elif m[7]:
                    exp_elemts.append({'operator':m[7]})
                elif m[8]:
                    exp_elemts.append({'constant':m[8]})
        exp_grp.append(exp_elemts)
    return exp_grp

def parser(sql:str):
    commands = split_commands(sql)
    r = []
    for sql in commands:
        #print(sql)
        r.append(parse_exp(sql))
    return r
   
