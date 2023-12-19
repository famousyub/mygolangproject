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
    number_line=0
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
            if idx ==1 :
                #print(type(line_str))
                pass
            fi2 =Finder(s_line,"===================> Lecture DFA <========================================================")
            check_ ,h= fi2.chack("LECTURE DFA", "DFA")
            line  = f.readline()
            if check_ ==True:
                print(f.tell())
                
               
                print(f'R{res}')
                with open('dfa.txt','a+') as dfa :
                    dfa.write('dfa > \r\n')
                    dfa.write(f'dfa :  R{res} \n\r')
                    if res2 != '':
                        dfa.write("Mesure <M_DUREE_TEST_FCT>\r\n")
                        dfa.write(f" Mesure <M_DUREE_TEST_FCT> : {res2}")
                        res22 = ''
                        res22['M_DUREE_TEST_FCT'] =res2 
                        dfa.write(f' M_DUREE_TEST_FCT :  {res22["M_DUREE_TEST_FCT"]} ')
            
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
            
            
            
            
            ten00 = "Mesure <M_DEBIT_SENDER_ETH2>"
            fi00 = Finder(s_line,ten00)
            check00 ,h00  = fi0.chack("Mesure <M_DEBIT_SENDER_ETH2>               : Mesure Consommation - Status 0","status0")
            
            if check00 ==True :
                print(f'0 {h00} -  {check00}')
                f_1 = f.seek(f.tell())
                print(f_1)
                print(number_line)
                print(s_line)
                
                last_pos22 = f.tell()
                
                last_pos += 4
                
                f.seek(last_pos)
                line22 = f.readline()
                
                s_line_mesured    = line22.decode('ISO-8859-1') 
                fg00 = s_line_mesured.split(' ')
                fg00 = [i   for i in fg00  if i !='']
                print(fg00)
                
                print("********************")
                
                
                with open('M_DEBIT_SENDER_ETH2.txt','w+') as temp :
                    temp.write('\n')
                    temp.write(f' Mesure <M_DEBIT_SENDER_ETH2> : > {fg00[0]} W')
            
            
        
            fi3 =Finder(s_line,"Mesure <M_DUREE_TEST_FCT>                 : Temps de test - Status 0")
        
            chech2 , h2 = fi3.chack("Mesure <M_DUREE_TEST_FCT>", "DUREE")
            
            if chech2 == True :
                print(idx)
                print(h2)
                print(f.tell())
               # f.next()
                #f.next()
                print(s_line)
                
                
                
            fi3 =Finder(s_line,"Mesure <M_DEBIT_SENDER_ETH3>")
        
            chech2 , h2 = fi3.chack("Mesure <M_DEBIT_SENDER_ETH3>", "DUREE")
            
            if chech2 == True :
                print(idx)
                print(h2)
                print(f.tell())
               # f.next()
                #f.next()
                print(s_line)
            
            phrfindmesure = "Mesure <M_Temperature_Measured>           : la valeur de la temperature mesurée par capteur après calibration - Status 1"
            phi4 = Finder(s_line,phrfindmesure )
            
            ckeck4,h4 = phi4.chack("Mesure <M_Temperature_Measured>","Mesure <M_Temperature_Measured> : 4000")
            
            if ckeck4 ==True :
                print(f'0 {h4} -  {ckeck4}')
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
                
                with open('temperature2.txt','w+') as temp :
                    temp.write('\n')
                    temp.write(f' M_Temperature_Measured : > {fg[0]} C')
                    
            phrfindmesure = "Mesure <M_DEBIT_RECEIVER_ETH3>"
            phi4 = Finder(s_line,phrfindmesure )
            
            ckeck4,h4 = phi4.chack("Mesure <M_DEBIT_RECEIVER_ETH3>","Mesure <M_Temperature_Measured> : 4000")
            
            if ckeck4 ==True :
                print(f'0 {h4} -  {ckeck4}')
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
                
                with open('M_DEBIT_RECEIVER_ETH3.txt','w+') as temp :
                    temp.write('\n')
                    temp.write(f' Mesure <M_DEBIT_RECEIVER_ETH3> : {fg[0]} Mbits')
                
            phresexgg  ='Mesure <M_Temperature_Measured_XGS>       : ATR_BCTT - Status 1'
            
            phi5 = Finder(s_line,phresexgg)
            check5 , h5 = phi5.chack('Mesure <M_Temperature_Measured_XGS>' , 'XSG')
            if check5 ==True :
                print(f'0 {h5} -  {check5}')
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
                
                with open('temperaturexsg2.txt','w+') as temp :
                    temp.write('\n')
                    temp.write(f' M_Temperature_Measured_XGS : > {fg[0]} C')
            
            phrasetension = "Mesure <M_Measured_Tesion_XGS>            : ATR_BCTT - Status 0"
            phi7 = Finder(s_line,phrasetension )
            
            ckeck7,h7 = phi7.chack("Mesure <M_Measured_Tesion_XGS","<M_Measured_Tesion> : 4000")
         
            if ckeck7 ==True :
                print(f'0 {h7} -  {ckeck7}')
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
                
                with open('tension2.txt','w+') as temp :
                    temp.write('\n')
                    temp.write(f' <M_Measured_Tesion> : > {fg[0]} V')
                    
                    
                    
                    
                    
            phrasetension2 = "Mesure <M_Measured_Tesion>                : la valeur de la Tension mesurée par le testeur après la calibration - Status 0"
            phi8 = Finder(s_line,phrasetension2 )
            
            ckeck8,h8 = phi8.chack("Mesure <M_Measured_Tesion_XGS","<M_Measured_Tesion> : 4000")
         
            if ckeck8 ==True :
                print(f'0 {h8} -  {ckeck8}')
                f_ = f.seek(f.tell())
                print(f_)
                print(number_line)
                print(s_line)
                
                last_pos = f.tell()
                print(phrasetension2)
                last_pos += 3
                
                f.seek(last_pos)
                line3 = f.readline()
                
                s_line_mesured3    = line3.decode('ISO-8859-1') 
                fg3 = s_line_mesured3.split(' ')
                print(fg3)
                fg3 = [i   for i in fg  if i !='']
                print(fg3)
                
                with open('tensionmesure2.txt','w+') as temp :
                    temp.write('\n')
                    temp.write(f' Mesure <M_Measured_Tesion> : la valeur de la Tension  {fg3[0]} V')
                
        
    f.close()
    dfa.close()
                
                
                
            
            