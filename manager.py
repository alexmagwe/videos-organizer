from video import Video
import os,sys,pickle
from gui import Gui

class Manager:
    maxtasks=5
    types={'video':['.avi','.mkv','.mpeg4','.ts'],'documents':['pdf','docx','xlsx','txt'],'music':['mp3','m4a']}
    def __init__(self,filetype='video'):
        self.filetypes=self.types[filetype]
        self.files=[]
        self.setup()
        self.getVideos()
    def setup(self):
        try:
            with open('setup.pkl','rb') as f:
                data=pickle.load(f)
                print(data)
                self.downloadfolder,self.moviespath,self.seriespath=data.get('dlpath'),data.get('moviespath'),data.get('seriespath')
        except FileNotFoundError:
            self.getSetup()
            self.setup()
    def getSetup(self):
            self.startGui()
            with open('setup.pkl','wb') as f:
                pickle.dump(self.values,f)
    def startGui(self):
        gui=Gui()
        while True:
            event,values=gui.window.read()
            if event is None:
                break
            if event=='FINISH':
                print(values)
                if values['ORIGINPATH']!='' and values['MOVIESPATH']!='' and values['SERIESPATH']!='':
                    error=False
                    for key,val in values.items():
                        if os.path.exists(val):
                            continue
                        else:
                            error=True
                            gui.window.FindElement('INFO').Update(f'{key} not found')
                    if not error:
                        self.values=values
                        break
        
        
    # sort videos into movies and series
    def getVideos(self):
        for root,dirs,files in os.walk(self.downloadfolder):
            for file in files:
                name,ext=os.path.splitext(file)
                if ext in self.filetypes:
                    self.files.append(Video(os.path.join(root,file)))
        return self.files
    def sortVideos(self):
        pass
        
        
    def createTasks(self):
        pass
    def startTasks(self):
        pass
        
if __name__=='__main__':
    m=Manager()
    
        
        
    
    
    
    
    
    
    