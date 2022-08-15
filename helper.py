def deep_get(obj: dict = {}, keyspec: str = ''):
    for key in keyspec.split('.'):
        if obj.has(key):
            obj = obj[key]
        else:
            return None
    return obj

def deep_set(obj: dict = {}, keyspec: str = '', field: str = '', entry = None):
    obj = deep_get(obj, keyspec)
    if isinstance(obj, list):
        obj.append(entry)
    elif isinstance(obj, dict):
        obj[field] = entry
    else:
        return False

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

def get_next2(template: dict = {}, obj: dict = {}, current: list = [], new: bool = False):
    # a.b.c3 -> a2 or b2 or c4
    print('get_next', obj.get('label'), current)
    if not current:
        return { 'done': True }
    parent = current
    last = parent.pop()
    if 'list' in obj:
        # get next item OR sibling
        # if list, `last` should be index
        print('yyylist', parent, current, last)
        if new:
            return get_leaf(template, obj, parent + [int(last) + 1])
        else:
            return get_next(template, obj, parent)
    if 'fields' in obj:
        # find the current item index
        idx = find(obj['fields'], 'name', last)
        print('xxfieldx', idx, last)
        if len(obj['fields']) - 1 > idx:
            # not last item
            next_item = obj['fields'][idx + 1]
            next_field = next_item['name']
            return get_leaf(template, next_item, parent + [next_field]) #, parent + [next_field])
        else:
            return get_next(template, obj, parent)

def get_leaf2(template: dict = {}, obj: dict = {}, current: list = []):
    print('get_leaf', obj.get('label'), current)
    if 'list' in obj:
        return [get_leaf(template, obj['list'], current + [0])]
    if 'fields' in obj: # dont care if fields is empty, since its not supposed to
        item = obj['fields'][0]
        return [get_leaf(template, item, current + [item['name']])]
    if 'option' in obj:
        return []
    if obj.get('labelOnly'):
        return [obj, get_leaf(template, obj)]
    # simple
    return [obj]

def get_next(template: dict = {}, obj: dict = {}, current: list = [], terminal: bool = True):
    if 'fields' in obj:
        children = obj['fields']
        child = children[0]
        return get_next(template, child, current + [child['name']], terminal)
    if 'list' in obj:
        return get_next(template, obj['list'], current + [0], terminal)
    if terminal:
        return obj
    else:
        return 

# get_next takes address, return obj
# get next is called on leaf, always go up to parent, pointer to self
# parent will exclude caller, find next child, or go up again
# get_leaf takes obj, return obj

def get_next_field_item(children = [], exclude = []):
    for child in children:
        if child not in exclude:
            return child
    return None

# 'project'
# 'attendees.1.attendee_name'
# 'tags.1'
