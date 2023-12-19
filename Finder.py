# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 09:31:51 2023

@author: G702306
"""


import os 
import sys 
import re

regex = r"R(\d+)"
regex_mesure_tems = r'(\d+)  s'
dfa_pattern = re.compile(r'R(\d+)')
mesure_pattern = re.compile(regex_mesure_tems)
pattern_temp = r"(\d+) \\0b "
mesure_temperateure = ""

class Finder :
    
    
    def  __init__(self, sentexte , comparator_):
        
        self.sentexte = sentexte
        self.comparator_ = comparator_ 
        
        
    def  chack(self,syn,data):
        j=" ".join([syn,data])
        
        
        if  self.sentexte.find(syn) == -1 :
            f = [syn,data]
            j = " ".join(self.sentexte)
            f"{j}".join(f)
            return False  ,  j
        return True ,j
    
    
    

if __name__  =='__main__':
    fi = Finder("hello world how are you" ,   "how are you ")
    rep_logs = "C:\\Users\\g702306\\Desktop\\testy000\\formationpython\\data"
    fichiers = [f for f in os.listdir(rep_logs) if f.endswith('.log')]
    regex = r"R(\d+)"
    
    _join = os.path.abspath(os.path.join(rep_logs, fichiers[1]))
    
    lk = os.path
    check_ = fi.chack("how", "are you")
    print(check_)
    
    
    
    
    
    with open(_join , "rb") as f : 
        line = f.readline()
        print(type(line))
        s_line = line.decode('utf-8')
        res=''
        res2 =''
        
        print(type(s_line))
        print(s_line)
        idx = 0
        
        while line :
            idx += 1
            #s_line  = str(line.decode('latin-1').encode('utf-8'))
            s_line  = line.decode('ISO-8859-1')
            matches = re.finditer(regex, s_line, re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                for groupNum in range(0, len(match.groups())):
                    groupNum = groupNum + 1
                    res = match.group(groupNum)
            
            matches2 = re.finditer(regex_mesure_tems, s_line, re.MULTILINE)
            for matchNum2, match2 in enumerate(matches2, start=1):
                for groupNum2 in range(0, len(match2.groups())):
                    groupNum2 = groupNum2 + 1
                    res2 = match2.group(groupNum2)
        
            line_str =str( line)
            if idx ==1 :
                #print(type(line_str))
                pass
            fi2 =Finder(line_str,"===================> Lecture DFA <========================================================")
            check_ ,h= fi2.chack("LECTURE DFA", "DFA")
            line  = f.readline()
            if check_ ==True:
                print(f.tell())
                print(check_)
                print(h)
                print(f'R{res}')
                with open('dfa.txt','a+') as dfa :
                    dfa.write('dfa > \r\n')
                    dfa.write(f'dfa :  R{res} \n\r')
                    if res2 != '':
                        dfa.write("Mesure <M_DUREE_TEST_FCT>\r\n")
                        dfa.write(f" Mesure <M_DUREE_TEST_FCT> : {res2}")
            
        
            fi3 =Finder(line_str,"Mesure <M_DUREE_TEST_FCT>                 : Temps de test - Status 0")
        
            chech2 , h2 = fi3.chack("Mesure <M_DUREE_TEST_FCT>", "DUREE")
            
            if chech2 == True :
                print(idx)
                print(h2)
                print(f.tell())
               # f.next()
                #f.next()
                print(s_line)
        
        
    f.close()
    dfa.close()
                
                
                
            
            