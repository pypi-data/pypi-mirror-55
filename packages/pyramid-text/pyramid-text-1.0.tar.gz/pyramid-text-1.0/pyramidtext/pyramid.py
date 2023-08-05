def generate(text):
    aout = []
    out = ""
    rout = []
    for i in range(len(text)):
        out += text[i]
        aout.append(out)
    for i in range(len(aout)-1, -1, -1):
        rout.append(aout[i])
    aout = aout[:-1]
    result = '\n'.join(aout)+'\n'+'\n'.join(rout)
    return(result)