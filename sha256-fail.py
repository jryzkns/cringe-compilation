import os

def xor(s1,s2):
    return "".join(["1" if dig[0]!=dig[1] else "0" for dig in zip(s1,s2)])

def ror(s,places):
    return s[-1*places:] + s[:-1*places]

def shr(s,places):
    return places*"0" + s[:-1*places]

def b_and(s1,s2):
    return "".join(["1" if (pair[0] == "1" and pair[1] == "1") else "0" for pair in zip(s1,s2)])

def b_not(s):
    return "".join(["0" if bit == "1" else "1" for bit in s])

def add(s1,s2):
    sum = ""
    carry = 0
    for pair in zip(s1[::-1],s2[::-1]):
        current = 0
        if carry == 1:
            current += 1
        if pair[0] == '1' and pair[1] == '1':
            current += 2
        elif pair[0] != pair[1]:
            current += 1

        carry, current = divmod(current, 2)
        sum += str(current)

    return sum[::-1]

def pad_bitpat(bitpat,size=32):
    return "0"*(size-len(bitpat)) + bitpat

msg = ''.join(  [pad_bitpat(bitpat,8) for bitpat in 
                    [str(format(i, 'b')) for i in 
                        "Because I am a fox, that is why!".encode('utf-8')
                    ]
                ])

with open("D.txt","r") as D_f:
    km_digest = D_f.read().split()[1]

with open("E.txt","r") as E_f:
    kmpm_digest = E_f.read().split()[1]

h0 = format(0xf7407834,"b"); h0 = pad_bitpat(h0)
h1 = format(0xb0228749,"b"); h1 = pad_bitpat(h1)
h2 = format(0x978e521d,"b"); h2 = pad_bitpat(h2)
h3 = format(0x3773ce7c,"b"); h3 = pad_bitpat(h3)
h4 = format(0xf5d90e3b,"b"); h4 = pad_bitpat(h4)
h5 = format(0x38cab084,"b"); h5 = pad_bitpat(h5)
h6 = format(0xbd9be08d,"b"); h6 = pad_bitpat(h6)
h7 = format(0x70b5c87a,"b"); h7 = pad_bitpat(h7)

k = [   
        format(0x428a2f98,"b"), format(0x71374491,"b"), format(0xb5c0fbcf,"b"), format(0xe9b5dba5,"b"), 
        format(0x3956c25b,"b"), format(0x59f111f1,"b"), format(0x923f82a4,"b"), format(0xab1c5ed5,"b"),
        format(0xd807aa98,"b"), format(0x12835b01,"b"), format(0x243185be,"b"), format(0x550c7dc3,"b"), 
        format(0x72be5d74,"b"), format(0x80deb1fe,"b"), format(0x9bdc06a7,"b"), format(0xc19bf174,"b"),
        format(0xe49b69c1,"b"), format(0xefbe4786,"b"), format(0x0fc19dc6,"b"), format(0x240ca1cc,"b"), 
        format(0x2de92c6f,"b"), format(0x4a7484aa,"b"), format(0x5cb0a9dc,"b"), format(0x76f988da,"b"),
        format(0x983e5152,"b"), format(0xa831c66d,"b"), format(0xb00327c8,"b"), format(0xbf597fc7,"b"), 
        format(0xc6e00bf3,"b"), format(0xd5a79147,"b"), format(0x06ca6351,"b"), format(0x14292967,"b"),
        format(0x27b70a85,"b"), format(0x2e1b2138,"b"), format(0x4d2c6dfc,"b"), format(0x53380d13,"b"), 
        format(0x650a7354,"b"), format(0x766a0abb,"b"), format(0x81c2c92e,"b"), format(0x92722c85,"b"),
        format(0xa2bfe8a1,"b"), format(0xa81a664b,"b"), format(0xc24b8b70,"b"), format(0xc76c51a3,"b"), 
        format(0xd192e819,"b"), format(0xd6990624,"b"), format(0xf40e3585,"b"), format(0x106aa070,"b"),
        format(0x19a4c116,"b"), format(0x1e376c08,"b"), format(0x2748774c,"b"), format(0x34b0bcb5,"b"), 
        format(0x391c0cb3,"b"), format(0x4ed8aa4a,"b"), format(0x5b9cca4f,"b"), format(0x682e6ff3,"b"),
        format(0x748f82ee,"b"), format(0x78a5636f,"b"), format(0x84c87814,"b"), format(0x8cc70208,"b"), 
        format(0x90befffa,"b"), format(0xa4506ceb,"b"), format(0xbef9a3f7,"b"), format(0xc67178f2,"b")
    ]

k = [pad_bitpat(val) for val in k]

##### PAD
# L + 1 + K + 64 = 0 (mod 512)
# K = 512 - (L+1+64) % 512
msg_l = format(len(msg),"b")
msg = msg + "1" +"0"*(512 - (len(msg)+1+64) % 512) + "0"*(64 - len(msg_l))+msg_l

# msg sched arr
w = [None for i in range(64)]

# populate chunk into msg sched
for i in range(16):
    w[i] = msg[i*32:(i+1)*32]

# populate rest of msg sched
for i in range(16,64):
    s0   = xor(xor(ror(w[i-15], 7), ror(w[i-15],18)),shr(w[i-15], 3))
    s1   = xor(xor(ror(w[i- 2],17), ror(w[i- 2],19)),shr(w[i- 2],10))
    w[i] = add(add(add(w[i-16], s0), w[i-7]), s1)

a = h0
b = h1
c = h2
d = h3
e = h4
f = h5
g = h6
h = h7

# main compresion loop
for i in range(64):
    S1    = xor(xor(ror(e,6),ror(e,11)),ror(e,25))
    ch    = xor(b_and(e,f),b_and(g,b_not(e)))
    temp1 = add(add(add(add(h,S1),ch),k[i]),w[i])
    S0    = xor(xor(ror(a,2),ror(a,13)),ror(a,22))
    maj   = xor(xor(b_and(a,b), b_and(a,c)),b_and(b,c))
    temp2 = add(S0, maj)

    h = g
    g = f
    f = e
    e = add(d,temp1)
    d = c
    c = b
    b = a
    a = add(temp1,temp2)

h0 = add(h0,a)
h1 = add(h1,b)
h2 = add(h2,c)
h3 = add(h3,d)
h4 = add(h4,e)
h5 = add(h5,f)
h6 = add(h6,g)
h7 = add(h7,h)

digest = h0+h1+h2+h3+h4+h5+h6+h7

kmpm_digest = bin(int(kmpm_digest,16))[2:]

# final check
print(digest == pad_bitpat(kmpm_digest,256))