from basesolver import BaseSolver

class Dock1:
    def __init__(self, input_lines):
        self.cmds = input_lines
        self.memory = {}
    
    def parse_mv_cmd(cmd):
        value = cmd.split(' = ')[1]
        mem = cmd.split('[')[1].split(']')[0]
        return int(mem), int(value)
    
    def parse_mask_cmd(cmd):
        return [value for value in cmd.split(' = ')[1]]
    
    def value_to_bits_value(value):
        # Calculate bits
        bits_value = []
        while value:
            bit = value % 2
            bits_value.append(bit)
            value = value // 2
        
        # Add padding
        bits_value.extend([0] * (36 - len(bits_value)))

        return bits_value[::-1]
    
    def bits_value_to_value(bits_value):
        bits_value = bits_value[::-1]
        value = 0
        for i in range(len(bits_value)):
            if bits_value[i] == 1:
                value += 2**i
        return value
    
    def apply_mask(bits_value, mask):
        bits_value = bits_value[::-1]
        mask = mask[::-1]
        for i in range(len(mask)):
            to_set = mask[i]
            if to_set != 'X':
                bits_value[i] = int(to_set)
        return bits_value[::-1]
    
    def run(self):
        for cmd in self.cmds:
            if cmd.startswith('mask'):
                mask = Dock1.parse_mask_cmd(cmd)
                self.mask = mask
            elif cmd.startswith('mem'):
                mem, value = Dock1.parse_mv_cmd(cmd)
                bits_value = Dock1.value_to_bits_value(value)
                masked_bits_value = Dock1.apply_mask(bits_value, self.mask)
                masked_value = Dock1.bits_value_to_value(masked_bits_value)
                self.memory[mem] = masked_value


class Dock2(Dock1):
    def apply_mask(bits_value, mask):
        # Apply mask
        bits_value = bits_value[::-1]
        mask = mask[::-1]
        for i in range(len(mask)):
            to_set = mask[i]
            if to_set == '0':
                continue
            elif to_set == '1':
                bits_value[i] = 1
            elif to_set == 'X':
                bits_value[i] = 'X'
        
        # Unpack
        packed_bits_values = [bits_value[::-1]]
        unpacked_bits_values = []
        while packed_bits_values:
            packed_bits_value = packed_bits_values.pop()
            if 'X' not in packed_bits_value:
                unpacked_bits_values.append(packed_bits_value)
                break
            x_at = packed_bits_value.index('X')

            bits_values_1 = packed_bits_value.copy()
            bits_values_1[x_at] = 0
            if 'X' not in bits_values_1:
                unpacked_bits_values.append(bits_values_1)
            else:
                packed_bits_values.append(bits_values_1)

            bits_values_2 = packed_bits_value.copy()
            bits_values_2[x_at] = 1
            if 'X' not in bits_values_2:
                unpacked_bits_values.append(bits_values_2)
            else:
                packed_bits_values.append(bits_values_2)
        return unpacked_bits_values

    def run(self):
        for cmd in self.cmds:
            if cmd.startswith('mask'):
                mask = Dock2.parse_mask_cmd(cmd)
                self.mask = mask
            elif cmd.startswith('mem'):
                mem, value = Dock2.parse_mv_cmd(cmd)
                bits_mem = Dock2.value_to_bits_value(mem)
                masked_bits_mems = Dock2.apply_mask(bits_mem, self.mask)
                for masked_bits_mem in masked_bits_mems:
                    mem = Dock2.bits_value_to_value(masked_bits_mem)
                    self.memory[mem] = value


class Y2020D14Solver(BaseSolver):
    def solve_part_a(self):
        dock = Dock1(self.lines)
        dock.run()
        result = sum([value for value in dock.memory.values()])
        return str(result)
    

    def solve_part_b(self):
        dock = Dock2(self.lines)
        dock.run()
        result = sum([value for value in dock.memory.values()])
        return str(result)
