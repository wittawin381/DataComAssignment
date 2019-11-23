ACK = '#'
dt = list()
receivedData = ''
receivedDataFinal = ''
transfering = 0

testframetmp = '00100011001100010111011100100011'
testframe = ''
for i in range(len(testframetmp)):
    testframe += testframetmp[len(testframetmp)-1-i]
print('testframe',testframe)
    # ser.write(cmd.encode())

# def sending(data):
#     sendData(data[i])

def sendData(data):
    print(data.encode())
    # ser.write(data.encode())
    # for i in range(len(data)):
    #     ser.write(data[i].encode())



def makeFrame(cmd,sum):
    frame = ''
    frame += '$'
    if cmd == 'w':
        frame += '1'
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
    if cmd == '#':#add
        frame += '#'
    frame += sum
    frame += '$'
    return frame

def receiveData():
    global receivedData
    size = 0
    count = 0#change
    while True:
    # receivedData += ser.readline()
        receivedData += testframe[size:size+8]
        tmp = bitToChar(receivedData)
        print('received data',tmp)
        size+=8
        if tmp == '#':
            count += 1
        if count >= 2:
            return 0
        dt.append(tmp)
        receivedData ='' #add
        # write-file
        # if len(dt) >= 2:
        #     return 0
    return 0
        

def sendAck():
    framedAck = makeFrame(ACK,ACK)
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

print(bitToChar('01110111'))
while True:
    cmd = input("Input :")
    transfering = 1
    dt.clear()
    framed = makeFrame(cmd,cmd)
    print('frame :',framed)
    sendData(framed)
    while transfering:
        transfering = receiveData()
        
        sendAck()