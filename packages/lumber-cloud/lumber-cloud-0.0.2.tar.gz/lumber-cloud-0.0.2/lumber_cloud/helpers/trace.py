from traceback import extract_stack

def trace():
    t = extract_stack(limit=4)
    return {
        'line': t[0][1],
        'method': t[0][2]
    }
