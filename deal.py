#! /usr/bin/env python3.6
import math

class Feature:
	E_p_base = 1.0
	def __CalculateInformationGain(self,train):
		word = {}
		lastword = {}
		docu_num = 0
		docu_1_num =0
		docu_0_num = 0
		
		#print(word)
			
		for line in train:
			docu_num +=1
			length = len(line)-1
			if line[0] == '1':
				
				for col in line[1:length]:
					docu_1_num += 1
					if col in word:
						word[col][0] +=1
					else: 
						word[col] = [self.E_p_base+1,self.E_p_base,self.E_p_base,self.E_p_base]
			elif line[0] == '0':
				
				for col in line[1:length]:
					docu_0_num += 1
					if col in word:
							word[col][2] +=1
					else :
						word[col] = [self.E_p_base,self.E_p_base,self.E_p_base+1,self.E_p_base]
			else:
				print(line),
				print("error")
			
				
			#print(docu_num)
		N1 = 0.0
		N0 = 0.0
		for line in train:
			if line[0] == '0':
				N0 +=1
			else:
				N1 +=1
		#del train
		if docu_num != N1+N0:
			print("error")
			exit()
		total_word = 0
		for w in word:
			total_word +=1
			word[w][1] = docu_1_num - word[w][0]
			word[w][3] = docu_0_num - word[w][2]
		#for w in word:
			#if docu_num != word[w][0]+word[w][1]+word[w][2]+word[w][3]:
				#print("error")
				#exit()
		N1 = docu_1_num
		N2 = docu_0_num
		E_s = -((N1/(N1+N0))*math.log(N1/(N1+N0)) + (N0/(N1+N0))*math.log(N0/(N1+N0)))# get the system etropy
		#print(E_s)
##############################################		
		info_gain={}
		num = 0
		for w in word:
			num +=1
			A = word[w][0]# 正例中出现
			B = word[w][2]# 负例中出现
			C = word[w][1]# 正例中不出现
			D = word[w][3]# 负例中不出现
			#print(A,B,C,D)
			if A+B+C+D != docu_1_num +docu_0_num :
				print("Number Not Equal ---> error")
				exit()
			A_part = (A/(A+B)) * math.log(A/(A+B),2)
			
			B_part = (B/(A+B)) * math.log(B/(A+B),2)
			
			C_part = (C/(C+D)) * math.log(C/(C+D),2) 
			
			D_part = (D/(C+D)) * math.log(D/(C+D),2)
			info_gain[w] = E_s +((A+B)/(N1+N0))*(A_part + B_part) + ((C+D)/(N1+N0))*(C_part + D_part)
			if(info_gain[w] == 0):
				print("Info Gain equal to 0 ---> error")
				exit()
			#print("processing is "+str(float(num)/float(total_word)))
	
		del word

		####################################################################3
		info_gain= sorted(info_gain.items(), key=lambda d:d[1], reverse = True)
		return info_gain

	def __OutPutFeature(self,info_gain_sorted,Num,OutputFeature,OutputAllFeature):
		result_file = open(OutputFeature,"w") #取前面的特征

		for k in info_gain_sorted[0:Num]:
			result_file.write(str(k)+'\r\n')
		result_file.flush()
		result_file.close()

		all_result_file = open(OutputAllFeature,"w") #所有的特征

		for k in info_gain_sorted:
			result = str(k)
			all_result_file.write(result[1:len(result)-1]+'\r\n')
		all_result_file.flush()
		all_result_file.close()
	
	
	def GetFeature(self,train,NumOfFeature,outputfeaturefile,outputallfeaturefile):
		info_gain = self.__CalculateInformationGain(train)
		self.__OutPutFeature(info_gain,NumOfFeature,outputfeaturefile,outputallfeaturefile)
		feature = []
		for k in info_gain[0:NumOfFeature]:
			s = str(k).split(',')
			s[0] = s[0][2:len(s[0])-1]
			s[0] = s[0].strip()
			feature.append(s[0])
		return feature


class Deal:
	
	InputTrainingFile = "training_result.txt"
	InputTestingFile = "testing_result.txt"
	InputOriginalTestingFile = "testing.txt"
	OutPutResultFile = "testing_classify_result.txt"
	OutputFeature = "feature.txt"
	OutputAllFeature = "all_feature.txt"
	NumOfFeature = 10000#特征取前10000个
	E_p_base = 1.0000000#0.001 
	


	def GetTraingData(self):
		training_file = open(self.InputTrainingFile)
		tmp_train = []
		for line in training_file:
			tmp_train.append(line.split('|'))
		training_file.close()	
		
		return tmp_train
	def GetTestingData(self):
		testing_file = open(self.InputTestingFile)
		test_result = []
		for line in testing_file:
			test_result.append(line.split('|'))
		testing_file.close()
		return test_result
	def GetFeature(self):
		feature_file = open(self.OutputFeature)
		tmp_feature = []
		for line in feature_file:
			s = line.split(',')
			s[0] = s[0][2:len(s[0])-1]
			s[0] = s[0].strip()
			tmp_feature.append(s[0])
		feature_file.close()
		return tmp_featrue
	
	def Training(self,fold):
		print("Evaluate the model by "+str(fold)+"-fold(it will cost some time to training the model)......\n")
		util_feature = Feature() 
		
		train = self.GetTraingData()
		percision = 0.0
		recall = 0.0
		F1 = 0.0
		for i in range(fold):
			Py_0 = 0.0
			Py_1 = 0.0
			Pfeature = {}
			lastPfeature = {}
			tmp_train =[]
			#print(len(train))
			for line in train[0:int((i)*len(train)/fold)]:#训练集前半部分
				tmp_train.append(line)

			for line in train[int((i+1)*len(train)/fold):int((fold)*len(train)/fold)]:#训练集后半部分
				tmp_train.append(line)
			
			tmp_feature = util_feature.GetFeature(tmp_train,self.NumOfFeature,self.OutputFeature,self.OutputAllFeature)
			
			# + -
			for f in tmp_feature:
				Py_0 += self.E_p_base
				Py_1 += self.E_p_base
				Pfeature[f] = [self.E_p_base,self.E_p_base]

			for line in tmp_train:
				if line[0] == '0':
					
					for col in line[1:len(line)-1]:
						if col in Pfeature :
							Py_0 +=1
							Pfeature[col][1] += 1  
				if line[0] == '1':
					
					for col in line[1:len(line)-1]:
						
						if col in Pfeature:
							Py_1 +=1
							Pfeature[col][0] += 1
			
			#for f in Pfeature:
				#if(Pfeature[f][0]+Pfeature[f][1] != Py_0+Py_1)
			#print(Py_1+Py_0)
			TP = 0.0
			FP = 0.0
			TN = 0.0
			FN = 0.0
			print(str(i+1)+"th training is down! \n")
			
			
			for line in train[int((i)*len(train)/fold):int((i+1)*len(train)/fold)]:#测试集部分
				current_P1 = math.log((Py_1/(Py_0+Py_1)),10)
				current_P0 = math.log((Py_0/(Py_0+Py_1)),10)
				for f in Pfeature:
					if f in line[1:len(line)-1]:
						current_P1 += math.log(Pfeature[f][0]/Py_1,10)
						current_P0 += math.log(Pfeature[f][1]/Py_0,10)
				#for col in line[1:len(line)-1]:
					
					#if col in Pfeature:
						#current_P1 *= Pfeature[col][0]/Py_1
						#current_P0 *= Pfeature[col][1]/Py_0
				if(current_P1 == 0 or current_P0 ==0):
					print("equal to 0 --->error")
					exit()
				if (current_P1 >= current_P0 and line[0] == '1'):
					TN +=1
				elif (current_P1 < current_P0 and line[0] == '0'):
					TP += 1
				elif (current_P1 >= current_P0 and line[0] == '0'):
					FN += 1
				elif (current_P1 < current_P0 and line[0] == '1'):
					FP += 1
				else:
					print("error result")
			#print("Right is"+ str((TP+TN)/(TP+TN+FP+FN)))
			print("Percision OF "+str(i+1)+"th training is " + str(TP/(TP+FP)))
			print("Recall OF "+str(i+1)+"th training is " + str(TP/(TP+FN)))
			print("F1 OF "+str(i+1)+"th training is " + str(2*TP/(2*TP+FP+FN)) + '\n\n')
			percision += TP/(TP+FP)
			recall += TP/(TP+FN)
			F1 += 2*TP/(2*TP+FP+FN)
		print("Now Get The Final Evaluation Of This Model:")
		print("percision is " + str(percision/5))
		print("recall is "+ str(recall/5))
		print("F1 is " + str(F1/5)+"\n")
	
	def GetResult(self):
		util_feature = Feature() 
		
		train = self.GetTraingData()
		Py_0 = 0.0
		Py_1 = 0.0
		Pfeature = {}
		lastPfeature = {}
		tmp_train =[]
			
		for line in train:
			tmp_train.append(line)

		tmp_feature = util_feature.GetFeature(tmp_train,self.NumOfFeature,self.OutputFeature,self.OutputAllFeature)
			
		# + -
		for f in tmp_feature:
			Py_0 += self.E_p_base
			Py_1 += self.E_p_base
			Pfeature[f] = [self.E_p_base,self.E_p_base]

		for line in tmp_train:
			if line[0] == '0':
					
				for col in line[1:len(line)-1]:
						
					if col in Pfeature :
						Py_0 +=1
						Pfeature[col][1] += 1  
			if line[0] == '1':
					
				for col in line[1:len(line)-1]:
						
					if col in Pfeature:
						Py_1 +=1
						Pfeature[col][0] += 1
		
		test = self.GetTestingData()
		for line in test:
			current_P1 = (Py_1/(Py_0+Py_1))
			current_P0 = (Py_0/(Py_0+Py_1))
			
			for f in Pfeature:
				if f in line[1:len(line)-1]:
					current_P1 *= Pfeature[f][0]/Py_1
					current_P0 *= Pfeature[f][1]/Py_0
			#for col in line[1:len(line)-1]:
				#if col in Pfeature:
					#current_P1 *= Pfeature[col][0]/Py_1
					#current_P0 *= Pfeature[col][1]/Py_0
			if (current_P1 >= current_P0 ):
				line.insert(0,'1 ')
			elif (current_P1 < current_P0):
				line.insert(0,'0 ')
		print("calculating data is down!\nThen write it to the file --->"+self.OutPutResultFile)
	
		orignalTestingFile = open(self.InputOriginalTestingFile)
		orignalTest = []
		for line in orignalTestingFile:
			orignalTest.append(line)
		orignalTestingFile.close()
		all_result_file = open(self.OutPutResultFile,"w")
		for i in range(len(test)):
			all_result_file.write(test[i][0]+' '+orignalTest[i]+'\r\n')

		print('Now Writing file is down!')
		all_result_file.flush()
		all_result_file.close()

util_MessageClassify = Deal()
util_MessageClassify.Training(5)
#util_MessageClassify.GetResult()
