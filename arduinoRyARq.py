import pyfirmata
import time
import serial
# import board
# import busio
# import adafruit_mcp4725
# i2c = busio.I2C(board.SCL, board.SDA)
# dac = adafruit_mcp4725.MCP4725(i2c)

# boards = pyfirmata.Arduino("COM10")
ser = serial.Serial('COM13',115200)

dt = ''
command = 0
receivedData = ''
receivedACK = ''
transfering = False
f = open("test.txt","r")
buffer = ''
ACK = '#'

dataCount = 0
def receiveCommand():
    global receivedData
    global dt
    size = 0
    count = 0
    global dataCount #change
    if ser.in_waiting > 0:
        print('receivingCommand')
        receivedData += (ser.read(4)).decode()
        print(receivedData)
        dt = receivedData
        # receivedData += testframe[size:size+8]
        # tmp = bitToChar(receivedData)
        # print('received data',tmp)
        # size+=8
        # if tmp == chr(17):
        #     dataCount += 1
        # if count >= 2:
        #     return
        #     # return 0
        # dt.append(tmp)
        receivedData ='' #add
        # write-file
        # if len(dt) >= 2:
        #     return 0
    return
    # return 0

def getImg():
    print('getting img')
    global command
    global dt
    command = dt[1]
    dt = ''
    if command == 'w':
        f = open("img.txt","w")
        f.write('capture left')
        f.close()
    elif command == chr(2):
        pass
    elif command == chr(3):
        pass
    elif command == chr(4):
        pass
    elif command == chr(5):
        pass
    elif command == chr(6):
        pass

def bitToChar(arr):
    a = 0
    for i in range(len(arr)):
        if arr[i] == '1':
            a += pow(i)
    return chr(a)

def sendData():
    print('sending img data')
    global f
    global buffer
    
    n = fread(5,1,f)
    framed = makeFrame(buffer,'w')
    print('framed',framed)

    ser.write(framed.encode())
    
    return n

def receiveAck():
    global receivedData
    size = 0
    global dt
    # count = 0#change
    global dataCount
    if ser.in_waiting > 0:
        print('wait for ack')
        receivedData += (ser.read(4)).decode()
        print(receivedData)
        dt = receivedData
        # receivedData += testframe[size:size+8]
        # tmp = bitToChar(receivedData)
        # print('received ack',tmp)

            # return 0
        # dt.append(tmp)
        receivedData ='' #add
        # break
        # write-file
        # if len(dt) >= 2:
        #     return 0
    # return 0

def makeFrame(data,sum):
    frame = ''
    frame += '@'
    for i in range(len(data)):
        frame += data[i]
    frame += sum
    frame += '@'
    return frame

def makeSum(data):
    sum = 0
    for i in range(len(data)):
        sum += ord(data[i])
    return chr(sum)


def fread(size, count, file):
    global buffer
    buffer = ''
    elementCount = 0
    for i in range(count):
        tmp = file.read(size)
        if tmp == '':
            break
        buffer += tmp
        elementCount += 1
        # print(buffer)
    return elementCount


def pow(i):
    n = 1
    for i in range(i):
        n *= 2
    return n

def sendAck():
    framedAck = makeFrame(ACK,ACK)
    print('sending ACK : ',framedAck)
    ser.write(framedAck.encode())

time_out = 1
while True: 
    dt = ''
    while len(dt) == 0:
        receiveCommand()
        # time.sleep(1)
    time.sleep(1)
    sendAck()
    time.sleep(1)
    getImg()
    time.sleep(1)
    dt = ''
    transfering = 1
    time.sleep(1)
    while transfering:
        time.sleep(1)
        n = sendData()
            
        # print(n)
        dt = ''
        timestart = time.time()
        time.sleep(1)
        while len(dt) == 0 :
            receiveAck()
        # sendAck()
        # time.sleep(1)
        
            # framed = makeFrame(buffer,'w')
            # print('resend framed',framed)
            # ser.write(framed.encode())
            # timestart = time.time() 
            # while len(dt) == 0:
            #     receiveAck()
        dt = ''
        time.sleep(1)
        if n == 0:
            transfering = 0
            break

    