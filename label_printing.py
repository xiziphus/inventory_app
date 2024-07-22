import subprocess

def print_label(part_number, printer_name="YOUR_PRINTER_NAME"):
    zpl_command = f"^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH0,0^JMA^PRA,8~SD15^JUS^LRN^CI27^PA0,1,1,0^XZ" \
                  f"^XA" \
                  f"^MMT" \
                  f"^PW799" \
                  f"^LL400" \
                  f"^LS0" \
                  f"^FT63,295^A0N,43,35^FH^CI28^FD{part_number}^FS^CI27" \
                  f"^BY1,3,50^FT80,363^BCN,,N,N" \
                  f"^FH^FD{part_number}^FS" \
                  f"^FT48,248^A0N,25,25^FH^CI28^FDMALHOTRA CABLES^FS^CI27" \
                  f"^FT294,248^A0N,25,25^FH^CI28^FDMALHOTRA CABLES^FS^CI27" \
                  f"^FT326,297^A0N,43,35^FH^CI28^FD{part_number}^FS^CI27" \
                  f"^BY1,3,50^FT330,361^BCN,,N,N" \
                  f"^FH^FD{part_number}^FS" \
                  f"^FT536,246^A0N,25,25^FH^CI28^FDMALHOTRA CABLES^FS^CI27" \
                  f"^FT559,297^A0N,43,35^FH^CI28^FD{part_number}^FS^CI27" \
                  f"^BY1,3,50^FT560,361^BCN,,N,N" \
                  f"^FH^FD{part_number}^FS" \
                  f"^FT63,133^A0N,43,35^FH^CI28^FD{part_number}^FS^CI27" \
                  f"^BY1,3,50^FT80,200^BCN,,N,N" \
                  f"^FH^FD{part_number}^FS" \
                  f"^FT48,85^A0N,25,25^FH^CI28^FDMALHOTRA CABLES^FS^CI27" \
                  f"^FT294,85^A0N,25,25^FH^CI28^FDMALHOTRA CABLES^FS^CI27" \
                  f"^FT326,134^A0N,43,35^FH^CI28^FD{part_number}^FS^CI27" \
                  f"^BY1,3,50^FT330,199^BCN,,N,N" \
                  f"^FH^FD{part_number}^FS" \
                  f"^FT536,84^A0N,25,25^FH^CI28^FDMALHOTRA CABLES^FS^CI27" \
                  f"^FT559,134^A0N,43,35^FH^CI28^FD{part_number}^FS^CI27" \
                  f"^BY1,3,50^FT560,199^BCN,,N,N" \
                  f"^FH^FD{part_number}^FS" \
                  f"^PQ1,0,1,Y^XZ"
    
    print_command = f'echo "{zpl_command}" | lp -d {printer_name}'
    
    subprocess.run(print_command, shell=True)
