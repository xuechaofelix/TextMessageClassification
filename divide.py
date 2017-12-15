#! /usr/bin/env python3.6
import jieba  
import re

# 创建停用词list  
def stopwordslist(filepath):  
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]  
    return stopwords  

def Divide(InputFileName,OutPutFileName):
	Input_file = open(InputFileName)
	result_file = open(OutPutFileName,"w")
	tmp = []
	for line in Input_file:
		tmp.append(line)
		seg_list = jieba.cut(line.strip(), cut_all=True )#
		stopwords = stopwordslist('stopword.dic')  # 这里加载停用词的路径
		result = ''
		for word in seg_list:  
	        	if word not in stopwords:  
	        	    	#if word != '\t':  
	        		        result += word  
	        		        result += "|"  
				
		#result = str("|".join(seg_list))
		
		result = re.sub('xx*','|',result)
		result = re.sub('\|\|*','|',result)
		#result = result[0:len(result)-1]
		result = result.strip()
		if result != '' and result != '0' and result != '1':
			result_file.write(result + '\r\n')
	result_file.flush();
	result_file.close();
	Input_file.close()	

Divide('training.txt','training_result.txt')
print("Training Text Divide Is Down!")
Divide('testing.txt','testing_result.txt')
print("Testing Text Divide Is Down!")
