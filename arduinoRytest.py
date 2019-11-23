dt = list()
command = 0
receivedData = ''
receivedACK = ''
transfering = 0
f = open("test.txt","r")
testframetmp = '00100011001100010111011100100011'
testframe = ''
buffer = ''
for i in range(len(testframetmp)):
    testframe += testframetmp[len(testframetmp)-1-i]
print('testframe',testframe)




def receiveCommand():
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

def getImg():
    global command
    command = dt[2]
    if command == '1':
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
    global f
    global buffer
    
    n = fread(8,1,f)
    framed = makeFrame(buffer,'w')
    print('framed',framed)
    # ser.write(buffer.encode())
    
    return n

def receiveAck():
    global receivedData
    size = 0
    count = 0#change
    while True:
    # receivedData += ser.readline()
        receivedData += testframe[size:size+8]
        tmp = bitToChar(receivedData)
        print('received ack',tmp)
        size+=8
        
        if tmp == '#':
            count += 1
        if count >= 2:
            return 0
        dt.append(tmp)
        receivedData ='' #add
        # break
        # write-file
        # if len(dt) >= 2:
        #     return 0
    return 0

def makeFrame(data,sum):
    frame = ''
    frame += '#'
    for i in range(len(data)):
        print('data',data[i])
        frame += data[i]
    frame += sum
    frame += '#'
    return frame

def makeSum(data):
    sum = 0
    for i in range(len(data)):
        sum += ord(data[i])
    return chr(sum)



def fread(size, count, file):
    global buffer
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

# print(bitToChar('10001100'))
# print(makeFrame('qwer','w'))


while True: 
    
    receiveCommand()
    getImg()
    transfering = 1
    while transfering:
        n = sendData()
        # print(n)
        receivedData=''
        receiveAck()
        if n == 0:
            break
    break