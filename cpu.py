class CPU:
    MODDED = False
    IDXNME = "Jade v1.2"
    def __init__(self, mem, start_pos):
        self.STACK_LENGTH = 255
        self.RESERVED = 8 + self.STACK_LENGTH # 2 (start vector) + 1 (stack ptr) + 1 (A) + 1 (X) + 1 (Y) + 2 (PC)
        if len(mem) < 65536 - self.RESERVED:
            raise ValueError("Memory must be at least 65528 bytes")
        if len(mem) > 65536 - self.RESERVED:
            mem = mem[:65536 - self.RESERVED]
        mem += [0] * self.RESERVED
        self.mem = mem
        # Set start vector and PC in reserved area
        self._set_word(65536 - self.RESERVED, start_pos) # start vector
        self._set_word(65536 - 2, start_pos) # PC

        self.halted = False

    def _get_word(self, addr):
        return self.mem[addr] | (self.mem[addr + 1] << 8)

    def _set_word(self, addr, value):
        self.mem[addr] = value & 0xFF
        self.mem[addr + 1] = (value >> 8) & 0xFF

    def _set_a(self, value):
        self.mem[65536 - 5] = value & 0xFF
    def _get_a(self):
        return self.mem[65536 - 5]
    
    def _set_x(self, value):
        self.mem[65536 - 4] = value & 0xFF
    def _get_x(self):
        return self.mem[65536 - 4]
    
    def _set_y(self, value):
        self.mem[65536 - 3] = value & 0xFF
    def _get_y(self):
        return self.mem[65536 - 3]

    def clock(self):
        pc_addr = 65536 - 2
        pc = self._get_word(pc_addr)
        opcode = self.mem[pc]

        if pc >= 65536 - self.RESERVED:
            if not self.halted:
                print(f"SEGFAULT")
                print(f"PC: {pc:04X} - Code overrun, reached stack content")
                print("This shouldnt happen.")
                self.halted = True
            return
        if opcode == 0x00: # NOP
            pc += 1

        elif opcode == 0xA9: # LDA immediate
            value = self.mem[pc + 1]
            self._set_a(value)
            pc += 2

        elif opcode == 0xA2: # LDX immediate
            value = self.mem[pc + 1]
            self._set_x(value)
            pc += 2

        elif opcode == 0xA0: # LDY immediate
            value = self.mem[pc + 1]
            self._set_y(value)
            pc += 2

        elif opcode == 0x8D: # STA absolute
            addr = self.mem[pc + 1] | (self.mem[pc + 2] << 8)
            self.mem[addr] = self._get_a()
            pc += 3

        elif opcode == 0x8E: # STX absolute
            addr = self.mem[pc + 1] | (self.mem[pc + 2] << 8)
            self.mem[addr] = self._get_x()
            pc += 3

        elif opcode == 0x8C: # STY absolute
            addr = self.mem[pc + 1] | (self.mem[pc + 2] << 8)
            self.mem[addr] = self._get_y()
            pc += 3

        elif opcode == 0x4C: # JMP absolute
            addr = self.mem[pc + 1] | (self.mem[pc + 2] << 8)
            pc = addr

        elif opcode == 0x20: # OUT
            # prints the content of the last 256 (or terminated by 00) bytes of memory before reserved area to the console as HSJ characters
            # because HSJ doesnt have mosto f the control characters, it has more useufl characters than ASCII that all fit in 256 values!
            HSJ_SET = "  \n0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~äÄöÖß§┌┐└┘├┤┬┴─│┼╔╗╚╝╠╣╦╩═║╬░▒▓█▀▄▌▐━┃┯┷┠┨┿╀╁╂╃╄╅╆╇╈╉╊╋←↑→↓↔↕¦™©®±²³⁰⁴⁵⁶⁷⁸⁹⁺⁻₀₁₂₃₄₅₆₇₈₉                                                                        " # the first element here doesnt matter because you cant print it (its a NUL)
            start = 65536 - self.RESERVED - 256
            end = 65536 - self.RESERVED

            output = []
            for i in range(start, end):
                if self.mem[i] == 0:
                    break
                output.append(HSJ_SET[self.mem[i]])
            print(''.join(output))
            pc += 1
        elif opcode == 0xFF: # stop
            if self.halted == False: print("bai!!!"); self.halted = True
            # Dont increment pc, so if clock is called again, it wont do anything else and maybe overrun, instead just tays at the end
            return
        
        elif opcode == 0x69:  # ADC immediate (Add with Carry, but here just ADD)
            value = self.mem[pc + 1]
            result = (self._get_a() + value) & 0xFF
            self._set_a(result)
            pc += 2

        elif opcode == 0xE9:  # SBC immediate (Subtract with Carry, but here just SUB)
            value = self.mem[pc + 1]
            result = (self._get_a() - value) & 0xFF
            self._set_a(result)
            pc += 2

        elif opcode == 0x20:  # OUT (already present)
            # ...existing OUT code...
            pc += 1

        elif opcode == 0x22:  # JSR absolute (choose an unused opcode, e.g. 0x22)
            addr = self.mem[pc + 1] | (self.mem[pc + 2] << 8)
            # Push return address (pc+3) to stack
            sp_addr = 65536 - 6
            sp = self.mem[sp_addr]
            ret_addr = (pc + 3) & 0xFFFF
            self.mem[0x0100 + sp] = ret_addr & 0xFF
            self.mem[0x0100 + ((sp - 1) & 0xFF)] = (ret_addr >> 8) & 0xFF
            self.mem[sp_addr] = (sp - 2) & 0xFF
            pc = addr

        elif opcode == 0x60:  # RTS (ReTurn from Subroutine)
            sp_addr = 65536 - 6
            sp = (self.mem[sp_addr] + 2) & 0xFF
            ret_lo = self.mem[0x0100 + sp]
            ret_hi = self.mem[0x0100 + ((sp - 1) & 0xFF)]
            self.mem[sp_addr] = sp
            pc = ret_lo | (ret_hi << 8)

        else:
            # Unknown opcode: skip
            pc = (pc + 1) & 0xFFFF

        self._set_word(pc_addr, pc)

    def run_until_halt(self):
        while not self.halted:
            self.clock()





# Test
# Example test for writing and printing "Hello, world!" using STA
mem = [0] * (65536 - (8 + 255)) # user memory, not including reserved
HSJ_SET = "  \n0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~äÄöÖß§┌┐└┘├┤┬┴─│┼╔╗╚╝╠╣╦╩═║╬░▒▓█▀▄▌▐━┃┯┷┠┨┿╀╁╂╃╄╅╆╇╈╉╊╋←↑→↓↔↕¦™©®±²³⁰⁴⁵⁶⁷⁸⁹⁺⁻₀₁₂₃₄₅₆₇₈₉                                                                        "
def hord(c):
    return HSJ_SET.index(c) if c != " " else 1
output_str = "Jade says 'Hello, world!'"
output_bytes = [hord(c) for c in output_str] + [0] # NUL-terminated
program_start = 0x0200
outbuf_start = 65536 - (8 + 255) - 256
# Assemble the program
pc = program_start
for i, b in enumerate(output_bytes):
    # LDA #imm
    mem[pc] = 0xA9
    mem[pc + 1] = b
    pc += 2
    # STA abs
    addr = outbuf_start + i
    mem[pc] = 0x8D
    mem[pc + 1] = addr & 0xFF
    mem[pc + 2] = (addr >> 8) & 0xFF
    pc += 3
# OUT
mem[pc] = 0x20
pc += 1
# stop
mem[pc] = 0xFF
# Create CPU and run the program
cpu = CPU(mem, program_start)
# run
cpu.run_until_halt()