def print_dict(d: dict, indent = ''):
    for key, value in d.items():
        if type(value) == dict:
            print('{}{}:'.format(indent, key))
            print_dict(value, indent+'  ')
        else:
            print('{}{}: {}'.format(indent, key, value))
