#! /usr/bin/env python
# -*- coding: utf-8 -*-
import jieba  
import re
import io

#  
def stopwordslist(filepath):  
    stopwords = [line.strip() for line in io.open(filepath, 'r',encoding = 'utf-8').readlines()]  
    return stopwords  

def Divide(InputFileName,OutPutFileName):
	Input_file = io.open(InputFileName,'r',encoding = 'utf-8')
	result_file = io.open(OutPutFileName,"w",encoding = 'utf-8')
	tmp = []
	#docus = []
	#for line in Input_file.readlines():
		#string = str(line)
		#print(string)
		#docus.append(str(line))

	docus = [line for line in Input_file.readlines()] 
	num = 0
	for line in docus:
		if line.strip() == '':
			num = num +1
			print("sss"+str(num))
	for line in docus:
		#print(line)
		seg_list = jieba.cut(line.strip(), cut_all=True )#
		#stopwords = stopwordslist('stopword.dic')  # 
		result = ''
		#for word in seg_list:  
	        	#if word not in stopwords:  
	        	    	#if word != '\t':  
	 		#result+= word
	       # result+= "|"  
				
		result = str("|".join(seg_list))
		
		result = re.sub('xx*','|',result)
		result = re.sub('\|\|*','|',result)
		#result = result[0:len(result)-1]
		result = result.strip()
		if result != '' and result[0] == '|':
				result = result[1:len(result)]
		result = result.strip()
		#if result != '' and result != '0' and result != '1':
		result_file.write(result + '\n')
	result_file.flush();
	result_file.close();
	Input_file.close()	

Divide('training.txt','training_result.txt')
print("Training Text Divide Is Down!")
Divide('testing.txt','testing_result.txt')
print("Testing Text Divide Is Down!")
