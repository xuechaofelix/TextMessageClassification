#! /usr/bin/env python3.6

InputTrainingFile = "training_result.txt"
InputFeatureFile = "feature.txt"
OutPutResultFile = "testing_classify_result.txt"

training_file = open(InputTrainingFile)
train = []
for line in training_file:
	train.append(line.split('|'))
training_file.close()

feature_file = open(InputFeatureFile)
feature = []
for line in feature_file:
	s = line.split(',')
	s[0] = s[0][2:len(s[0])-1]
	s[0] = s[0].strip()
	feature.append(s[0])
feature_file.close()

Py_0 = 0.0
Py_1 = 0.0
Pfeature = {}
# + -
for f in feature:
	Pfeature[f] = [0.0,0.0]

for line in train[0:int(4*len(train)/5)]: #前4/5为训练集
	if line[0] == '0':
		for col in line[1:len(line)]:
			Py_0 +=1
			if col in Pfeature:
				Pfeature[col][1] += 1 
	if line[0] == '1':
		for col in line[1:len(line)]:
			Py_1 +=1
			if col in Pfeature:
				Pfeature[col][0] += 1

right = 0.0
total = 0.0
for line in train[int(4*len(train)/5):len(train)]:# 后1/5是用来测试
	total +=1
	current_P1 = (Py_1/(Py_0+Py_1))
	current_P0 = (Py_0/(Py_0+Py_1))
	
	for col in line[1:len(line)]:
		if col in Pfeature:
			current_P1 *= Pfeature[col][0]/Py_1
			current_P0 *= Pfeature[col][1]/Py_0
	if (current_P1 >= current_P0 and line[0] == '1') or (current_P1 < current_P0 and line[0] == '0'):
		right +=1
	print("current right rate is" + str(right/total));
right = right/total
#get the test result
testing_file = open("testing_result.txt")
test = []
test_result = []
total =0
for line in testing_file:
	test.append(line.split('|'))
	test_result.append(line)
	total +=1
testing_file.close()

all_result_file = open(OutPutResultFile,"w")

current =0
print("Now Calculating The Testing File....")
for i in range(len(test)):
	line = test[i]
	current_P1 = (Py_1/(Py_0+Py_1))
	current_P0 = (Py_0/(Py_0+Py_1))
	for col in line[0:len(line)]:
		if (col in Pfeature):
			current_P1 *= Pfeature[col][0]/Py_1
			current_P0 *= Pfeature[col][1]/Py_0
	
	if (current_P1 >= current_P0) :
		all_result_file.write('1'+' '+test_result[i]+'\r\n')
	elif (current_P1 < current_P0):
		all_result_file.write('0'+' '+test_result[i]+'\r\n')
	current +=1 
	print("Processing is" + str(current/total));

print('Now Calculating is down!')
print('Right rate is',str(right))
print('The testing file result is in the \'testing_classify_result\'')
all_result_file.flush()
all_result_file.close()
