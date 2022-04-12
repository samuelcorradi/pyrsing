import json
from pyrsing.sql import get_groups
import sys

if __name__=="__main__":
    sql = "( SELECT * FROM table1, other_table )"
    print(json.dumps(get_groups(sql), indent=4))