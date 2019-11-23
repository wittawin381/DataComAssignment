import pyfirmata
import time
import serial
# import board
# import busio
# import adafruit_mcp4725
# i2c = busio.I2C(board.SCL, board.SDA)
# dac = adafruit_mcp4725.MCP4725(i2c)

# boards = pyfirmata.Arduino('COM13')
ser = serial.Serial('COM8',115200)

ACK = '#'
dt = list()
receivedData = ''
receivedDataFinal = ''
transfering = 0


    # ser.write(cmd.encode())

# def sending(data):
#     sendData(data[i])

def sendData(data):
    print('sending data')
    ser.write(data.encode())
    # for i in range(len(data)):
    #     ser.write(data[i].encode())



def makeFrame(cmd,sum):
    print('makeframe')
    frame = ''
    frame += chr(17)
    if cmd == 'w':
        frame += chr(1)
    if cmd == 'e':
        frame += chr(2)
    if cmd == 'r':
        frame += chr(3)
    if cmd == 's':
        frame += chr(4)
    if cmd == 'd':
        frame += chr(5)
    if cmd == 'f':
        frame += chr(6)
    frame += sum
    frame += chr(17)
    print(frame)
    return frame

def receiveData():
    global receivedData
    count = 0
    print('wait for response')
    while True:
        print('received img data')
        receivedData += (ser.readline()).decode()
        tmp = bitToChar(receivedData)
        print('received data',tmp)
        if tmp == chr(17):
            count += 1
        if count >= 2:
            return 0
        dt.append(tmp)
        receivedData =''
        
    return 0
        

def sendAck():
    framedAck = makeFrame(ACK,ACK)
    print('sending ACK : ',framedAck)
    sendData(framedAck)

def bitToChar(arr):
    a = 0
    for i in range(len(arr)):
        if arr[i] == '1':
            a += pow(i)
    return chr(a)

def pow(i):
    n = 1
    for i in range(i):
        n *= 2
    return n

while True:
    cmd = input("Input :")
    transfering = 1
    dt.clear()
    framed = makeFrame(cmd,cmd)
    sendData(framed)
    while transfering:
        transfering = receiveData()
        sendAck()