import cpu

HSJ_SET = "  \n0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~äÄöÖß§┌┐└┘├┤┬┴─│┼╔╗╚╝╠╣╦╩═║╬░▒▓█▀▄▌▐━┃┯┷┠┨┿╀╁╂╃╄╅╆╇╈╉╊╋←↑→↓↔↕¦™©®±²³⁰⁴⁵⁶⁷⁸⁹⁺⁻₀₁₂₃₄₅₆₇₈₉                                                                        "

def encode_hsj(text):
    return [HSJ_SET.index(c, 1 if c == " " else 0) for c in text]

cpu = cpu.CPU([0] * 65536, 0x0000)
reserved_start = len(cpu.mem) - cpu.RESERVED
out_start = reserved_start - 256

# ---- INPUT: Change this value only! ----
cpu.mem[0x0100] = encode_hsj("0")[0]  # Set to encode_hsj("0")[0] for 0, encode_hsj("1")[0] for 1
# ----------------------------------------

# Clear output buffer
cpu.mem[out_start:out_start+256] = [0] * 256
print(out_start)
program = [
    0xAD, 0x00, 0x01,                # LDA $0100
    0xC9, encode_hsj("1")[0],        # CMP #HSJ('1')
    0xD0, 0x0A,                      # BNE +10 (to print_zero)
    # print_one:
    0xA9, encode_hsj("1")[0],        # LDA #HSJ('1')
    0x8D, out_start & 0xFF, out_start >> 8,  # STA out_start
    0xA9, encode_hsj("\n")[0],       # LDA #HSJ('\n')
    0x8D, (out_start+1) & 0xFF, (out_start+1) >> 8,  # STA out_start+1
    0xA9, 0x00,                      # LDA #0
    0x8D, (out_start+2) & 0xFF, (out_start+2) >> 8,  # STA out_start+2
    0x20,                            # OUT
    0x4C, 0x09, 0x00,                # JMP print_one (to OUT)
    # print_zero:
    0xA9, encode_hsj("0")[0],        # LDA #HSJ('0')
    0x8D, out_start & 0xFF, out_start >> 8,        # STA out_start
    0xA9, encode_hsj("\n")[0],       # LDA #HSJ('\n')
    0x8D, (out_start+1) & 0xFF, (out_start+1) >> 8,  # STA out_start+1
    0xA9, 0x00,                      # LDA #0
    0x8D, (out_start+2) & 0xFF, (out_start+2) >> 8,  # STA out_start+2
    0x20,                            # OUT
    0xFF                             # HALT
]
cpu.mem[0x0000:0x0000+len(program)] = program

cpu.run_until_halt()