import json
# from pyrsing.sql import parser
import sys

if __name__=="__main__":
    sys.path.insert(0, '/Users/samuelcorradi/Desktop/programas_python/pyrsing/src')
    from pyrsing.sql import parser, get_groups, parse_exp_parts
    sql = "( SELECT * FROM tb55, tb66 )"
    print(json.dumps(get_groups(sql), indent=4))