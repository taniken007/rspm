# coding: utf-8
#!/usr/bin/env python

from time import sleep #for demo
import binascii  #temporary for convenience
# import serial
import json
import crc8

chk_count = 0
res_str = ""

# copy from crc8, should not be necessary here
poly = 0x07
mask = 0xFF
TABLE = [0 for i in range(256) ]

for i in range(256):
    c = i
    for j in range(8):
        if (c & 0x80):
            c = (((c << 1) & mask) ^ poly)
#            print (c)
        else:
            c <<= 1
#            print (c, "else")
        j +=1

    TABLE[i] = hex(c)
#    print ("table#",i," ",c,"",hex(c))
    i += 1
# END


def make_crc8(data_str): #copy, should not be necessary here
    sleep(2) # for demo
    crc8 = "0x00"
    print ("generating CRC...", data_str)
    for i in range(len(data_str)):
        crc8 = TABLE[int(crc8, 16) ^ int(
            binascii.hexlify(data_str[i].encode()), 16)]
    return crc8

def crc_calc(): #better moving to  crc8.py
    print ("received CRC8: ", recv_crc)
    self_result = 0
    self_crc_calc = "0x00"
    self_object = recv_command.encode('utf-8', 'replace').hex()
    print ("checking CRC...", self_object) # for demo
    for i in range(len(recv_command)):
        self_crc_calc = TABLE[int(self_crc_calc, 16) ^ int(
            binascii.hexlify(recv_command[i].encode()), 16)]
    print ("CRC check result:", self_crc_calc) #for demo
    if self_crc_calc == recv_crc:
        self_result = 1
    return self_result

def send(byte_str): #better to remove CRC calculation
#    print ("sending...", byte_str)
    self_json_str = json.dumps(byte_str)
#    ser = serial.Serial("/dev/serial0")  # Open named port
#    ser.baudrate = 9600  # Set baud rate to 9600
#    ser.write(self_json_str)  # Send back the received data
#    ser.close()
    print ("sent JSON: ", self_json_str)
#    print("Close...")
    sleep(1) # for demo

#def exec_command(self_command): #temporary, need to replace
#    sleep(2) # for demo
#    print ("processing...", self_command)
#    crc8_value = make_crc8(self_command)
#    res_str = self_command + crc8_value + '\n'
#    send(res_str)


while True:
#    recv_msg = input("message from MainOBC: ") # for demo
#    self_msg = json.loads(recv_msg)
    self_msg = input("message from MainOBC: ") # for demo
    crc_chk = 0

    if self_msg == "OK":
        print ("command completed")
    elif self_msg == "NG":
        print ("Received NG. Resending...")
        send(res_str)
    elif self_msg == "Error":
        print ("from Main OBC: imcomplete !!!")
        break
    else:
        recv_crc = self_msg[-4:]
        recv_command = self_msg[:-5]
        print ("received command: ", recv_command)
        crc_chk = crc_calc()
        print ("crc check result: ", crc_chk)
        if crc_chk == 1:
            print ("OK")
            resok = "OK" + "\n"
            send(resok)
            chk_count = 0
            print ("command processing...", recv_command) # for demo
#            exec_command(recv_command)
            crc8_value = make_crc8(recv_command)
            res_str = recv_command + crc8_value + '\n'
            send(res_str)
        else:
            chk_count += 1
            if chk_count >= 3:
                print ("Comm Error !")
                reserr = "Error" + "\n" #need to specify this msg
                chk_count = 0
                send(reserr)
                break
            else:
                print("NG")
                resng = "NG" +"\n"
                send(resng)
