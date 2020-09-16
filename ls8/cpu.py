"""CPU functionality."""

import sys

filename = sys.argv[1]

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 #memory
        self.pc = 0 #program counter, address of the currently-executing instruction
        self.register = [0] * 8 # R0-R7
        self.running = True
        self.reg = [0] * 8,
        self.SP = 0xf4

    def load(self, filename):
        """Load a program into memory."""
        #get file path
        #split input file per line
        #turn into program instructions (str -> int)
        #specify base

        address = 0 #index into memory / address of currently-executing instruction

        with open(filename) as f:
            for address, line in enumerate(f):
                line = line.split('#')

                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue

                self.ram[address] = v
                address += 1

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        #elif op == "SUB": etc
        elif op == 'MUL':
            self.register[reg_a] *= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        # create program dicti
        prog = {
            'LDI': 0b10000010,
            'PRN': 0b01000111,
            'HLT': 0b00000001,
            'ADD': 0b10100000,
            'MUL': 0b10100010,
            'PUSH': 0b01000101,
            'POP': 0b01000110
        }
        while self.running:
            IR = self.ram[self.pc] # Instruction register, copy of the currently-executed instruction
            operandA = self.ram_read(self.pc + 1)
            operandB = self.ram_read(self.pc + 2)

            if IR == prog['HLT']: #instruct to HLT
                self.running = False

            elif IR == prog['LDI']: #instruct to save
                address = operandA
                value = operandB
                self.register[address] = value
                self.pc += 3

            elif IR == prog['PRN']: #instruct to print
                address = operandA
                value = self.register[address]
                print(value)
                self.pc += 2

            elif IR == prog['MUL']: #instruct to multiply
                self.alu('MUL', operandA, operandB)
                self.pc +=3

            elif IR == prog['PUSH']: #instruct value in the register into RAM and save the value to the stack
                address = operandA
                value = self.register[address]
                self.SP -= 1
                self.ram[self.SP] = value
                self.pc += 2

            elif IR == prog['POP']: #instruct to retrieve the value from RAM and add to register
                address = operandA
                value = self.ram[self.SP]
                self.register[address] = value

                self.SP += 1
                self.pc += 2

            else:
                print(f"Can't find {IR} with index of {self.pc}")
                sys.exit(1)