import pyfirmata
import time
import serial
# import board
# import busio
# import adafruit_mcp4725
# i2c = busio.I2C(board.SCL, board.SDA)
# dac = adafruit_mcp4725.MCP4725(i2c)

# boards = pyfirmata.Arduino('COM13')
ser = serial.Serial('COM11',115200)

ACK = '#'
dt = ''
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
    frame += '#' #flag
    if cmd == 'w':
        frame += 'w'
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
    frame += '#'
    print(frame)
    return frame
recCount = 0
def receiveData():
    global receivedData
    global recCount
    global dt
    count = 0
    print('wait for response')
    if ser.in_waiting > 0:
        print('received img data')
        if recCount == 0:
            ser.read(4)
            recCount+=1
        receivedData += (ser.read(8)).decode()
        # tmp = bitToChar(receivedData)
        print('received data',receivedData)
        dt = receivedData
        imgData = open("data.txt","a")
        imgData.write(receivedData[1:6])
        imgData.close()
        # dt.append(tmp)
        receivedData =''
        
    return 0
        

def sendAck():
    framedAck = makeFrame(ACK,'x')
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

def receiveCommand():
    global receivedData
    size = 0
    count = 0
    global dt
    global dataCount #change
    if ser.in_waiting > 0:
        print('receivingAck')
        
        receivedData += (ser.read(4)).decode()
        # dt = receivedData
        print(receivedData)
        dt = receivedData
        # receivedData += testframe[size:size+8]
        # tmp = bitToChar(receivedData)
        # print('received data',tmp)
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
count = 0
while True:
    cmd = input("Input :")
    transfering = 1
    dt = ''
    framed = makeFrame(cmd,cmd)
    sendData(framed)
    time.sleep(1)
    timestart = time.time()
    # while len(dt) == 0:
    #     # time.sleep(1)
    #     # print("HELLO")
    #     if(len(dt) > 0):
    #         break
    #     receiveCommand()
        # time.sleep(1)
    
    time.sleep(1)
    while len(dt) == 0:
        framed = makeFrame(cmd,'w')
        print('resend framed',framed)
        ser.write(framed.encode())
        timestart = time.time()
        while time.time() < timestart + 3:
            receiveCommand()
            time.sleep(1)
    dt = ''
    transfering = 1
    time.sleep(1)
    while transfering:
        time.sleep(1)

        # while(len(dt) == 0):    
        receiveData()
        
        time.sleep(1)
        # time.sleep(1)
        framed = '@##@'
        print('send Ack',framed)
        sendData(framed)
        # if(dt == '@w@'):
        #     break
        # dt = ''
        print('dt : ',dt)
        if(len(dt) == 8 and dt[0] == '@' and dt[1] =='w' and dt[2] == '@'):
            transfering = 0
        dt = ''
        time.sleep(1)