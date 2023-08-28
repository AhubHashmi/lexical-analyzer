# for_loop_library.py

def simple_for_loop(start, end, step=1):
    result = []
    for i in range(start, end, step):
        result.append(i)
    return result

def nested_for_loop(rows, cols):
    result = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append((i, j))
        result.append(row)
    return result
