import sys
import re

OPCODES = {
    "LIA": 0xA9,   # LDA immediate
    "STA": 0x8D,   # STA absolute
    "OUT": 0x20,   # OUT
    "HLT": 0xFF,   # HALT
    "CAL": 0x22,   # JSR absolute (subroutine call)
    # Add more as needed
}

def parse_operand(operand):
    operand = operand.strip()
    if operand.startswith("0x"):
        return int(operand, 16)
    elif operand.isdigit():
        return int(operand)
    else:
        return operand  # Possibly a label

def assemble(lines):
    labels = {}
    output = []
    pc = 0
    # First pass: find labels
    for line in lines:
        line = line.split(";")[0].strip()
        if not line:
            continue
        if line.endswith(":"):
            labels[line[:-1]] = pc
        else:
            pc += 3 if any(inst in line for inst in ["STA", "CAL"]) else 2 if "LIA" in line else 1

    # Second pass: assemble
    pc = 0
    for line in lines:
        line = line.split(";")[0].strip()
        if not line or line.endswith(":"):
            continue
        parts = re.split(r"\s+", line, maxsplit=1)
        inst = parts[0]
        operand = parts[1] if len(parts) > 1 else None

        if inst == "LIA":
            output += [(OPCODES["LIA"]), (parse_operand(operand))]
            pc += 2
        elif inst == "STA":
            addr = parse_operand(operand)
            output += [(OPCODES["STA"]), (addr & 0xFF), ((addr >> 8) & 0xFF)]
            pc += 3
        elif inst == "OUT":
            output += [(OPCODES["OUT"])]
            pc += 1
        elif inst == "HLT":
            output += [(OPCODES["HLT"])]
            pc += 1
        elif inst == "CAL":
            addr = labels.get(operand, 0)
            output += [(OPCODES["CAL"]), (addr & 0xFF), ((addr >> 8) & 0xFF)]
            pc += 3
        else:
            print("compilation error: unknown instruction", inst)
            sys.exit(1)

    return output

def main():
    if len(sys.argv) < 2:
        print("Usage: python assembly.py <inputfile> [outputfile]")
        print("SUGGESTION: input files should use the .jal extension and output files should be in the .jbn format.")
        sys.exit(1)
    infile = sys.argv[1]
    outfile = sys.argv[2] if len(sys.argv) > 2 else 0
    with open(infile, "r") as f:
        lines = f.readlines()
    machine_code = assemble(lines)
    # Output as bytes (or write to file, or print as Python list)
    print(f"compilation successful -- generating {outfile}" if outfile else "compilation successful -- printing to console")
    if outfile == 0:
        print(machine_code)
    else:
        with open(outfile, "wb") as f:
            f.write(bytearray(machine_code))

if __name__ == "__main__":
    main()