import msvcrt


while True:

    key = msvcrt.getch()
    if key == b'\xe0':

        scan_code = msvcrt.getch()
        print(f'Special Key: {scan_code.decode()}')

    elif key == b'\x03':
        break
    else:
        print(key)