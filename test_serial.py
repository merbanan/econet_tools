import serial
import argparse
from time import sleep
sleep(0.05)
# sys memrl BFB90000

#<Address>       <Value>
#0xbfb90000      0x00960020

def get_reg_value(ser, mode, addr):

    if mode == "sys":
        #test
        ser.timeout = 1
        #sero = "\n"
        #ser.write(sero.encode('ascii'))
        #ser.flushOutput()
        #ser.flushInput()

        sero = "sys memrl %s\n" % (hex(addr).lstrip("0x"))
        ser.flushOutput()
        ser.flushInput()
        #print (sero)
        ser.write(sero.encode('ascii'))
        sleep(0.040)
        data = ser.readline()
        #sleep(0.05)
        #print('Data received:', data)
        data = ser.readline()
        #sleep(0.05)
        #print('Data received:', data)
        data = ser.readline()
        #sleep(0.05)
        #print('Data received:', data)
        data = ser.readline()
        #sleep(0.05)
        #print('Data received:', data.decode())
        ds = data.decode()
        sub_ds = ds[13:-2]
        ser.flushInput()
        reg_val = "0x%s" % sub_ds.upper()
    else:
        ser.timeout = 1
        #print("devmem %s\n" % (hex(addr)))
        sero = "devmem %s\n" % (hex(addr))
        ser.flushOutput()
        ser.flushInput()
        ser.write(sero.encode('ascii'))
        sleep(0.015)
        data = ser.readline()
        #print('Data received:', data)
        data = ser.readline()
        #print(data)
        reg_val = data.decode()
        #print('Data received:', data)
        #data = ser.readline()
        #logging.info(f"Received: {data}")
        ser.flushInput()
        #print("%s" % reg_val.rstrip("\r\n"))
    return reg_val.rstrip("\r\n")

def main(mode, start_addr, num_regs):
    
    print('Mode: ' + mode);
    print('Start address: ' + start_addr);

    s_addr = int(start_addr.replace("0x", ""),16)
    num_regs_int = int(int(num_regs.replace("0x", ""),16))
    print('Number of registers: ' + str(num_regs_int) +' (' + num_regs + ')');

    ser = serial.Serial('/dev/ttyUSB0', 115200)
    #ser.open()

    if ser.isOpen():
        print('Serial connection established!')
    else:
        print('Error: Failed to establish serial connection.')

    for x in range(0, num_regs_int, 8*4):
        v0 = get_reg_value(ser, mode, s_addr+x)
        v1 = get_reg_value(ser, mode, s_addr+x+1*4)
        v2 = get_reg_value(ser, mode, s_addr+x+2*4)
        v3 = get_reg_value(ser, mode, s_addr+x+3*4)
        v4 = get_reg_value(ser, mode, s_addr+x+4*4)
        v5 = get_reg_value(ser, mode, s_addr+x+5*4)
        v6 = get_reg_value(ser, mode, s_addr+x+6*4)
        v7 = get_reg_value(ser, mode, s_addr+x+7*4)
        
        #v0 = hex(s_addr+x)
        d_addr = str(hex(s_addr+x))
        if (mode == "devmem"):
            d_addr =  "b%s" % d_addr[3:]
            #d_addr = d_addr.lower()
        else:
            d_addr =  d_addr[2:]
        print("[0x%s] %s %s %s %s %s %s %s %s" % (d_addr, v0, v1, v2, v3, v4, v5, v6, v7))

    #while True:
        #test = 'devmem 0x1234a100\n'
        ##test = 'env'
        #ser.write(test.encode('ascii'))
        #ser.timeout = 1
        #data = ser.readline()
        #logging.info(f"Received: {data}")
        #print('Data received:', data)
        #data = ser.readline()
        #logging.info(f"Received: {data}")
        #print('Data received:', data)
        #data = ser.readline()
        #logging.info(f"Received: {data}")

        # Add code to send data and log it as well
    ser.close()
    exit()


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='Econet user space memory dumper')
    parser.add_argument('--mode', type=str, required=False,
                        default='devmem',
                        help='mode sys/devmem')
    parser.add_argument('--start_addr', type=str, required=True,
                        help='dump start address')
    parser.add_argument('--num_regs', type=str, required=False,
                        default='0x100',
                        help='amount of registers to dump in hex')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(mode=args.mode, start_addr=args.start_addr, num_regs=args.num_regs)
