import sys, random
payload, sarcastic_payload= " ".join(sys.argv[1:]).lower(), ""
for ch in payload:
    if random.choice([0, 1]): ch = ch.upper()
    sarcastic_payload += ch
print(sarcastic_payload)
