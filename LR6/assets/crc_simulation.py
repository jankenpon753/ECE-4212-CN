def findXor(a, b):
    """Performs bitwise XOR between two binary strings (a and b)."""
    result = []
    for i in range(1, len(b)):  # Skip first bit (CRC standard)
        if a[i] == b[i]:
            result.append("0")
        else:
            result.append("1")
    return "".join(result)


def mod2div(dividend, divisor, show_steps=False):
    """Performs Modulo-2 division (CRC division algorithm) with step tracking."""
    pick = len(divisor)
    tmp = dividend[0:pick]

    if show_steps:
        print(f"    [DIV] Initial Dividend: {dividend}")
        print(f"    [DIV] Divisor:          {divisor}")

    while pick < len(dividend):
        if tmp[0] == "1":
            if show_steps:
                print(f"    [DIV] {tmp} XOR {divisor} -> ", end="")
            tmp = findXor(divisor, tmp) + dividend[pick]
            if show_steps:
                print(f"{tmp} (pulled down {dividend[pick]})")
        else:
            if show_steps:
                print(f"    [DIV] {tmp} XOR {'0'*pick} -> ", end="")
            tmp = findXor("0" * pick, tmp) + dividend[pick]
            if show_steps:
                print(f"{tmp} (pulled down {dividend[pick]})")
        pick += 1
    # Final step
    if tmp[0] == "1":
        if show_steps:
            print(f"    [DIV] Final Step: {tmp} XOR {divisor} -> ", end="")
        tmp = findXor(divisor, tmp)
    else:
        if show_steps:
            print(f"    [DIV] Final Step: {tmp} XOR {'0'*pick} -> ", end="")
        tmp = findXor("0" * pick, tmp)

    if show_steps:
        print(f"{tmp}\n")
    return tmp


def encodeData(data, key):
    """Appends CRC remainder to the original data."""
    l_key = len(key)
    appended_data = data + "0" * (l_key - 1)
    print(f"--- SENDER SIDE ---")
    print(f"Original Data: {data}")
    print(f"Key (Polynomial): {key}")
    print(f"Appended Data (with {l_key - 1} zeros): {appended_data}\n")

    print("Calculating Remainder:")
    remainder = mod2div(appended_data, key, show_steps=True)

    codeword = data + remainder
    print(f"Calculated Remainder: {remainder}")
    print(f"Transmitted Codeword: {codeword}\n")
    return codeword


def receiver(data, key):
    """Checks if received data has errors (remainder == 0)."""
    print(f"--- RECEIVER SIDE ---")
    print(f"Received Codeword: {data}\n")

    print("Performing Modulo-2 Division on Received Data:")
    remainder = mod2div(data, key, show_steps=True)

    print(f"Final Remainder: {remainder}")
    if "1" in remainder:
        print(
            "[RESULT] ERROR DETECTED: The remainder is non-zero. The data was corrupted during transmission.\n"
        )
    else:
        print("[RESULT] SUCCESS: The remainder is zero. No errors detected.\n")


if __name__ == "__main__":
    data = "100100"
    key = "1101"
    # 1. Sender Encodes
    codeword = encodeData(data, key)
    # 2. Receiver Receives Valid Data
    print(">>> SCENARIO 1: Transmission without errors")
    receiver(codeword, key)
    # 3. Receiver Receives Corrupted Data
    print(">>> SCENARIO 2: Transmission WITH errors (Fault Simulation)")
    # Flip the 3rd bit from '0' to '1'
    error_codeword = codeword[:2] + "1" + codeword[3:]
    print(f"(Simulating noise... flipping a bit: {codeword} -> {error_codeword})")
    receiver(error_codeword, key)
