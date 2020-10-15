import platform
import os
import re
class Video:
    minmovielength=75
    def __init__(self,path):
        self.path=path
        self.size=self.getSize()
        self.name=self.getName()
    def __repr__(self):
        return f'{self.getName()}'
    def getName(self):
        if platform.system()=='Windows':
            name=self.path.split('\\')[-1]            
        elif platform.system()=='Linux':        
            name=self.path.split('/')[-1]
        return name
    def getSize(self):
        self.size=os.stat(self.path).st_size//1000000
        return self.size
        
    def getIndex(self,name):
        pattern=r'([s|S][0-9][0-9][e|E][0-9][0-9])'
        match=re.search(pattern,name)
        return match
    
    @property
    def is_a_movie(self):
        if self.size>750:
            return True
        else:return False
    
    @property
    def is_a_series(self):
        match=self.getIndex(self.name)
        if match:
            return True
        else: return False
        
    def setDestination(self,destination):
        self.destination=destination
class Movie(Video):
    def __init__(self,path):
        super().__init__(path)
 
class Series(Video):
    def __init__(self,path):
        super().__init__(path)
        self.index=self.getIndex(self.name)
        self.name=self.setName()
        self.season=self.setSeason()
        self.episode_number=self.setEpisode()
    
        
    def setName(self):
        name=self.name[:self.index.start()-1]
        return name
        
    def setSeason(self):
        season=self.index.group()[:3]
        return season
        
    def setEpisode(self):
        episode_number=self.index.group()[-2:]
        return episode_number
    
        

        
        
