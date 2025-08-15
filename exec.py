# executes .jbn files
import sys
import os
import cpu

def execute_jbn(file_path):
    with open(file_path, "rb") as f:
        bytecode = f.read()
    memory = bytearray(65536)  # Initialize memory
    for i in range(len(bytecode)):
        if i < 65536 - cpu.CPU(bytearray(65536), 0).RESERVED:
            memory[i] = bytecode[i]
        else:
            print(f"Warning: Bytecode exceeds memory limit at index {i}. Truncating.")
            break
    mycpu = cpu.CPU(memory, 0x0000)
    mycpu.run_until_halt()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python exec.py <inputfile>")
        sys.exit(1)
    infile = sys.argv[1]
    if not infile.endswith(".jbn"):
        print("SUGGESTION: input files should use the .jbn extension.")
    if not os.path.exists(infile):
        print(f"Error: File {infile} does not exist.")
        sys.exit(1)
    execute_jbn(infile)