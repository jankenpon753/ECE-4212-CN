def calcRedundantBits(m):
    """Calculate the number of redundant bits needed."""
    for i in range(m):
        if 2**i >= m + i + 1:
            return i


def posRedundantBits(data, r):
    """Place redundant bits at positions that are powers of two."""
    j = 0
    k = 1
    m = len(data)
    res = ""
    for i in range(1, m + r + 1):
        if i == 2**j:
            res = res + "0"
            j += 1
        else:
            res = res + data[-1 * k]
            k += 1
    return res[::-1]


def calcParityBits(arr, r, show_steps=False):
    """Calculate and set parity bits based on bit positions."""
    n = len(arr)
    if show_steps:
        print("Calculating Parity Bits (Even Parity):")

    for i in range(r):
        val = 0
        checked_positions = []
        for j in range(1, n + 1):
            if j & (2**i) == (2**i):
                val = val ^ int(arr[-1 * j])
                checked_positions.append(f"pos {j} (val {arr[-1 * j]})")
        # Insert the calculated parity bit back into the array
        arr = arr[: n - (2**i)] + str(val) + arr[n - (2**i) + 1 :]

        if show_steps:
            print(f"  P{2**i} checks: {', '.join(checked_positions)}")
            print(f"  => P{2**i} is set to {val}")

    return arr


def detectAndCorrectError(arr, r):
    """Detect error position using parity bits and correct it."""
    n = len(arr)
    res = 0
    print("\n--- RECEIVER SIDE: Error Checking ---")
    print("Recalculating parity bits over received data:")

    for i in range(r):
        val = 0
        for j in range(1, n + 1):
            if j & (2**i) == (2**i):
                val = val ^ int(arr[-1 * j])
        res = res + val * (10**i)
        print(f"  P{2**i} parity check evaluates to: {val}")
    # Convert binary syndrome to decimal
    error_pos = int(str(res), 2)

    if error_pos == 0:
        print("\n[RESULT] Syndrome is 0. No error in the received message.")
        return arr
    else:
        print(
            f"\n[RESULT] Syndrome is {str(res).zfill(r)}. Error detected at position {error_pos} (from the right)."
        )
        # Correct the error
        arr_list = list(arr)
        error_index = n - error_pos
        print(
            f"-> Fixing error... Flipping bit at index {error_index} (which is currently '{arr_list[error_index]}')"
        )

        arr_list[error_index] = "0" if arr_list[error_index] == "1" else "1"
        corrected_arr = "".join(arr_list)
        print(f"-> Corrected Data Codeword: {corrected_arr}")
        return corrected_arr


if __name__ == "__main__":
    data = "1011001"
    m = len(data)
    r = calcRedundantBits(m)

    print("--- SENDER SIDE ---")
    print(f"Original Data: {data}")
    print(f"Data Bits (m): {m}")
    print(f"Redundant Parity Bits required (r): {r}")
    # Place '0' in parity positions (1, 2, 4, 8)
    arr = posRedundantBits(data, r)
    print(f"Data with empty parity bits: {arr}")
    # Calculate actual parity
    arr = calcParityBits(arr, r, show_steps=True)
    print(f"\nTransmitted Codeword: {arr}")
    # Simulate Error
    print("\n>>> Simulating transmission noise...")
    # Let's flip the bit at position 7 from the right (index 4 from left)
    error_arr = arr[:4] + ("0" if arr[4] == "1" else "1") + arr[5:]
    print(f"Original sent: {arr}")
    print(f"Received     : {error_arr}")

    # Detect and correct
    corrected_data = detectAndCorrectError(error_arr, r)
