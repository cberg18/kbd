import re
import sys

def modify_kicad_pcb(filename):
    with open(filename, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    in_diode = False
    for i, line in enumerate(lines):
        if '(footprint "Diode_SMD:' in line or '(footprint "Diode_THT:' in line or '(footprint "Diode_' in line:
            in_diode = True
        elif in_diode and line.strip().startswith('(at '):
            parts = line.strip().split()
            x_str = parts[1]
            if x_str.endswith(')'):
                x_str = x_str[:-1]
                x_val = float(x_str) + 3.3
                new_line = f'(at {x_val:g})'
            else:
                x_val = float(x_str) + 3.3
                if len(parts) == 3:
                    y_str = parts[2][:-1]
                    new_line = f'(at {x_val:g} {y_str})'
                else:
                    y_str = parts[2]
                    rot_str = ' '.join(parts[3:])
                    rot_str = rot_str[:-1]
                    new_line = f'(at {x_val:g} {y_str} {rot_str})'
            
            indent = line[:len(line) - len(line.lstrip())]
            lines[i] = indent + new_line
            in_diode = False # only modify the main footprint `at`

    with open(filename, 'w') as f:
        f.write('\n'.join(lines))

modify_kicad_pcb('Main Board.kicad_pcb')
