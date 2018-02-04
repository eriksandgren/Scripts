#!/usr/bin/python
import os
import operator
class file():
    def __init__(self, name, size):
        self.name = name
        self.size = size
    def display(self):
        if self.size > (10 ** 9):
            print '{0:100} {1:10d} GB'.format(self.name, self.size / (10 ** 9))
        elif self.size > (10 ** 6):
            print '{0:100} {1:10d} MB'.format(self.name, self.size / (10 ** 6))
        elif self.size > (10 ** 3):
            print '{0:100} {1:10d} KB'.format(self.name, self.size / (10 ** 3))
        else:
            print '{0:100} {1:10d} byte'.format(self.name, self.size)

files = []

def check_folder(folder):
  inFolder = os.listdir(folder)
  for item in inFolder:
      full_path = folder + "/" + item
      try:
        info = os.stat(full_path)
      except OSError:
        continue
      if os.path.isfile(full_path):
          files.append(file(name=full_path, size=info[6]))
      elif os.path.isdir(full_path):
          check_folder(full_path)

# Recursively go through all subfolders and add all files to list
check_folder(".")

# Sort the list of files
files.sort(key=operator.attrgetter('size'), reverse=True)
for file in files[:20]:
    file.display()