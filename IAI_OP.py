import random
import sys
import threading
from time import sleep
import uic_serial
from ctypes import create_string_buffer

#############################
# ****** B8 code Start ******
#############################


def checksum(bytestr):
    result = 0
    for x in bytestr:
        result = result ^ x
    return bytes(chr(result), 'ascii')


def payment_cmd():
    K = b'\xC2'
    L = b'\x01\x06<Req><Cmd><CmdId>TxnStart</CmdId><CmdTout>300</CmdTout></Cmd><Param><Txn><TxnType>Sale</TxnType>' \
        b'<AccType>Credit/Debit</AccType><CurrCode>840</CurrCode><TxnAmt>'
    M = bytes((str(random.randint(0, 9)) + str(random.randint(1, 9))), 'ascii')
    N = b'.00</TxnAmt><CashbackAmt>0</CashbackAmt><TipAmt>0</TipAmt><InvoiceId></InvoiceId></Txn></Param></Req>'
    O = L + M + N
    P = checksum(O)
    return K + O + P


# def delay_msec():
#     return random.randint(1000, 3999)


def Senddata(cmd):
    buf_size = len(cmd)+1
    buf = create_string_buffer(buf_size)
    buf.value = cmd
    # print(f'PC2 --> {ser.portname} : {buf.value}')
    ser.rs232_SendBuf(buf, len(cmd))


def Rcvdata(Rcvlen):  # Rcvdata(Comport,預期接收長度)
    # ETX = 3
    # SO = 14
    total_resp = b''
    buf_size = 1024
    buf = create_string_buffer(buf_size)
    n = 0
    buf.value = b''
    Rcvn = 0  # 目前實際接收到的資料長度
    readRcvbuftimes = 0
    while Rcvn < Rcvlen:
        #print(time.strftime('%Y-%m-%d %H:%M:%S')+' Read buf:')
        n = ser.rs232_RcvBuf(buf, buf_size)
        readRcvbuftimes = readRcvbuftimes+1
        #print (time.strftime('%Y-%m-%d %H:%M:%S')+' receive n={}'.format(n))
        #print('Rcv data={}'.format(buf.value[0:n]))
        #print('************************Next Read***********************')
        if n > 0:
            total_resp = total_resp+buf.value[0:n]
            # #print('Rcv data={}'.format(buf.value[1:n-1]))
            # #print('Eot ={}'.format(buf.value[n - 2]))
            # if (buf.value[n-2] == ETX or buf.value[n-2] == SO):
            #     #print('Rcv data LRC={}'.format(checksum(buf.value[1:n - 1])))
            #     #print('Rcv data LRC={}'.format(buf.value[n-1]))
            #     if (checksum(total_resp[2:- 1]) == bytes(chr(buf.value[n - 1]), 'ascii')):
            #         Rcvn = Rcvlen
            # # Senddata(Comportn,buf.value[0:n])
            Rcvn = Rcvn+n
            n = 0
        else:  # else 接收資料是否完成?
            # sleep(0.001)# 不加timeout 須sleep 1msec,不然詢問次數太快太多9600以下baudrate反而讀不到資料(若此處不加sleep,9600 baudrate以下設定，下面的readRcvbuftimes須改為>10000次，不合理)
            #if Rcvn == 0:  # if 收完資料判定條件:(可修改ex:Bezel8判定目前收到的資料total_resp最後第二字元為<03> or <0E> or 只有單一字元<06> ACK <04> EOT <15>NACK)，因目前用loop back傳送資料,command送出長度為266，確定接收資料長度應為266，判定Rcvn已接收266時跳出接收迴圈
            Rcvn = Rcvlen
            if Rcvn > 1 and readRcvbuftimes > 50:
                Rcvn = Rcvlen
            # if readRcvbuftimes>200:#if 如果遇到特殊狀況如斷線、測試機器當機時，因沒設timer若m.RS232_Rcvbuf讀取數超過50(可修改)次(50*1msec=50msec)，也必須跳出接收迴圈，避免卡住(另一種timeout 方式，資料越長或Vcom baudrate越低此數值須加大因接收速度越慢收到的時間也需要越大)。
            #    Rcvn=Rcvlen
            #if ...:可以自行增加條件
            #if ...:可以自行增加條件

    return total_resp


###########################
# ****** B8 code End ******
###########################


def get_random_range(r):
    if r >= 100 and 400 > r:
        return 1
    elif r >= 400 and 700 > r:
        return 2
    elif r >= 700 and 999 >= r:
        return 3
    else:
        return 4


def delay_random_msec(last_msec):
    new_msec = random.randint(100, 999)

    new_range = get_random_range(new_msec)
    last_range = get_random_range(last_msec)

    #print("msec : {}, r_range : {}, last_msec : {}, last_range : {}".format(new_msec, new_range, last_msec, last_range))

    if new_range == last_range:
        return delay_random_msec(last_msec)
    else:
        return new_msec


def option_01_Go_Home(ser):
    print('GO HOME')
    cmd = b'!99HOM0100@@\x0D\x0A'
    print(f'PC --> {ser.portname} : {cmd}')
    Senddata(cmd)
    A = Rcvdata(1024)
    print(f'PC --< {ser.portname} : {A}\n')


def optopn_02_Move_Forward(ser):
    print('FORWARD')
    cmd = b'!99MOV010000000500000070@@\x0D\x0A'
    print(f'PC --> {ser.portname} : {cmd}')
    Senddata(cmd)
    A = Rcvdata(1024)
    print(f'PC --< {ser.portname} : {A}\n')


def option_03_Move_Reverse(ser):
    print('REVERSE')
    cmd = b'!99MOV010000299900000060@@\x0D\x0A'
    print(f'PC --> {ser.portname} : {cmd}')
    Senddata(cmd)
    A = Rcvdata(1024)
    print(f'PC --< {ser.portname} : {A}\n')


def option_04_Loop(ser):
    sleep_sec = 0
    while True:
        for i in range(1000):
            print('Loop\n')
            # Senddata(b'!99MOV010000299900000020@@<CR><LF>')
            cmd = b'!99MOV010000299900000070@@\x0D\x0A'
            print(f'PC --> {ser.portname} : {cmd}')
            Senddata(cmd)
            A = Rcvdata(1024)
            print(f'PC --< {ser.portname} : {A}')

            sleep_sec = delay_random_msec(sleep_sec)
            print(f"delay {sleep_sec} msec\n")
            sleep(sleep_sec/1000)
            # sleep(2)

            # Senddata(b'!99MOV010000299900000010@@<CR><LF>')
            cmd = b'!99MOV010000299900000060@@\x0D\x0A'
            print(f'PC --> {ser.portname} : {cmd}')
            Senddata(cmd)
            A = Rcvdata(1024)
            print(f'PC --< {ser.portname} : {A}')

            sleep_sec = delay_random_msec(sleep_sec)
            print(f"delay {sleep_sec} msec")
            sleep(sleep_sec/1000)
        # sleep(2)
        # Senddata(b'!99MOV010000299900000020@@<CR><LF>')
        cmd = b'!99MOV010000299900000070@@\x0D\x0A'
        print(f'PC --> {ser.portname} : {cmd}')
        Senddata(cmd)
        A = Rcvdata(1024)
        print(f'PC --< {ser.portname} : {A}')
        sleep(7)

        # Senddata(b'!99MOV010000299900000010@@<CR><LF>')
        cmd = b'!99MOV010000299900000060@@\x0D\x0A'
        print(f'PC --> {ser.portname} : {cmd}')
        Senddata(cmd)
        A = Rcvdata(1024)
        print(f'PC --< {ser.portname} : {A}')
        sleep(15)


def option_05_Reset_The_Driver(ser):
    print('RESET')
    cmd = b'!99RST@@\x0D\x0A'
    print(f'PC --> {ser.portname} : {cmd}')
    Senddata(cmd)
    A = Rcvdata(1024)
    print(f'PC --< {ser.portname} : {A}\n')


# main function**********
#ser = uic_serial.UIC_Serial(9600, "COM3", 0, 0, 100, 0, 0)
ser = uic_serial.UIC_Serial(9600, sys.argv[1], 0, 0, 100, 0, 0)
# ser.rs232_Init()


while True:
    if ser.rs232_OpenPort()==0:
        print('{} on, please select option:'.format(ser.portname))
        choice = input('1.GO HOME、2.FORWARD、3.REVERSE、4.LOOP、5.RESET、按e退出:')
        if choice == '1':
            option_01_Go_Home(ser)
        elif choice == '2':
            optopn_02_Move_Forward(ser)
        elif choice == '3':
            option_03_Move_Reverse(ser)
        elif choice == '4':
            option_04_Loop(ser)
        elif choice == '5':
            option_05_Reset_The_Driver(ser)
        elif choice == 'e':
            print('退出')
            sys.exit()
        else:
            print(f'指令錯誤…({choice})')

