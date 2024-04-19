grid_size = 200
grid_offset = 20


def pos(i): return i*grid_offset

def invpos(i): return round(i/grid_offset)

def roundpos(x): return pos(invpos(x))