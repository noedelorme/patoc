grid_size = 200
grid_offset = 20


def pos(i): return i*grid_offset

def invpos(i): return round(i/grid_offset)

def roundpos(x): return pos(invpos(x))

def type_parse(type: str):
    if type[0] == "[":
        nb_controls = int(type.split("]")[0][1:])
        target_type = type.split("]")[1]
        return nb_controls, target_type
    else:
        return 0,type