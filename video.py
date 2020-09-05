import platform
import os
import subprocess
import moviepy.editor

class Video:
    minmovielength=75
    def __init__(self,path):
        self.path=path
        self.getLength()
        self.getSize()
        self.is_a_movie()
        
    def getName(self):
        if platform.system()=='Windows':
            self.name=self.path.split('\\')[-1]
            
        elif platform.system()=='Linux':        
            self.name=self.path.split('/')[-1]
        return self.name
    def getSize(self):
        self.size=os.stat().st_size//1000000
        return self.size
    def is_a_movie(self):
        if self.size>750 & self.duration<minmovielength:
            return True
        else:return False
    def getLength(self):
        video=moviepy.editor.VideoFileClip(self.path)
        self.duration=video.length//60
        return self.duration
    