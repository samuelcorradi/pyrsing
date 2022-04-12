import json
from pyrsing.sql import parser
import sys 

if __name__=="__main__":
    sql = """
    -- teste
    -- Some comment.

    SELECT  [field] + MYFUNCTION('parameter') , [field2], [field3], 'Some, (Wor)d with Parenteses', lost_item (2 (32),65), another item, 87778.87 + 323,,,
    FROM ((

        SELECT * FROM tb55, tb66

    )) WHERE [meucampo] = (SELECT [outro_campo] FROM anothertable);

    SELECT 2 
    -- Commented command SELECT 2 

    --- Another comment
    """
    parsed = parser(sql)
    pretty = json.dumps(parsed, indent=4)
    print(pretty)
