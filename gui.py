import sys
try:
    import PySimpleGUI as sg
except ImportError:
    print(' Please run pip install PySimpleGUI')
    sys.exit()
import os
class Gui:
    def __init__(self):
        self.layout=[[sg.Text('LETS SETUP SOME STUFF')],[sg.Text('',key='INFO',size=(20,1),text_color='red')],[sg.Text('enter default downloads dolder')],
        [sg.Text('Download folder',size=(10,1)),sg.Input(size=(40,1),key='dlpath'),sg.FolderBrowse('browse',key='ORIGINPATH')],
        [sg.Text('enter the videos folder inside downloads')],
        [sg.Text('Video downloads folder',size=(10,1)),sg.Input(size=(40,1),key='dv_path'),sg.FolderBrowse('browse',key='DOWNLOAD_VIDEOS_PATH')],
        [sg.Text('enter the root folder path where you want Movies stored in',size=(50,1))],
        [sg.Text('Movies folder',size=(10,1)),sg.Input(size=(40,1),key='moviespath'),sg.FolderBrowse('browse',key='MOVIESPATH')],
        [sg.Text('enter the root folder path where you want Series stored in',size=(50,1))],
        [sg.Text('Series folder',size=(10,1)),sg.Input(size=(40,1),key='seriespath'),sg.FolderBrowse('browse',key='SERIESPATH')],
        [sg.Button('finish',key='FINISH')]]
        self.window=sg.Window('Setup',self.layout)
        

        
