import cv2
import numpy as np
import sys
import time
from PyQt5.QtGui import*
from PyQt5.QtWidgets import*
from PyQt5.uic import*
from PyQt5.QtCore import*
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import*
import requests


# ui handel

ui,_=loadUiType('hologram.ui')


class mainApp(QMainWindow,ui):
    def __init__(self):
        super(mainApp,self).__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handel_ui()
        self.Handel_button()
          
    def handel_ui(self):
        self.videoOutput = self.MakeVideoWidget()
        self.mediaPlayer = self.MakeMediaPlayer()   
        
    def Handel_button(self):
        
        self.startButton.clicked.connect(self.Make_Hologram) 
        self.openButton.clicked.connect(self.onActionopenTriggered)
        self.playButton.clicked.connect(self.mediaPlayer.play)
        self.pauseButton.clicked.connect(self.mediaPlayer.pause)
        self.stopButton.clicked.connect(self.mediaPlayer.stop)
    
    def MakeMediaPlayer(self):
        
        self.mediaPlayer=QMediaPlayer(self)
        self.mediaPlayer.setVideoOutput(self.videoOutput)
        
        return self.mediaPlayer
    
    def MakeVideoWidget(self):
    
        videoOutput =QVideoWidget(self)
        vbox = QVBoxLayout()
        vbox.addWidget(videoOutput)
        self.VideoWidget.setLayout(vbox)
        return videoOutput
    
    
    def handel_ui(self):
        self.videoOutput = self.MakeVideoWidget()
        self.mediaPlayer = self.MakeMediaPlayer()
       
    
    def onActionopenTriggered(self):
    
        path=QFileDialog.getOpenFileName(self,'OpenFile',"/")
        
        filepath = path[0]
        if filepath== "":
            
            return
        
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filepath)))
        self.mediaPlayer.play()
        
###################################################################################################        
        
    def Make_Hologram(self):
        
        
        self.GifUrl = self.lineEdit.text()
        self.gif_url =cv2.VideoCapture(self.GifUrl)
        self.saveFile = self.lineEdit_2.text()
        self.forcc = cv2.VideoWriter_fourcc('W','M','V','2')
        self.output = cv2.VideoWriter(self.saveFile,self.forcc, 11.5, (750,750))

        
        count = 0

        while (True):
            


            ret,self.frame = self.gif_url.read()
            
            if ret == True:
                
                
                
                count +=1
                time.sleep(0.1)
                #create picture with matrix
                self. out= np.zeros((750,750,3),np.uint8)
                #image = cv2.imread('4.jpeg')
                self.frame = cv2.resize(self.frame,(200,200))
                #top image
                self.top =np.copy(self.frame[:200,:200,:])

                self.out[10:210,270:470, :]=self.top
                #left image
                self.left = np.copy(self.frame[:200,:200,:])
                rows,columns,channels = self.left.shape
                self.r = cv2.getRotationMatrix2D((columns/2,rows/2),90,1)
                self.out1=cv2.warpAffine(self.left,self.r,(columns,rows))
                self.out[250:450,20:220, :]=self.out1
                #right image
                self.right = np.copy(self.frame[:200,:200,:])
                rows,columns,channels = self.right.shape
                self.r = cv2.getRotationMatrix2D((columns/2,rows/2),270,1)
                self.out2=cv2.warpAffine(self.right,self.r,(columns,rows))
                self.out[250:450,530:730, :]=self.out2
                #down image 
                self.down = np.copy(self.frame[:200,:200,:])
                rows,columns,channels = self.down.shape
                self.r = cv2.getRotationMatrix2D((columns/2,rows/2),180,1)
                self.out3=cv2.warpAffine(self.down,self.r,(columns,rows))
                self.out[490:690,274:474, :]=self.out3 
                self.output.write(self.out)
                cv2.imshow('hologram',self.out)
                if cv2.waitKey(60)== ord('q'):
                    break
            else:
                break
                    
        self.gif_url.release()
        self.output.release()
        cv2.destroyAllWindows()
    
       
        
        
        
        
def main():
    app=QApplication(sys.argv)
    window=mainApp()
    window.show()
    app.exec_()
    
if __name__=="__main__":
    main()
