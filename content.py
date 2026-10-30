"""Lesson content for BitWatch."""

M = {
    "parity": dict(
        title="Parity", length=8, default="10110010",
        one="One extra bit that makes the count of 1s even.",
        read=[
            ("", "Bits travel as voltages, light pulses or radio waves, and noise can flip one. "
                 "The receiver cannot see the sender's data, so the sender adds a little redundancy: "
                 "extra information that the data must agree with.\n\n"
                 "With even parity, the sender counts the 1s in the data and adds one more bit so the "
                 "total number of 1s is even. The receiver counts again. An odd total means at least "
                 "one bit changed. Odd parity is the mirror image."),
            ("Worked example", "Data 10110010 has four 1s, which is already even, so the parity bit is 0 "
                               "and the frame is 101100100. Flip one bit and the receiver counts an odd "
                               "number of 1s: error detected. Flip two bits and the count is even again: "
                               "the error slips through."),
            ("Strengths and limits", "Very cheap (one bit) and fast. It detects every odd-sized error but "
                                     "misses every even-sized one, it cannot say where the error is, and "
                                     "it cannot fix it."),
        ],
        real=["Serial links (UART) can add a parity bit to each byte.",
              "RAID 5 stores XOR parity across disks so a lost disk can be rebuilt.",
              "Older computer memory used a parity bit per byte to spot damaged RAM."],
        notes=["extra bit -> total 1s EVEN (even parity)", "10110010 -> four 1s -> bit = 0",
               "send 101100100", "receiver counts: odd = ERROR", "1 flip -> caught",
               "2 flips -> cancel! missed", "detects only, never corrects"],
        quiz=("Data 1110 (three 1s), even parity. The parity bit is...", ["0", "1"], 1,
              "Three 1s is odd, so add a 1 to make four."),
        videos=[("Parity Check and Parity Bits (Error Detection)", "jLuj62Gq-1I"),
                ("Error Detecting Code: Parity Explained", "Bwih7_AT1oI"),
                ("Parity Bits and Error Detection Explained", "KvTc43Jt76w")]),
    "checksum": dict(
        title="Checksum", length=16, default="0101100111110000",
        one="Add the bytes, fold the carry, flip the bits.",
        read=[
            ("", "A checksum treats the data as numbers. The sender splits it into bytes, adds them, and "
                 "sends the (complemented) total along with the data. The receiver adds everything again, "
                 "including the checksum, and expects a fixed result."),
            ("Worked example (8-bit)", "Bytes 0x59 and 0xF0 add to 0x149, which is 9 bits. The extra carry is "
                                       "added back in (end-around carry): 0x49 + 1 = 0x4A. Flip every bit "
                                       "(the complement): 0xB5 is the checksum.\n\n"
                                       "Receiver: 0x59 + 0xF0 + 0xB5 with end-around carry equals 0xFF "
                                       "(all 1s) when nothing changed."),
            ("Strengths and limits", "Compact, and catches many byte changes. But swapping two bytes, or one "
                                     "error plus a compensating error, gives the same sum: a collision. "
                                     "It detects only."),
        ],
        real=["IPv4 headers, TCP and UDP use a 16-bit one's-complement checksum.",
              "ISBN and barcode check digits are checksums in spirit.",
              "Download pages often list a checksum so you can verify a file."],
        notes=["split into bytes, ADD them", "carry out? add it back (end-around)",
               "0x59 + 0xF0 = 0x149 -> 0x4A", "flip all bits -> 0xB5",
               "receiver: total must be 0xFF", "collisions possible", "detects only"],
        quiz=("A checksum sum overflows 8 bits. The carry is...", ["Dropped", "Added back in"], 1,
              "That is the end-around carry."),
        videos=[("Checksum Error Detection method with example (one's complement)", "S4dmIdhKAJ4"),
                ("Checksum in Computer Networks", "CxjrrWt9CLU"),
                ("Checksum for Error Detection (Lecture 52)", "WTP06IWWgGA")]),
    "crc": dict(
        title="CRC", length=8, default="10110010",
        one="Divide the bits like a polynomial and send the remainder.",
        read=[
            ("", "A cyclic redundancy check treats the data as one huge binary number and divides it by an "
                 "agreed generator. The division uses XOR instead of subtraction (modulo-2), so there are "
                 "no borrows. The sender transmits the data plus the remainder. The receiver divides the "
                 "whole frame: remainder zero means it looks intact."),
            ("Worked example", "Generator 100000111 (x^8 + x^2 + x + 1). Payload 1101.\n"
                               "1) Append eight zeros: 110100000000.\n"
                               "2) Divide with XOR: remainder 00100011.\n"
                               "3) Send 110100100011.\n"
                               "4) Receiver divides again and expects remainder 0."),
            ("Strengths and limits", "Excellent at catching burst errors (several adjacent bad bits) and many "
                                     "common patterns, and easy in hardware. It still cannot tell which bit "
                                     "is wrong, so networks respond by asking for a resend."),
        ],
        real=["Ethernet frames end with a CRC-32 frame check sequence.",
              "ZIP and PNG files store CRC-32 values to detect corruption.",
              "Storage and USB links use CRCs to catch burst errors."],
        notes=["generator: 100000111", "1) append 8 zeros", "2) divide with XOR (mod-2)",
               "3) send data + REMAINDER", "1101 -> 110100100011", "receiver remainder = 0",
               "great for bursts, no fixing"],
        quiz=("CRC division uses...", ["XOR instead of subtraction", "Ordinary subtraction"], 0,
              "Modulo-2 arithmetic has no borrows, which is just XOR."),
        videos=[("Cyclic Redundancy Check (CRC), Part 1", "A9g6rTMblz4"),
                ("Cyclic Redundancy Check (CRC) example", "ZJH0KT6c0B0"),
                ("Error Detection and Correction 2: Cyclic Redundancy Check", "6gbkoFciryA")]),
    "hamming": dict(
        title="7-bit Hamming code", length=4, default="1011",
        one="Overlapping parity bits that point at the bad bit.",
        read=[
            ("", "Hamming(7,4) packs 4 data bits into 7 positions. Parity bits sit at positions 1, 2 and 4 "
                 "(powers of two); data bits fill positions 3, 5, 6 and 7. Each parity bit watches a "
                 "different overlapping group.\n\n"
                 "P1 checks positions 1,3,5,7. P2 checks 2,3,6,7. P4 checks 4,5,6,7. Each is set so its "
                 "group has an even number of 1s."),
            ("Worked example", "Data 1011 goes to D1..D4. P1 = 0, P2 = 1, P4 = 0, so the codeword is 0110011.\n\n"
                               "Suppose position 5 flips. P1's group and P4's group now fail, P2's passes. "
                               "Read the failures as binary (P4 P2 P1 = 101): that is 5, the syndrome. "
                               "Flip position 5 back and the data is recovered."),
            ("Strengths and limits", "Corrects any single-bit error. With two flips it can 'fix' the wrong "
                                     "bit and return bad data silently. SECDED (one extra overall parity "
                                     "bit) adds double-error detection."),
        ],
        real=["ECC memory in servers uses Hamming-style SECDED codes.",
              "Spacecraft and satellites protect stored data against radiation bit flips.",
              "Flash and SSD controllers use stronger relatives of Hamming codes."],
        notes=["P1 P2 D1 P4 D2 D3 D4", "parity at 1, 2, 4", "P1:1,3,5,7  P2:2,3,6,7  P4:4,5,6,7",
               "1011 -> 0110011", "failed checks -> binary -> position",
               "syndrome 101 = bit 5 -> flip it", "fixes 1 error (2 can fool it)"],
        quiz=("Syndrome 110 (binary) means which position is wrong?", ["3", "6"], 1,
              "110 in binary is 6."),
        videos=[("But what are Hamming codes? (3Blue1Brown)", "X8jsijhllIA"),
                ("How Hamming Code Corrects the Error: (7,4) encode and decode", "t4kiy4Dsx5Y"),
                ("7 Bit Hamming Code example", "dhfhM_4aO8U"),
                ("Syndrome decoding of (7,4) Hamming code", "CmvF2Rc1xvo")]),
}
KEYS = list(M)
HL = ["P1", "P2", "D1", "P4", "D2", "D3", "D4"]

NOTE_LINKS = [
    ("Stanford EE179 lecture notes: parity, CRC, Hamming (7,4)", "https://web.stanford.edu/class/ee179/lectures/notes18.pdf"),
    ("NPTEL (IIT Kharagpur) notes: parity, checksum, Hamming", "https://archive.nptel.ac.in/content/storage2/courses/106105080/pdf/M3L2.pdf"),
    ("WPI slides: parity, internet checksum, CRC, Hamming", "https://web.cs.wpi.edu/~rek/Nets2/C13/Transmission_Errors_C13.pdf"),
    ("GeeksforGeeks: checksum with worked example", "https://www.geeksforgeeks.org/computer-networks/error-detection-code-checksum/"),
    ("GeeksforGeeks: CRC and modulo-2 division", "https://www.geeksforgeeks.org/dsa/modulo-2-binary-division/"),
    ("Scribd: Error Detection and Correction (Hamming, CRC, checksum)", "https://www.scribd.com/document/636690342/Error-Detection-and-Correction-Hamming-Code-CRC-Checksum-1"),
]
HAND_LINKS = [
    ("Search Google for handwritten notes", "https://www.google.com/search?q=handwritten+notes+error+detection+and+correction+parity+checksum+crc+hamming+code"),
    ("Search Scribd for handwritten notes", "https://www.scribd.com/search?query=handwritten%20notes%20error%20detection%20and%20correction"),
]

COLORS = {"parity": "#2f5fb8", "checksum": "#b5607f", "crc": "#3f8f86", "hamming": "#c4783f"}
