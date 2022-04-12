import json
from pyrsing.sql import parser
import sys

if __name__=="__main__":
    sql = """
    SELECT [my_field]
    FROM (my_table)
    WHERE 1=2;

    SELECT 4 FROM another_table
    """
    print(json.dumps(parser(sql), indent=4))