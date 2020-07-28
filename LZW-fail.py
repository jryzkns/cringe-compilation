def LZW_enc(msg, 
            d = {"A":0, "B":1, "C":2, "D":3, "E":4}):
    out, next_code_id, s = [], len(d), msg[0]
    for ch in msg[1:]:
        c = ch
        if s + c in d:
            s = s + c
        else:
            out += [d[s]]
            d[s+c], s = next_code_id, c
            next_code_id += 1
    out += [d[s]]
    return " ".join([str(val) for val in out]), d