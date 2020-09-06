import platform
import os
class Video:
    minmovielength=75
    def __init__(self,path):
        self.path=path
        self.getSize()
    def __repr__(self):
        return f'{self.getName()} is a movie {self.is_a_movie()}'
        
    def getName(self):
        if platform.system()=='Windows':
            self.name=self.path.split('\\')[-1]

            
        elif platform.system()=='Linux':        
            self.name=self.path.split('/')[-1]
        return self.name
    def getSize(self):
        self.size=os.stat(self.path).st_size//1000000
        return self.size
    def is_a_movie(self):
        if self.size>750:
            return True
        else:return False