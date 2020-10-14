import platform
import os
import re
class Video:
    minmovielength=75
    def __init__(self,path):
        self.path=path
        self.getSize()
        self.getName()
    def __repr__(self):
        return f'{self.getName()}'
    @staticmethod
    def find_name_match(name):
        pattern=r'([s|S][0-9][0-9][e|E][0-9][0-9])'
        match=re.search(pattern,name)
        return match
        
    def getName(self):
        if platform.system()=='Windows':
            self.name=self.path.split('\\')[-1]

            
        elif platform.system()=='Linux':        
            self.name=self.path.split('/')[-1]
        return self.name
    def getSize(self):
        self.size=os.stat(self.path).st_size//1000000
        return self.size
    @property
    def is_a_movie(self):
        if self.size>750:
            return True
        else:return False
    @property
    def is_a_series(self):
        match=self.find_name_match(self.name)
        if match:
            return True
        else: return False
