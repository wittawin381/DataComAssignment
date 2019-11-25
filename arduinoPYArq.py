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
dataCount = 0
buffer = ''


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
    frame += chr(17) #flag
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
            imgData = open("data.txt","a")
            imgData.write(dt[1:len(dt)-3])
            imgData.close()
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

def receiveAck():
    global receivedData
    size = 0
    # count = 0#change
    global dataCount
    if ser.in_waiting > 0:
        print('wait for ack')
        receivedData += (ser.readline()).decode()
        # receivedData += testframe[size:size+8]
        tmp = bitToChar(receivedData)
        print('received ack',tmp)
        size+=8
        
        if tmp ==  chr(17):
            dataCount += 1
        if dataCount >= 2:
            return
            # return 0
        dt.append(tmp)
        receivedData ='' #add
        # break
        # write-file
        # if len(dt) >= 2:
        #     return 0
    # return 0

while True:
    cmd = input("Input :")
    transfering = 1
    dt.clear()
    framed = makeFrame(cmd,cmd)
    sendData(framed)
    timestart = time.time()
    while time.time() < timestart + 2:
        receiveAck()
    while len(dt) == 0:
        framed = makeFrame(buffer,'w')
        print('resend framed',framed)
        ser.write(framed.encode())
        timestart = time.time()
        while time.time() < timestart + 2:
            receiveAck()
    dt.clear()
    while transfering:
        transfering = receiveData()
        sendAck()