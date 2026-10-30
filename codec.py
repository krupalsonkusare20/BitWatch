"""Error detection / correction logic: parity, checksum, CRC, Hamming(7,4)."""

GEN = [1, 0, 0, 0, 0, 0, 1, 1, 1]  # x^8 + x^2 + x + 1


def to_bits(n, length):
    return [int(c) for c in format(n, "b").zfill(length)]


def to_num(a):
    x = 0
    for b in a:
        x = x * 2 + b
    return x


def ones(a):
    return sum(a)


def crc_rem(a):
    """Modulo-2 division by GEN, returns the 8-bit remainder."""
    a = list(a)
    for i in range(len(a) - 8):
        if a[i]:
            for j in range(9):
                a[i + j] ^= GEN[j]
    return a[-8:]


def fold(byte_list):
    """One's-complement style sum with end-around carry (8-bit)."""
    s = sum(byte_list)
    while s > 255:
        s = (s & 255) + (s >> 8)
    return s


def to_bytes(a):
    return [to_num(a[i:i + 8]) for i in range(0, len(a) - 7, 8)]


def hamming_encode(d):
    r = 0
    while (1 << r) < len(d) + r + 1:
        r += 1
    n = len(d) + r
    w = [0] * (n + 1)
    k = 0
    for p in range(1, n + 1):
        if p & (p - 1):          # not a power of two -> data position
            w[p] = d[k]
            k += 1
    for i in range(r):
        p = 1 << i
        x = 0
        for q in range(1, n + 1):
            if (q & p) and q != p:
                x ^= w[q]
        w[p] = x
    return w[1:]


def hamming_data(frame):
    return [b for i, b in enumerate(frame) if (i + 1) & i]


def encode(method, d):
    if method == "parity":
        return d + [ones(d) % 2]
    if method == "checksum":
        return d + to_bits(255 - fold(to_bytes(d)), 8)
    if method == "crc":
        return d + crc_rem(d + [0] * 8)
    return hamming_encode(d)


def evaluate(method, data_str, flipped):
    """Return (received_frame, frame, verdict_text, good_bool)."""
    d = [int(c) for c in data_str]
    e = encode(method, d)
    rx = [b ^ 1 if i in flipped else b for i, b in enumerate(e)]
    n = len(flipped)
    if method == "hamming":
        s = 0
        for i, b in enumerate(rx):
            if b:
                s ^= i + 1
        if not s:
            if n:
                return rx, e, "Undetected: the flips formed another valid codeword.", False
            return rx, e, "No errors: syndrome is 0.", True
        f = list(rx)
        if s <= 7:
            f[s - 1] ^= 1
        ok = "".join(map(str, hamming_data(f))) == data_str
        if ok:
            return rx, e, (f"Syndrome {s:03b} = position {s}. "
                           "Flipped it back: data recovered."), True
        return rx, e, (f"Syndrome = position {s}. Flipped it, but the data is "
                       "still wrong (miscorrection)."), False
    if method == "parity":
        passes = ones(rx) % 2 == 0
    elif method == "checksum":
        passes = fold(to_bytes(rx)) == 255
    else:
        passes = not any(crc_rem(rx))
    if not n:
        return rx, e, "No errors injected: the check passes.", True
    if passes:
        return rx, e, "Undetected: the check passes although the data changed.", False
    return rx, e, ("Detected: the receiver rejects the frame. "
                   "It cannot say which bit is wrong."), True
