import os
import argparse


def process_file(input_file, output_suffix):
    filename, extension = os.path.splitext(input_file)
    output_file = filename + "-" + output_suffix + extension

    xmin = None
    xmax = None
    ymin = None
    ymax = None

    xcenter = None
    ycenter = None
    zfirst = None
    
    with open(input_file, 'r') as f_input:
        active = False
        for line in f_input:

            match line:
                case '; START OBJECT GCODE\n':
                    active = True
                case '; END OBJECT GCODE\n':
                    active = False
                case _:
                    if not active:
                        continue
                    splitline = line.split(' ')
                    match splitline[0]:
                        case 'G0' | 'G1':
                            for index, part in enumerate(splitline):
                                match part[0]:
                                    case 'X':
                                        tx = float(part[1:])
                                        if xmin == None or tx < xmin:
                                            xmin = tx
                                        if xmax == None or tx > xmax:
                                            xmax = tx
                                    case 'Y':
                                        ty = float(part[1:])
                                        if ymin == None or ty < ymin:
                                            ymin = ty
                                        if ymax == None or ty > ymax:
                                            ymax = ty
                                    case 'Z':
                                        if zfirst == None:
                                            zfirst = float(part[1:])
                                    case _:
                                        pass

        xcenter = (xmax + xmin) / 2
        ycenter = (ymax + ymin) / 2

        print(f'First Z: ({zfirst})')
        print(f'Min: ({xmin}, {ymin})')
        print(f'Max: ({xmax}, {ymax})')
        print(f'Found center: ({xcenter}, {ycenter})')
        
    with open(input_file, 'r') as f_input, open(output_file, 'w') as f_output:
        active = False
        x = xcenter
        y = ycenter
        z = zfirst

        for line in f_input:

            match line:
                case '; START OBJECT GCODE\n':
                    active = True
                case '; END OBJECT GCODE\n':
                    active = False
                case _:
                    pass

            splitline = line.split(' ')
            match splitline[0]:
                case 'G0' | 'G1':
                    if active:
                        for index, part in enumerate(splitline):
                            match part[0]:
                                case 'X':
                                    tx = float(part[1:])
                                    if x == None:
                                        x = tx
                                        splitline[index] = part[0] + str(0)
                                    else:
                                        dx = round(tx - x, 3)
                                        x = tx
                                        splitline[index] = part[0] + str(dx)
                                case 'Y':
                                    ty = float(part[1:])
                                    if y == None:
                                        y = ty
                                        splitline[index] = part[0] + str(0)
                                    else:
                                        dy = round(ty - y, 3)
                                        y = ty
                                        splitline[index] = part[0] + str(dy)
                                case 'Z':
                                    tz = float(part[1:])
                                    if z == None:
                                        z = tz
                                        part = part[0] + str(0)
                                    else:
                                        dz = round(tz - z, 3)
                                        z = tz
                                        splitline[index] = part[0] + str(dz)
                                case _:
                                    pass
                case 'G90':
                    if active:
                        splitline = ['G91', '; using relative coordinates\n']
                case _:
                    pass

            outline = ' '.join(splitline)
            if outline[-1] != '\n':
                outline += '\n'
            f_output.write(outline)

    print(f"File processed successfully. Output written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a file with a given suffix.")
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("--suffix", default="relative", help="Suffix to add to the output filename")
    args = parser.parse_args()

    process_file(args.input_file, args.suffix)
