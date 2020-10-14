from video import Video
import os,sys,pickle,shutil,sys
from gui import Gui
from fuzzywuzzy import process
import threading
class Manager:
    maxtasks=5
    types={'video':['.avi','.mkv','.mpeg4'],'documents':['pdf','docx','xlsx','txt'],'music':['mp3','m4a']}
    def __init__(self,filetype='video'):
        self.filetypes=self.types[filetype]
        self.files=[]
        self.setup()
        self.getSeriesFolders()
        self.getVideos()
        self.sortVideos()
        self.get_destinations()
    
    def stageMovies():
        pass
    def stageSeries():
        pass
    
    def createNewFolder(path):
        try:
            os.mkdir(path)
            return True
        except Exception as e:
            print(sys.exc_info()[0])
            return False
    
    def findDestination(self,name):
        bestmatch=process.extractOne(name,self.seriesfolders) 
        foldername=bestmatch[0]
        percentagematch=bestmatch[1]
        print (name,' matches the folder ',foldername, 'by ',percentagematch,"%\n",)
        if percentagematch>=90:
            return os.path.join(self.seriespath,foldername)
        else:return False

            
   
    def getSeriesFolders(self):
        folders=[]
        for _,dirs,_ in os.walk(self.seriespath):
            folders.append(dirs)
            break
        self.seriesfolders=folders[0]
        print(self.seriesfolders)

    def setup(self):
        try:
            with open('setup.pkl','rb') as f:
                data=pickle.load(f)
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
        self.movies=list(filter(lambda video:video.is_a_movie,self.files))
        self.series=list(filter(lambda video:video.is_a_series,self.files))
        print('series:',self.series)
        
    def get_destinations(self):
        for video in self.files:
            if video.is_a_movie:
                self.destination=self.moviespath
            elif video.is_a_series:            
                match=Video.find_name_match(video.name)
                video.series_name=video.name[:match.start()-1]
                path=self.findDestination(video.series_name)
                if path:
                    self.destination=path
                else:
                    path=os.path.join(self.seriespath,video.series_name)
                    if not os.path.exists(path):
                        created=Manager.createNewFolder(path)
                    if created:
                        print(f'created new folder {video.name}')
                        self.getSeriesFolders()
                        self.get_destinations()
                    else:
                        print('ould not create folder')
                        return
                
    def createTasks(self):
        pass

    def startTasks(self):
        pass
        
if __name__=='__main__':
    m=Manager()
    
        
        
    
    
    
    
    
    
    
