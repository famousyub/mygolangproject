

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
        self.number_line=0
       
        self.rep_logs = "C:\\Users\\g702306\\Desktop\\testy000\\formationpython\\data"
        self.fichiers = [f for f in os.listdir(self.rep_logs) if f.endswith('.log')]
        self.regex = r"R(\d+)"
    
        self._join = os.path.abspath(os.path.join(self.rep_logs, self.fichiers[1]))
    
        
        
        
        
    def  chack(self,syn,data):
        j=" ".join([syn,data])
        
        
        if  self.sentexte.find(syn) == -1 :
            f = [syn,data]
            j = " ".join(self.sentexte)
            f"{j}".join(f)
            return False  ,  j
        return True ,j
    
    
    def extrateData(self, log, tags  ,  ser):
        with open(self._join , "rb") as f : 
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
                n_p = s_line.count('\n')
            
            
                if s_line =='\n' or  s_line =='\r'  or  s_line =='\r\n' or s_line.find('\r') != -1 or s_line.find('\n') != -1 :
                    number_line+=1
                
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
                ten = "Mesure <M_CONS_CONSUMPTION>"
                fi0 = Finder(s_line,ten)
                check0 ,h0  = fi0.chack("Mesure <M_CONS_CONSUMPTION>               : Mesure Consommation - Status 0","status0")
            
                if check0 ==True :
                    print(f'0 {h0} -  {check0}')
                    f_ = f.seek(f.tell())
                    print(f_)
                    print(number_line)
                    print(s_line)
                
                    last_pos = f.tell()
                
                    last_pos += 4
                
                    f.seek(last_pos)
                    line2 = f.readline()
                
                    s_line_mesured    = line2.decode('ISO-8859-1') 
                    fg = s_line_mesured.split(' ')
                    fg = [i   for i in fg  if i !='']
                    print(fg)
                
                    with open('M_CONS_CONSUMPTION.txt','w+') as temp :
                        temp.write('\n')
                        temp.write(f' M_CONS_CONSUMPTION : > {fg[0]} W')