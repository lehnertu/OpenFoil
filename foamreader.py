import sys, re
import numpy as np

"""
This is a wrapper for a file
which removes all C-style comments ( '//' and '/*'-'*/' ).
"""
class CommentedFile:
    def __init__(self, f):
        self.f = f
    """
    deliver the next line which is not empty, not a single-line comment
    and not part of a multi-line comment
    """
    def next(self):
        found = False               # whether we found a valid content line
        multi = False               # whether we are in a multi-line comment
        while not found:
            line = self.f.__next__()
            if line.strip() == '': continue
            if '/*' in line: multi = True
            if multi:
                found = False
                if '*/' in line: multi = False
            else:
                found = True
            if line.startswith('//'): found = False
        return line
    def __iter__(self):
        return self

class FoamFile:
    def __init__(self, path):
        self.path = path
    def readHeader(self):
        line = self.fc.next()
        while not 'FoamFile' in line:
            line = self.fc.next()
        line = self.fc.next()
        if not '{' in line: raise Exception('file %s - header start not found' % path)
        line = self.fc.next()
        while not '}' in line:
            strings = line.split()
            if strings[0] == 'object': self.object = strings[1]
            line = self.fc.next()
        if not '}' in line: raise Exception('file %s - header end not found' % path)
    def readPoints(self):
        self.f = open(self.path,'r')
        self.fc = CommentedFile(self.f)
        self.readHeader()
        if not 'points' in self.object: raise Exception('file %s does not describe a points object' % path)
        line = self.fc.next()
        nop = int(line)
        # print('reading %d points' % nop)
        line = self.fc.next()
        if not '(' in line: raise Exception('file %s - data block start not found' % path)
        pts = []
        for i in range(nop):
            line = self.fc.next()
            line = line.replace('(','')
            line = line.replace(')','')
            pt = np.fromstring(line, dtype=float, sep=' ')
            pts.append(pt)
        line = self.fc.next()
        if not ')' in line: raise Exception('file %s - data block end not found' % path)
        return np.array(pts)            
    def readFaces(self):
        self.f = open(self.path,'r')
        self.fc = CommentedFile(self.f)
        self.readHeader()
        if not 'faces' in self.object: raise Exception('file %s does not describe a facess object' % path)
        line = self.fc.next()
        nof = int(line)
        # print('reading %d faces' % nof)
        line = self.fc.next()
        if not '(' in line: raise Exception('file %s - data block start not found' % path)
        quads = []
        for i in range(nof):
            line = self.fc.next()
            line = line.replace('(',' ')
            line = line.replace(')',' ')
            face = np.fromstring(line, dtype=int, sep=' ')
            if face[0] == 4:
                quads.append(face[1:5])
        line = self.fc.next()
        if not ')' in line: raise Exception('file %s - data block end not found' % path)
        return np.array(quads, dtype=int)            
        
ff = FoamFile('run/alfa200/constant/polyMesh/points')
point_data = ff.readPoints()
print(len(point_data))
print(point_data)

ff = FoamFile('run/alfa200/constant/polyMesh/faces')
face_data = ff.readFaces()
print(len(face_data))
print(face_data)


