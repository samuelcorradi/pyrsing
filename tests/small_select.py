import json
# from pyrsing.sql import parser
import sys

if __name__=="__main__":
    sys.path.insert(0, '/Users/samuelcorradi/Desktop/programas_python/pyrsing/src')
    from pyrsing.sql import parser, get_groups, parse_exp_parts
    sql = """
    SELECT [ass]
    FROM (table)
    WHERE 1=2;

    SELECT 4 FROM lala
    """
    print(json.dumps(parser(sql), indent=4))