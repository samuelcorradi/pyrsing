registry = {}

def on(rule_name: str, func=None):
    if func is None:
        def decorator(f):
            registry[rule_name] = f
            return f
        return decorator
    registry[rule_name] = func
    return func

@on('regra')
def regra_transformer(param:list):
    result=[]
    for item in param:
        if isinstance(item, dict) and 'paragraph' in item:
            r = []
            for i in item['paragraph']:
                if isinstance(i, dict):
                    if 'bold' in i:
                        r.append('BOLD')
                        continue
                else: # isinstance(i, str):
                    r.append(i)
                    continue
            item = {'paragraph': r}
        elif isinstance(item, str):
            item = item.replace('\n', '<br />')
        result.append(item)
    return result

