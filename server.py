import socket
import logging

logging.basicConfig(level=logging.DEBUG, format=r"%(asctime)s - %(filename)s:%(lineno)d [%(levelname)s]: %(message)s")


def create_server(ip_in: str, port_in: int):
    sock = socket.socket()
    sock.bind((ip_in, port_in))
    sock.listen(1)
    return sock


class Dobot:

    def __init__(self):
        self.curPosX = 0
        self.curPosY = 0
        self.curPosZ = 0
        self.curPosR = 0
        self.curPosJ1 = 0
        self.curPosJ2 = 0
        self.curPosJ3 = 0
        self.curPosJ4 = 0
        self.ctrl = 0
        self.speed = 0
        self.ptpMode = 0
        self.whatReturn = 0
        self.realTime = 0

    #def moveTo(self, x, y, z, r):
        #dType.SetPTPCmd(api, self.ptpMode, x, y, z, r)

    # def changePos(self):

    # self.curPosX, self.curPosY, self.curPosZ, self.curPosJ1, self.curPosJ2, self.curPosJ2, self.curPosJ3, self.curPosJ4 = map(dType.GetPose(api))


port = 9090
ip = "192.168.43.203"

logging.info("Server started!")

dobotMagic = Dobot()

while True:

    conn, addr = create_server(ip, port).accept()

    logging.info("connect CU with IP - " + str(addr[0]) + " and port -" + str(addr[1]))

    try:

        while True:

            data = (conn.recv(1024)).decode()

            if not data:
                break

            logging.info("CU -> Dobot :    " + str(data))

            x, y, z, r = map(int, data.split())

            #dobotMagic.moveTo(x, y, z, r)

    except:

        logging.error("Error! Connect aborted by exception")

    logging.info("Connection aborted CU")
    conn.close()

