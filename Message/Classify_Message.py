#! /usr/bin/env python
# coding:utf-8

import math
import WordSegmentation
import FeatureExtraction
import io
from sklearn.metrics import *

class Util_Classify_Message:

	InputTrainingFile = "training_result.txt"
	InputTestingFile = "testing_result.txt"
	InputOriginalTestingFile = "testing.txt"
	OutPutResultFile = "testing_classify_result.txt"
	OutputFeature = "feature.txt"
	OutputAllFeature = "all_feature.txt"

	NumOfFeature = 200#
	E_p_base = 0.00000001#0.001

	def __init__(self,Training_file,Testing_file):
		self.InputTrainingFile = Training_file
		self.InputTestingFile = Testing_file

	def GetTraingData(self):
		training_file = io.open(self.InputTrainingFile,'r',encoding = 'utf-8')
		train = []
		for line in training_file:
			train .append(line)
		w_seg = WordSegmentation.Util_WordSegmentation()
		cut_train = w_seg.CutList(train)
		tmp_train = []
		for line in cut_train:
			tmp_train.append(line.split('|'))
			#print(line)
		training_file.close()
		# for line in tmp_train:
		# 	for line2 in line:
		# 		print(line2),
		# 		print(' '),
		# 	print('')
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
		util_feature = FeatureExtraction.Util_Feature_Extraction()

		train = self.GetTraingData()
		accuracy = 0.0
		percision = [0.0,0.0]
		recall = [0.0,0.0]
		F1 = [0.0,0.0]
		for i in range(fold):
			Py_0 = 0.0
			Py_1 = 0.0
			Pfeature = {}
			lastPfeature = {}
			tmp_train =[]
			#print(len(train))
			for line in train[0:int((i)*len(train)/fold)]:#
				tmp_train.append(line)

			for line in train[int((i+1)*len(train)/fold):int((fold)*len(train)/fold)]:#
				tmp_train.append(line)

			tmp_feature = util_feature.GetFeature(tmp_train,self.NumOfFeature,self.OutputFeature,self.OutputAllFeature)

			# + -
			for f in tmp_feature:
				Py_0 += self.E_p_base
				Py_1 += self.E_p_base
				Pfeature[f] = [self.E_p_base,self.E_p_base]

			for line in tmp_train:
				if line[0] == '0':

					for col in line[1:len(line)]:
						if col in Pfeature :
							Py_0 +=1
							Pfeature[col][1] += 1
				if line[0] == '1':

					for col in line[1:len(line)]:

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

			Evaluation_Result = []
			Result = []
			for line in train[int((i)*len(train)/fold):int((i+1)*len(train)/fold)]:#
				current_P1 = math.log((Py_1/(Py_0+Py_1)),10)
				current_P0 = math.log((Py_0/(Py_0+Py_1)),10)
				for f in Pfeature:
					if f in line[1:len(line)]:
						current_P1 += math.log(1.25 * Pfeature[f][0]/Py_1,10)
						current_P0 += math.log(2 * Pfeature[f][1]/Py_0,10)
				#for col in line[1:len(line)-1]:

					#if col in Pfeature:
						#current_P1 *= Pfeature[col][0]/Py_1
						#current_P0 *= Pfeature[col][1]/Py_0
				if(current_P1 == 0 or current_P0 ==0):
					print("equal to 0 --->error")
					exit()
				if current_P1 >= current_P0:
					Evaluation_Result.append(1)
				else:
					Evaluation_Result.append(0)
				if line[0] == '1':
					Result.append(1)
				elif line[0] == '0':
					Result.append(0)
				'''
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
					'''
				'''
				if (current_P1 >= current_P0 and line[0] == '1'):
					TP +=1
				elif (current_P1 < current_P0 and line[0] == '0'):
					TN += 1
				elif (current_P1 >= current_P0 and line[0] == '0'):
					FP += 1
				elif (current_P1 < current_P0 and line[0] == '1'):
					FN += 1
				else:
					print("error result")
				'''
			#print("Right is"+ str((TP+TN)/(TP+TN+FP+FN)))
			Evaluation = precision_recall_fscore_support(Result,Evaluation_Result,pos_label = 1)
			Accuracy = accuracy_score(Result,Evaluation_Result)
			#print(Evaluation)
			# print("Percision OF "+str(i+1)+"th training is " + str(TP/(TP+FP)))
			# print("Recall OF "+str(i+1)+"th training is " + str(TP/(TP+FN)))
			# print("F1 OF "+str(i+1)+"th training is " + str(2*TP/(2*TP+FP+FN)) + '\n\n')
			print("Accuracy OF "+str(i+1)+"th training is "+str(Accuracy))
			print("Percision OF "+str(i+1)+"th training is " + str(Evaluation[0]))
			print("Recall OF "+str(i+1)+"th training is " + str(Evaluation[1]))
			print("F1 OF "+str(i+1)+"th training is " + str(Evaluation[2])+ '\n\n')
			percision += Evaluation[0]
			recall += Evaluation[1]
			F1 += Evaluation[2]
			accuracy += Accuracy
			#print("by tool")
		print("Now Get The Final Evaluation Of This Model:")
		print("Accuracy is " + str(accuracy/5)+"\n")
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

InputTrainingFileName = 'training.txt'
InputTestingFileName = 'testing.txt'
c_Msg = Util_Classify_Message(InputTrainingFileName,InputTestingFileName)
c_Msg.Training(5)
