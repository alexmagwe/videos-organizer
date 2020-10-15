from video import Video,Series,Movie
import os,sys,pickle,shutil,sys,re
from gui import Gui
from fuzzywuzzy import process
import threading
class Manager:
    maxtasks=5
    types={'video':['.avi','.mkv','.mp4','.mpeg4'],'documents':['pdf','docx','xlsx','txt'],'music':['mp3','m4a']}
    def __init__(self,filetype='video'):
        self.filetypes=self.types[filetype]
        self.files=[]
        self.setup()
        self.getSeriesFolders()
        self.getVideos()
        self.sortVideos()
        self.get_destinations()
        self.createTasks()
    
    def stageMovies():
        pass
        
    def stageSeries():
        pass
        
    @staticmethod
    def createNewFolder(path):
        try:
            os.mkdir(path)
            return True
        except Exception as e:
            print(sys.exc_info()[0])
            return False
    

    def getSeriesFolders(self):
        folders=[]
        for _,dirs,_ in os.walk(self.seriespath):
            folders.append(dirs)
            break
        self.seriesfolders=folders[0]

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
                    print(name)
        return self.files
        
    def sortVideos(self):
        movies=list(filter(lambda video:video.is_a_movie,self.files))
        print(movies)
        self.movies=list(map(lambda movie:Movie(movie.path),movies))
        series=list(filter(lambda video:video.is_a_series,self.files))
        self.series=list(map(lambda eps:Series(eps.path),series))
    
        
    def findDestination(self,eps):
        bestmatch=process.extractOne(eps.name,self.seriesfolders) 
        foldername=bestmatch[0]
        percentagematch=bestmatch[1]
        print (eps.name,' matches the folder ',foldername, 'by ',percentagematch,"%\n",)
        if percentagematch>=90:
            path=os.path.join(self.seriespath,foldername,eps.season)
            if os.path.exists(path):
                return path
            else:
                created=Manager.createNewFolder(path)
                if created:
                    return path
                else:
                    return False
                
        else:
            path=os.path.join(self.seriespath,foldername)
            created=Manager.createNewFolder(path)
            if created:
                seasonpath=(os.path.join(path,eps.season))
                result=Manager.createNewFolder(seasonpath)
                self.seriesfolders.apend(path)
                if result:
                    return seasonpath
        return False

    def get_destinations(self):
        for movie in self.movies:
            movie.destination=self.moviespath
        for eps in self.series:
            path=self.findDestination(eps)
            if path:
                eps.setDestination(path)
            else:
                path=os.path.join(self.seriespath,eps.name,eps.season)
                if not os.path.exists(path):
                    created=Manager.createNewFolder(path)
                if created:
                    eps.setDestination(path)
                else:
                    print('could not create folder')
                    return
                
    def createTasks(self):
        print(len(self.series),' episodes found')
        print(len(self.movies),' movies found')
        
        for file in self.movies:
            print(file.name,' : ',file.destination)
        for eps in self.series:
            print(eps.name,' : ',eps.destination)
        

    def startTasks(self):
        pass
        
if __name__=='__main__':
    m=Manager()
    
        
        
    
    
    
    
    
    
    
