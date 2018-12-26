#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
import os
class Files:
    def __init__(self):
        pass
    
    def file_save(self, file_name, contents):
        
        file_name = file_name + ".txt"
    
        
        if os.path.exists(file_name):
            f = open(file_name, 'a')
            f.write(contents+"\n")
        else :
            f = open(file_name, 'w')
            f.write(contents+"\n")
            f.close()
        pass

    def file_read(self, file_name):
        file_name = file_name + ".txt"
        if os.path.exists(file_name):
            f = open(file_name, 'r')
            while True:
                line = f.readline()
                if not line: break
                line2 = line
            f.close()
            return line2
        return "0"
    
    def file_overwrite_save(self,file_name, contents):
        file_name = file_name + ".txt"
        f = open(file_name, 'w')
        f.write(contents+"\n")
        f.close()
    
    def file_exist(self,file_name):
        file_name = file_name + ".txt"
        if os.path.exists(file_name):
            return True
        else :
            return False
    
    def file_remove(self,file_name):
        file_name = file_name + ".txt"
        if os.path.exists(file_name):
            os.remove(file_name)
            return True
        else :
            return False