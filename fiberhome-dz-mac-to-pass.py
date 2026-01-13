import hashlib
import re

UPPER = "ACDFGHJMNPRSTUWXY"
LOWER = "abcdfghjkmpstuwxy"
DIGIT = "2345679"
SYMBOL = "!@$&%"

def mac_to_pass(mac: str) -> str:
    if not re.fullmatch(r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", mac):
        print("\nInvalid MAC format (expected XX:XX:XX:XX:XX:XX)")
        return ""

    md5 = hashlib.md5()
    md5.update(mac.encode())
    md5.update(b"AEJLY")
    digest = md5.hexdigest()  # 32 hex chars

    vals = []
    for c in digest[:20]:
        if '0' <= c <= '9':
            vals.append(ord(c) - ord('0'))
        elif 'a' <= c <= 'f':
            vals.append(ord(c) - ord('a') + 10)
        elif 'A' <= c <= 'F':
            vals.append(ord(c) - ord('A') + 10)
        else:
            vals.append(0)

    password = [''] * 16

    for i in range(16):
        v = vals[i]
        case_type = v % 4
        if case_type == 0:
            password[i] = UPPER[(v * 2) % 17]
        elif case_type == 1:
            password[i] = LOWER[(v * 2 + 1) % 17]
        elif case_type == 2:
            password[i] = DIGIT[6 - (v % 7)]
        elif case_type == 3:
            password[i] = SYMBOL[4 - (v % 5)]

    # --- Step 4: enforce all character classes
    p0 = (vals[16] + 1) % 16
    p1 = (vals[17] + 1) % 16
    while p1 == p0: p1 = (p1 + 1) % 16
    
    p2 = (vals[18] + 1) % 16
    while p2 == p0 or p2 == p1: p2 = (p2 + 1) % 16
    
    p3 = (vals[19] + 1) % 16
    while p3 == p0 or p3 == p1 or p3 == p2: p3 = (p3 + 1) % 16

    password[p0] = UPPER[(vals[16] * 2) % 17]
    password[p1] = LOWER[(vals[17] * 2 + 1) % 17]
    password[p2] = DIGIT[6 - (vals[18] % 7)]
    password[p3] = SYMBOL[4 - (vals[19] % 5)]

    return ''.join(password)

if __name__ == "__main__":
    print("Fiberhome HG6145F1 (Algeria) Web Admin Password Generator")
    print("Firmware Version RP4423 | Username:  admin")
    print("07-01-2026 By Adel/NumberOneDz")
    print("_____________________________________This program is free\n\n")
    mac = date = input("Enter MAC address (XX:XX:XX:XX:XX:XX): ").strip()
    print("\nPassword:           " + mac_to_pass(mac.upper()))
    input("\n\nPress Enter to exit...")