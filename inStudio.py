import socket
import logging
import time

logging.basicConfig(level=logging.DEBUG, format=r"%(asctime)s - %(filename)s:%(lineno)d [%(levelname)s]: %(message)s")

def create_server(ip_in: str, port_in: int):
    sock = socket.socket()
    sock.bind((ip_in, port_in))
    sock.listen(1)
    return sock

class Dobot:

    def __init__(self):

        self._curPoX = 0
        self._curPosY = 0
        self._curPosZ = 0
        self._curPosR = 0
        self._curPosJ1 = 0
        self._curPosJ2 = 0
        self._curPosJ3 = 0
        self._ctrl = 0
        self._speed = 0
        self._ptpMode = 2
        self._whatReturn = 0
        self._realTime = 0

    def moveTo(self, x, y, z, r):

        dType.SetPTPCmd(api, self.ptpMode, x, y, z, r)

    def changePos(self):

        self._curPosX, self._curPosY, self._curPosZ, self._curPosJ1, self._curPosJ2, self._curPosJ2, self._curPosJ3, self._curPosJ4 = map(dType.GetPose(api))

    def printPosSocketWorld(self, sock):

        strIn = str(self._curPosX) + " " + str(self._curPosY) + " " + str(self._curPosZ)+ " " + str(self._curPosR) + "\n"
        logging.info("Dobot -> CU :    " + strIn)
        sock.send(strIn.encode())

    def printPosSocketJoint(self, sock):

        strIn = str(self._curPosJ1) + " " + str(self._curPosJ2) + " " + str(self._curPosJ3)+ " " + str(self._curPosJ4) + "\n"
        logging.info("Dobot -> CU :    " + strIn)
        sock.send(strIn.encode())
    


port = 9093
ip = "192.168.1.118"

logging.info("Server started!")

dobotMagic = Dobot()

while True:

    conn, addr = create_server(ip, port).accept()

    logging.info("connect CU with IP - "+ str(addr[0])+" and port -"+str(addr[1]))

    try:

        while True:

            dobotMagic.changePos()
            data = conn.recv(1024).decode()
				
            if not data:

                break
			

            logging.info("CU -> Dobot :    "+str(data))
			
            x, y, z, r = map(int, data.split())

            dobotMagic.moveTo(x, y, z, r)

            timeBefore = time.time()

            while True:

                dobotMagic.printPosSocketWorld(conn)
                dobotMagic.printPosSocketJoint(conn)
                if (time.time() - timeBefore > 5):
                    break
            
    
    except:

        logging.error("Error! Connect aborted by exception")

    logging.info("Connection aborted CU")
    
    conn.close()
