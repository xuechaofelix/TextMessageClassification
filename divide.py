#! /usr/bin/env python3.6
import jieba  
import re

training_file = open("training.txt")
training_result_file = open("training_result.txt","w")
tmp_train = []
for line in training_file:
	tmp_train.append(line)
	seg_list = jieba.cut(line.strip(), cut_all=True) 
	result = str("|".join(seg_list))
	result = re.sub('xx*','',result)
	result = re.sub('\|\|*','|',result)
	result = result.strip()
	if result != '' and result != '0' and result != '1':
		training_result_file.write(result + '\n')
training_result_file.flush();
training_result_file.close();
training_file.close()	


testing_file = open("testing.txt")
testing_result_file = open("testing_result.txt","w")
tmp_test = []
for line in testing_file:
	tmp_test.append(line)
	seg_list = jieba.cut(line.strip(), cut_all=True) 
	result = str("|".join(seg_list))
	result = re.sub('xx*','',result)
	result = re.sub('\|\|*','|',result)
	result = result.strip()
	if result != '' and result != '0' and result != '1':
		testing_result_file.write(result + '\n')
testing_result_file.flush();
testing_result_file.close();
testing_file.close()
