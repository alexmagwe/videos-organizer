from video import Video, Series, Movie
import os
import sys
import pickle
import shutil
import sys
import re
from collections import deque
from gui import Gui
try:
    from fuzzywuzzy import process
except ImportError:
    print('fuzzywuzzy required install it with pip install fuzzywuzzy')
    sys.exit()
import threading


class Manager:
    maxtasks = 5
    types = {'video': ['.avi', '.mkv', '.mp4', '.mpeg4'], 'documents': [
        'pdf', 'docx', 'xlsx', 'txt'], 'music': ['mp3', 'm4a']}

    def __init__(self, filetype='video'):
        self.filetypes = self.types[filetype]
        self.files = []
        self.jobs = deque()
        self.movedfiles = 0
        self.failed = []

    def run(self):
        self.setup()
        self.getSeriesFolders()
        self.getVideos()
        self.sortVideos()
        self.get_destinations()
        self.createTasks()
        self.startTasks()
        self.cleanUp()

    def stageMovies(self):
        pass

    def stageSeries(self):
        pass

    @staticmethod
    def createNewFolder(path):
        try:
            os.mkdir(path)
            return True
        except Exception as e:
            print(f'ERROR CREATING FOLDER {path} ', sys.exc_info()[0])
            return False

    def getSeriesFolders(self):
        folders = []
        for _, dirs, _ in os.walk(self.seriespath):
            folders.append(dirs)
            break
        self.seriesfolders = folders[0]

    def setup(self):
        data = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'setup.pkl')
        try:
            with open(data, 'rb') as f:
                data = pickle.load(f)
                self.downloadfolder, self.moviespath, self.seriespath,self.download_videos_folder = data.get(
                    'dlpath'), data.get('moviespath'), data.get('seriespath'),data.get('dv_path')
        except FileNotFoundError:
            self.getSetup()
            self.setup()

    def getSetup(self):
        self.startGui()
        with open('setup.pkl', 'wb') as f:
            pickle.dump(self.values, f)

    def startGui(self):
        gui = Gui()
        while True:
            event, values = gui.window.read()
            if event is None:
                break
                sys.exit()
            if event == 'FINISH':
                print(values)
                if values['ORIGINPATH'] != '' and values['MOVIESPATH'] != '' and values['SERIESPATH'] != '' and values['DOWNLOAD_VIDEOS_PATH'] != '':
                    error = False
                    for key, val in values.items():
                        if os.path.exists(val):
                            continue
                        else:
                            error = True
                            gui.window.FindElement(
                                'INFO').Update(f'{key} not found')
                    if not error:
                        self.values = values
                        break
                else:
                    sys.exit()

    # sort videos into movies and series

    def getVideos(self):
        for root, dirs, files in os.walk(self.downloadfolder):
            for file in files:
                name, ext = os.path.splitext(file)
                if ext in self.filetypes:
                    self.files.append(Video(os.path.join(root, file)))
        return self.files

    def sortVideos(self):
        series = list(filter(lambda video: video.is_a_series, self.files))
        self.series = list(map(lambda eps: Series(eps.path), series))
        movies = list(filter(lambda video: video.is_a_movie, self.files))
        self.movies = list(map(lambda movie: Movie(movie.path), movies))

    def findDestination(self, eps):

        bestmatch = process.extractOne(eps.name, self.seriesfolders)
        if bestmatch and bestmatch[1] >= 90:
            foldername = bestmatch[0]
            path = os.path.join(self.seriespath, foldername, eps.season)
            if os.path.exists(path):
                return path
            else:
                created = Manager.createNewFolder(path)
                if created:
                    return path
                else:
                    return False

        else:
            path = os.path.join(self.seriespath, eps.name)
            created = Manager.createNewFolder(path)
            print('created ', created)
            if created:
                seasonpath = (os.path.join(path, eps.season))
                result = Manager.createNewFolder(seasonpath)
                self.seriesfolders.append(path)
                if result:
                    return seasonpath
        return False

    def get_destinations(self):
        for movie in self.movies:
            movie.destination = self.moviespath
        for eps in self.series:
            path = self.findDestination(eps)
            if path:
                eps.setDestination(path)
            else:
                path = os.path.join(self.seriespath, eps.name, eps.season)
                if not os.path.exists(path):
                    created = Manager.createNewFolder(path)
                if created:
                    eps.setDestination(path)
                else:
                    print('could not create folder')
                    return

    def createTasks(self):
        print(len(self.series), ' episodes found')
        print(len(self.movies), ' movies found')

        if len(self.movies) > 0:
            for file in self.movies:
                self.jobs.append(threading.Thread(
                    target=self.worker, args=[file, ]))
        if len(self.series) > 0:
            for eps in self.series:
                self.jobs.append(threading.Thread(
                    target=self.worker, args=[eps, ]))

    def worker(self, job):
        try:
            print(f'moving {job.name} to {job.destination}')
            shutil.move(job.path, job.destination)
            self.movedfiles += 1
        except PermissionError:
            self.failed.append((job, sys.exc_info()[0]))
        except:
            self.failed.append((job, sys.exc_info()[0]))

    def startTasks(self):
        total = len(self.jobs)
        if total > 0:
            for job in self.jobs:
                job.start()
            for job in self.jobs:
                job.join()
            print(f'{self.movedfiles}/{total} files moved succesfully')

        if total != self.movedfiles:
            print(f"failed:\n{self.failed}")
            return

    def cleanUp(self):
        #deletes the folders left behind if any only
        if len(self.movies) > 0 or len(self.series) > 0:
            print(f'running clean up...')
        if len(self.movies) > 0:
            for movie in self.movies:
                parent_folder = movie.path.split('/')[-1]
        if len(self.series) > 0:
            for series in self.series:
                parent_folder = '/'.join(series.path.split('/')[:-1])
                if parent_folder != self.downloadfolder and  parent_folder!=self.download_videos_folder:
                    try:
                        print(parent+folder)
                        shutil.rmtree(parent_folder)
                    except Exception as e:
                        print(e)
                        return
                
