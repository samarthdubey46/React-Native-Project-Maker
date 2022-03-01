import argparse

class Main:
    def __init__(self, layout_file_path):
        self.isExpo = False
        self.project_name = ''
        self.project_path = ''
        self.layout_file_path = layout_file_path

    def ask_info(self):
        self.isExpo = input('Is this an Expo project? (y/n) ') == 'y'
        self.project_path = input('Enter the project path: ')
        self.project_name = input('Project name: ')



parser = argparse.ArgumentParser(description='Generate React Native project')
parser.add_argument('-p', '--path', help='Layout path', required=True)
