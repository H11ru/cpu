import cpu

cpu = cpu.CPU([0] * 65536, 0x0000)

# Assemble program at address 0x0000
program = [
    0xA9, 0x42,        # LDA #$42
    0x20,
    0x8D, 0x34, 0x12,  # STA $1234
    0xFF
]
cpu.mem[0x0000:0x0000+len(program)] = program

cpu.run_until_halt()

print(f"Value at $1234: {cpu.mem[0x1234]:02X}")