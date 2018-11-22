import socket
import logging
import time

logging.basicConfig(level=logging.DEBUG, format=r"%(asctime)s - %(filename)s:%(lineno)d [%(levelname)s]: %(message)s")


def create_server(ip_in: str, port_in: int):
    sock = socket.socket()
    sock.bind((ip_in, port_in))
    sock.listen(1)
    return sock



# class Point:
#TODO write this class
# it is Queue
# clear()
# add()
# delete()
# atributes: x y z r speed ctrltool


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
        self._coordSys = 0
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

        # dType.SetPTPCmd(api, self._ptpMode, x, y, z, r)

    def changePos(self):
        
        # self._curPosX, self._curPosY, self._curPosZ, self._curPosJ1, self._curPosJ2, self._curPosJ2, self._curPosJ3,\ self._curPosJ4 = map(dType.GetPose(api))

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

    def robotMoving(self):

        eps = 0.2

        self.changePos()
        a = [self._curPosJ1, self._curPosJ2, self._curPosJ3, self._curPosJ4]
        self.changePos()

        if (abs(self._curPosJ1 - a[0]) < eps) or (abs(self._curPosJ2 - a[1]) < eps) or (abs(self._curPosJ3 - a[2]) < eps) or (abs(self._curPosJ4 - a[3]) < eps):

            logging.debug("Dobot moving")
            return True

        else:

            logging.debug("Dobot don't moving")
            return False

    def stopRobot(self):

        logging.debug("Dobot stop")

        self.changePos()
        # dType.SetPTPCmd(api, 2, self._curPosX, self._curPosY, self._curPosZ, self._curPosR)

    def pointInput(self, listIn):

        xIn, yIn, zIn, rIn, speedIn, ctrlIn = listIn[1], listIn[2], listIn[3], listIn[4], listIn[5], listIn[6]

        logging.info("CU -> Dobot: ", data)
        # TODO check position
        if True and speedIn > 0 and ctrlIn > -1:

            logging.debug("Point is correct")

            self._needX, self._needY, self._needZ, self._needR = xIn, yIn, zIn, rIn
            self._speed = speedIn
            self._ctrlTool = ctrlIn

            if ctrlIn == 1:

                self._ctrl = 1

        else:

            logging.debug("Point is incorrect. It was ignored.")

    def setsetting(self, listIn):

        ptpModeIn, whatRetIn, epsIn, numIterIn, ctrlIn = listIn[1], listIn[2], listIn[3], listIn[4], listIn[5]

        if (ptpModeIn > -1) and (ptpModeIn < 10):

            logging.debug("PtpMode correct")

            if (ptpModeIn > 2) and (ptpModeIn < 7):
                self._coordSys = 0
            else:
                self._coordSys = 2

            self._ptpMode = ptpModeIn

        else:
            logging.warning("PtpMode incorrect")

        if (whatRetIn> -1) and (whatRetIn < 5):

            logging.debug("WhatReturn correct")
            self._whatReturn = whatRetIn

        else:
            logging.warning("WhatReturn incorrect")

        if epsIn >= 1:

            logging.debug("Epsilon correct")
            self._epsilon = epsIn

        else:
            logging.warning("Epsilon incorrect")

        if numIterIn > 0:

            logging.debug("NumberIteration correct")
            self._numberIteration = numIterIn

        else:
            logging.warning("NumberIteration incorrect")

        if ctrlIn > -1:

            logging.debug("Ctrl correct")
            self._ctrl = ctrlIn

        else:
            logging.warning("Ctrl incorrect")


    def specialPack(self, ctrlIn, sock):

        if ctrlIn == 1:

            self._ctrl = 1

        elif ctrlIn == 2:

            self.printPosSocketWorld(sock)

        elif ctrlIn == 3:

            self.printPosSocketJoint(sock)
        else:
            logging.warning("Wrong ctrl param")


        #... and other special function robot

    def distanceToPoint(self):

        self.changePos()

        if self._coordSys == 2:

            distance = ((self._needX - self._curPosX)**2 + (self._needY - self._curPosY)**2 + (self._needZ - self._curPosZ)**2)**(1/2)

            logging.debug("Distance to Point = ", distance)

            return  distance

        if self._coordSys == 0:

            distance = ((self._needX - self._curPosJ1)**2 + (self._needY - self._curPosJ2)**2 + (self._needZ - self._curPosJ3)**2)**(1/2)

            logging.debug("Distance to Point", distance)

            return  distance

        logging.error("Wrong system coord")

        return -1

    def TimeMode(self, sock):

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

                logging.debug("Dobot stopped at that moment")

                if self._whatReturn == 3:
                    self.printPosSocketWorld(sock)

                if self._whatReturn == 4:
                    self.printPosSocketJoint(sock)

                '''
                    tool action: open, close, relax
                '''

            if (self._moveNow and self._realTime) or (self._moveNow and not self._realTime and self.distanceToPoint() < self._epsilon):

                self._moveNow = False
                self._stopNow = True

                logging.info("Dobot moving in Point = (", self._needX, " , ", self._needY, ", ",  self._needZ, ", ", self._needR, ")")

                # CRUTCH
                self._toolValue = self._ctrlTool
                # CRUTCH

                if self.robotMoving() and self._realTime:

                    logging.debug("Dobot stopped at that moment")

                    self.stopRobot()

                    if self._whatReturn == 3:
                        self.printPosSocketWorld(sock)

                    if self._whatReturn == 4:
                        self.printPosSocketJoint(sock)

                    self.moveTo(self._needX, self._needY, self._needZ, self._needR)

                    #TODO class point and functions for it

                else:

                    if self._whatReturn == 1:
                        self.printPosSocketWorld(sock)

                    if self._whatReturn == 2:
                        self.printPosSocketJoint(sock)

                    if self._ctrlTool == 2:

                    # CRUTCH tool action

                    #TODO read about tool-functions in DobotAPI

                    self.moveTo(self._needX, self._needY, self._needZ, self._needR)

        if specialValue == 0:
            self._ctrlMode = 1

        if specialValue == 1:
            self.pointInput(dataList)

        if specialValue == 2:
            self.setSetting(dataList)

        if specialValue == 3:
            self.specialPack(dataList[1], sock)

        if self._ctrlMode == 1 and self._realTime:
            logging.info("Swap Mode RealTime to NoRealTime")
            self._realTime = False

        if self._ctrlMode == 1 and not self._realTime:
            logging.info("Swap Mode NoRealTime to RealTime")
            self._realTime = True

    def okay(self):

        if self._ctrl == 1:
            return False
        else:
            return True

########################################################################################################################

port = 9093
ip = "192.168.1.118"

logging.info("Server started!")

dobotMagic = Dobot()

while True:

    conn, addr = create_server(ip, port).accept()

    logging.info("connect CU with IP - " + str(addr[0]) + " and port -" + str(addr[1]))

    try:

        '''
        dobotMagic.changePos()
        data = conn.recv(1024).decode()

        if not data:
            break

        logging.info("CU -> Dobot :    " + str(data))

        x, y, z, r = map(int, data.split())

        dobotMagic.moveTo(x, y, z, r)

        timeBefore = time.time()'''

        while True:

            dobotMagic.changePos()
            dobotMagic.TimeMode(conn)

            if dobotMagic.okay():
                break

    except:

        logging.error("Error! Connect aborted by exception")

    logging.info("Connection aborted CU")

    conn.close()