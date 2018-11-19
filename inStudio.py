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
        self._ctrlTool = 0
        self._iteration = 0
        self._ctrlMode = 0
        self._numberIteration = 0
        self._toolValue = 0
        self._needX = 0
        self._needY = 0
        self._needZ = 0
        self._needR = 0
        self._epsilon = 4
        self._stopNow = False
        self._moveNow = False
        self._realTime = True

    def moveTo(self, x, y, z, r):
        dType.SetPTPCmd(api, self._ptpMode, x, y, z, r)

    def changePos(self):
        self._curPosX, self._curPosY, self._curPosZ, self._curPosJ1, self._curPosJ2, self._curPosJ2, self._curPosJ3,\
            self._curPosJ4 = map(dType.GetPose(api))

    def printPosSocketWorld(self, sock):
        strIn = str(self._curPosX) + " " + str(self._curPosY) + " " + str(self._curPosZ) + " " + str(
            self._curPosR) + "\n"
        logging.info("Dobot -> CU :    " + strIn)
        sock.send(strIn.encode())

    def printPosSocketJoint(self, sock):
        strIn = str(self._curPosJ1) + " " + str(self._curPosJ2) + " " + str(self._curPosJ3) + " " + str(
            self._curPosJ4) + "\n"
        logging.info("Dobot -> CU :    " + strIn)
        sock.send(strIn.encode())

    def robotMoving(self, sock):
        #TODO find Dobot possibility of moving

    def stopRobot(self, sock):
        #TODO function of stopping robot

    def realTimeMode(self, sock):

        self._iteration += 1
        self._ctrlMode = 0

        if self._numberIteration > 0:

            if (self._iteration % self._numberIteration) == 0:

                self._iteration = 0

                if (self._ctrl == 2) or (self._ctrl == 4):
                    self.printPosSocketWorld(sock)

                if (self._ctrl == 3) or (self._ctrl == 5):
                    self.printPosSocketJoint(sock)

        dataStr = sock.recv(128).decode()

        if dataStr:

            logging.info("CU -> Dobot :    " + dataStr)
            dataList = list(map(int, dataStr.split()))
            specialValue = dataList[0]

            if (dataList[0] < -1) or (dataList > 3):
                logging.error("Invalid package number")
                return

        else:

            specialValue = -1

        if (specialValue == -1):

            if (not self.robotMoving()) and self._stopNow:

                self._stopNow = False

                if self._whatReturn == 3:
                    self.printPosSocketWorld(sock)

                if self._whatReturn == 4:
                    self.printPosSocketJoint(sock)

                '''
                    tool action: open, close, relax
                '''

            if self._moveNow:

                self._moveNow = False
                self._stopNow = True

                # CRUTCH
                self._toolValue = self._ctrlTool
                # CRUTCH

                if self.robotMoving():

                    self.stopRobot()

                    if self._whatReturn == 3:
                        self.printPosSocketWorld(sock)

                    if self._whatReturn == 4:
                        self.printPosSocketJoint(sock)

                    self.moveTo(self._needX, self._needY, self._needZ.self._needR)

                    #TODO class point and functions for it

                else:

                    if self._whatReturn == 1:
                        self.printPosSocketWorld(sock)

                    if self._whatReturn == 2:
                        self.printPosSocketJoint(sock)

                    if self._ctrlTool == 2:

                    # CRUTCH tool action

                    #TODO read about tool-functions in DobotAPI

                    self.moveTo(self._needX, self._needY, self._needZ.self._needR)

        if specialValue == 0:
            self._ctrlMode = 1

        if specialValue == 1:
            self.pointInput(dataList)

        if specialValue == 2:
            self.setSetting(dataList)

        if specialValue == 3:
            self.specialPack(dataList[1])

        if self._ctrlMode == 1:
            self._realTime = False

    def noRealTime(self, sock):

        self._iteration += 1
        self._ctrlMode = 0

        if self._numberIteration > 0:

            if (self._iteration % self._numberIteration) == 0:

                self._iteration = 0

                if (self._ctrl == 2) or (self._ctrl == 4):
                    self.printPosSocketWorld(sock)

                if (self._ctrl == 3) or (self._ctrl == 5):
                    self.printPosSocketJoint(sock)

        dataStr = sock.recv(128).decode()

        if dataStr:

            logging.info("CU -> Dobot :    " + dataStr)
            dataList = list(map(int, dataStr.split()))
            specialValue = dataList[0]

            if (dataList[0] < -1) or (dataList > 3):
                logging.error("Invalid package number")
                return

        else:

            specialValue = -1

        if specialValue == -1:

            if (not self.robotMoving()) and self._stopNow:

                self._stopNow = False

                if self._whatReturn == 3:
                    self.printPosSocketWorld(sock)

                if self._whatReturn == 4:
                    self.printPosSocketJoint(sock)

                '''
                    tool action: open, close, relax
                '''

            if (self._moveNow) and (self.distanceToPoint() < self._epsilon):

                self._moveNow = False
                self._stopNow = True

                # CRUTCH
                self._toolValue = self._ctrlTool
                # CRUTCH

                if self._whatReturn == 1:
                    self.printPosSocketWorld(sock)

                if self._whatReturn == 2:
                    self.printPosSocketJoint(sock)

                if self._ctrlTool == 2:

                    # CRUTCH tool action

                self.moveTo(self._needX, self._needY, self._needZ, self._needR)

        if specialValue == 0:
            self._ctrlMode = 1

        if specialValue == 1:
            self.pointInput(dataList)

        if specialValue == 2:
            self.setSetting(dataList)

        if specialValue == 3:
            self.specialPack(dataList[1])

        if self._ctrlMode == 1:
            self._realTime = False


########################################################################################################################

port = 9093
ip = "192.168.1.118"

logging.info("Server started!")

dobotMagic = Dobot()

while True:

    conn, addr = create_server(ip, port).accept()

    logging.info("connect CU with IP - " + str(addr[0]) + " and port -" + str(addr[1]))

    try:

        while True:

            dobotMagic.changePos()
            data = conn.recv(1024).decode()

            if not data:
                break

            logging.info("CU -> Dobot :    " + str(data))

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