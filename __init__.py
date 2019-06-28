"""
Intercom Mycroft Skill.
"""
import pyaudio
import socket
import sys
import time
import threading
import json
from os.path import dirname
from adapt.intent import IntentBuilder
from os.path import join, dirname
from multiprocessing import Process
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.skills.context import *
from mycroft.util import read_stripped_lines
from mycroft.util.log import getLogger
from mycroft.messagebus.message import Message

__author__ = 'aix'
deviceName = "Aix-Laptop"
mute = True
deviceListObj = ""
voiceSoc = ""
deviceSoc = ""
audioStream = ""
voiceStream = ""

LOGGER = getLogger(__name__)

class IntercomSkill(MycroftSkill):
    def __init__(self):
        """
        Intercom Skill Class.
        """    
        super(IntercomSkill, self).__init__(name="IntercomSkill")

    def initialize(self):
        self.gui.register_handler('IntercomSkill.handleClientConnect',
                                  self.connectVoiceClient)
        self.gui.register_handler('IntercomSkill.handleClientDisconnect',
                                  self.disconnectVoiceClient)
        self.gui.register_handler('IntercomSkill.handleSpeakStart',
                                  self.speakStart)
        self.gui.register_handler('IntercomSkill.handleSpeakStop',
                                  self.speakStop)
        self.scanLocal()
        self.createPlayer()
        self.voiceServerT = threading.Thread(target=self.voiceServer)
        self.voiceServerT.start()
        self.client = ""
        self.speaking = False

    @intent_handler(IntentBuilder('handle_display_intercom_skill').require('intercom.show.devices'))
    def handle_display_intercom_skill(self, message):
        self.scanLocal()
        global deviceListObj
        self.gui["deviceScan"] = json.dumps(deviceListObj)
        self.gui.show_page("listdevices.qml", override_idle=True)

    # Scan Network For Valid Devices
    def scanLocal(self):
        deviceServerT = Process(target=self.deviceServer)
        deviceServerT.start()
        currentPath = dirname(__file__)
        sys.path.append(currentPath) 
        import nmscanner as nm
        deviceList = nm.check_own_subnet_for_open_port(50000)
        #print(deviceList)
        if deviceList:
            global deviceListObj
            deviceListObj = nm.discover_device_name(deviceList)
            print(deviceListObj)
            self.gui["deviceScan"] = json.dumps(deviceListObj)
            self.gui.show_page("listdevices.qml", override_idle=True)
        deviceServerT.terminate()
            #self.selectClient()

    # Start Voice Server
    def deviceServer(self):
        LOGGER.info("In deviceServer")
        currentPath = dirname(__file__)
        sys.path.append(currentPath) 
        import nmscanner as nm
        chunk = 1024
        host = nm.get_own_ip()
        port = 50000
        backlog = 4
        size = 1024
        global deviceSoc
        deviceSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            deviceSoc.bind((host,port))
        except:
            deviceSoc.shutdown(socket.SHUT_RDWR)
            deviceSoc.close()
            self.scanLocal()
        deviceSoc.listen(backlog)
        global deviceName
        while True:
            LOGGER.info(sys.stderr, 'waiting for a connection')
            client, address = deviceSoc.accept()
            if client:
                client.send(deviceName.encode("utf-8"))
        
        client.close()
    
    #Create AudioPlayer
    def createPlayer(self):
        paudio = pyaudio.PyAudio()
        global voiceStream
        voiceStream = paudio.open(format = pyaudio.paInt16,
                        channels = 1,
                        rate = 10240,
                        output = True)

    # Start Voice Server
    def voiceServer(self):
        currentPath = dirname(__file__)
        sys.path.append(currentPath) 
        import nmscanner as nm
        host = nm.get_own_ip()
        port = 50005

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host,port))
        sock.listen(5)
        while 1:
            conn, address = sock.accept()
            new_client = threading.Thread(target=self.clientThread, args=(conn,))
            new_client.start()
            
        sock.close 
        
    def clientThread(self, conn):
        message = "In ClientThread \n"
        conn.send(message.encode())
        
        while True:
            data = conn.recv(1024)
            if data:
                self.streamAudio(data)
            else:
                break
        
        conn.close()

    def streamAudio(self, data):
        global voiceStream
        if data:
            voiceStream.write(data)
        
    # Connect Voice Client
    def connectVoiceClient(self):
        LOGGER.info ("In vConnect")
        clientAddr = "192.168.1.119"
        LOGGER.info(clientAddr)
        chunk = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 10240
        p = pyaudio.PyAudio()
        global audioStream
        
        audioStream = p.open(format = FORMAT,
                        channels = CHANNELS,
                        rate = RATE,
                        input = True,
                        frames_per_buffer = chunk)

        # Socket Initialization
        host = clientAddr
        port = 50005
        size = 1024
        global voiceSoc
        voiceSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        voiceSoc.connect((host,port))
        LOGGER.info("In vConnect Complete")
  
    def disconnectVoiceClient(self):
        LOGGER.info("In vDisconnect Start")
        global voiceSoc
        voiceSoc.close()
        LOGGER.info("In vDisconnect Completed")
    
    def speakStart(self):
        global mute
        mute = False
        self.speak()

    def speakStop(self):
        global mute
        mute = True

    def speak(self):
        chunk = 1024
        size = 1024
        LOGGER.info ("You are now speaking")
        global voiceSoc
        global audioStream
        global mute
        print(voiceSoc)
        while mute is False:
            data = audioStream.read(chunk)  
            voiceSoc.send(data)

    def stop(self):
        """
        Mycroft Stop Function
        """
        pass
    
def create_skill():
    """
    Mycroft Create Skill Function
    """
    return IntercomSkill()
 
