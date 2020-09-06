import PySimpleGUI as sg
import os
class Gui:
    def __init__(self):
        self.layout=[[sg.Text('LETS SETUP SOME STUFF')],[sg.Text('',key='INFO',size=(20,1),text_color='red')],[sg.Text('origin folder',size=(10,1)),
                    sg.Input(size=(40,1),key='dlpath'),sg.FolderBrowse('browse',key='ORIGINPATH')],
                    [sg.Text('Movies folder',size=(10,1)),sg.Input(size=(40,1),key='moviespath'),sg.FolderBrowse('browse',key='MOVIESPATH')],
                    [sg.Text('Series folder',size=(10,1)),sg.Input(size=(40,1),key='seriespath'),sg.FolderBrowse('browse',key='SERIESPATH')],
                    [sg.Button('finish',key='FINISH')]]
        self.window=sg.Window('Setup',self.layout)
        

        