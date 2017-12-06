#! /usr/bin/env python3.6
import math
InputFileName = "training_result.txt"
OutputFeature = "feature.txt"
OutputAllFeature = "all_feature.txt"
NumOfFeature = 10000#特征取前10000个


########################################################################3
training_file = open(InputFileName)#通过分词后的训练集

train = []
for line in training_file:
	train.append(line.split('|'))
training_file.close()
#+1,+0,-1,-0
word = {}
docu_num = 0
docu_1_num =0
docu_0_num = 0
for line in train[0:int(4*len(train)/5)]:
	docu_num +=1
	if line[0] == '1':
		for col in line[1:len(line)-1]:
			docu_1_num += 1
			if col in word:
				word[col][0] +=1
			else:
				word[col] = [1.0,0.0,0.0,0.0]
	elif line[0] == '0' :
		for col in line[1:len(line)-1]:
			docu_0_num += 1
			if col in word:
				word[col][2] +=1
			else:
				word[col]= [0.0,0.0,1.0,0.0]
	else:
		print(line),
		print("eror")
N1 = 0.0
N0 = 0.0
for line in train[0:int(4*len(train)/5)]:
	if line[0] == '0':
		N0 +=1
	else:
		N1 +=1
del train
if docu_num != N1+N0:
	print("error")
	exit()
total_word = 0
for w in word:
	total_word +=1
	word[w][1] = docu_1_num - word[w][0]
	word[w][3] = docu_0_num - word[w][2]
E_s = -((N1/(N1+N0))*math.log(N1/(N1+N0)) + (N0/(N1+N0))*math.log(N0/(N1+N0)))

######################################################
info_gain={}
num = 0
for w in word:
	num +=1
	A = word[w][0]
	B = word[w][2]
	C = word[w][1]
	D = word[w][3]
	#print(A,B,C,D)
	if A == 0.0:
		A_part = 0.0
	else:
		A_part = (A/(A+B)) * math.log(A/(A+B),2)
	if B == 0.0:
		B_part = 0.0
	else:
		B_part = (B/(A+B)) * math.log(B/(A+B),2)
	if C == 0.0:
		C_part = 0.0
	else:
		C_part = (C/(C+D)) * math.log(C/(C+D),2) 
	if D == 0.0:
		D_part = 0.0
	else:
		D_part = (D/(C+D)) * math.log(D/(C+D),2)
	info_gain[w] = E_s +((A+B)/(N1+N0))*(A_part + B_part) + ((C+D)/(N1+N0))*(C_part + D_part)
	print("processing is "+str(float(num)/float(total_word)))
	
del word

####################################################################3
info_gain= sorted(info_gain.items(), key=lambda d:d[1], reverse = True)

result_file = open(OutputFeature,"w") #取前面的特征

for k in info_gain[0:NumOfFeature]:
	result_file.write(str(k)+'\r\n')
result_file.flush()
result_file.close()

all_result_file = open(OutputAllFeature,"w") #所有的特征

for k in info_gain:
	all_result_file.write(str(k)+'\r\n')
all_result_file.flush()
all_result_file.close()
	

