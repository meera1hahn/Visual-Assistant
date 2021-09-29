import MySQLdb as mdb
import json
from peewee import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
import csv

"""This shows how we created the question features used to obtain the results for taskA this script operates directly on the database so it will have to be modified to work on the hit data json file provided. The features are avalible in "questionFeatures.csv" but this serves as a reference on how to create them"""

qset_flythrough = json.load(open("../../Data/MemQATask_data.json"))
qId_objId = json.load(open("../../Data/questionInfo.json"))

config = json.load(open('config.json', 'r'))
db = mdb.connect(host="localhost", user=config['db_user'], db='assistDB',  passwd=config['db_pass'])
cursor = db.cursor()

ansBinary = ['yes', 'no']
ansCount = ['1','2','3']
ansColor = ['beige', 'black', 'blue', 'brown', 'green', 'grey', 'orange', 'purple', 'red', 'silver', 'white', 'yellow']
ansLocation = ['bathroom', 'bedroom', 'closet', 'dining room', 'family room', 'foyer', 'garage', 'gym', 'kitchen', 'laundry room', 'library', 'living room', 'lounge', 'meeting room', 'office', 'recreation room', 'spa', 'home theater']
ansDropList = {'location':ansLocation, 
        'count':ansCount, 'room_count':ansCount, 'room_object_count':ansCount, 
        'color':ansColor, 'color_room':ansColor,
        'exist_positive': ansBinary, 'exist_negative':ansBinary, 
        'object_size_compare_xroom': ansBinary, 'object_color_compare_xroom': ansBinary, 
        'object_color_compare_inroom': ansBinary, 'object_size_compare_inroom': ansBinary, 'room_size_compare': ansBinary};
questions_type_used = ['location','color','color_room','exist_positive','exist_negative']
objectTypes = ['toilet',
 'seating',
 'gym equipment',
 'chest of drawers',
 'stove',
 'clothes dryer',
 'oven',
 'table',
 'chair',
 'kitchen appliance',
 'washing machine',
 'toaster',
 'stool',
 'microwave',
 'tv stand',
 'curtain',
 'blinds',
 'picture',
 'plant',
 'door',
 'fridge',
 'cabinet',
 'dryer',
 'sink',
 'cushion',
 'wardrobe',
 'fireplace',
 'refrigerator',
 'furniture',
 'coffee maker',
 'dishwasher',
 'towel',
 'shelves',
 'sofa',
 'counter',
 'bed',
 'shower',
 'range',
 'bathtub',
 'clothes']

def get_exposureMetricRoom(location,qset):
    fly = qset_flythrough[str(qset)]
    cameraActions = fly['cameraAction']
    totalSteps = len(cameraActions) + 1
    totalArea = totalSteps * 768 * 432
    objArea = 0
    temporalExposure = 0
    step = -1
    for enum, i in enumerate(cameraActions):
        if str(location) == str(i.split(',')[0]):
            temporalExposure += 1
            objArea += (768 * 432)
            if step == -1:
                step = enum
    if step == -1:
        step = totalSteps-1
    spatialExposure = objArea/totalArea
    return step, totalSteps,temporalExposure,spatialExposure

def get_exposureMetricObj(objId,qset):
    instances = np.load("habSimData/qset_" + str(qset) + "/frame_instance_maps.npy")
    totalSteps = len(instances) + 1
    step = -1
    totalArea = totalSteps * 768 * 432
    objArea = 0
    temporalExposure = 0
    for enum,frame in enumerate(instances):
        if objId in frame.keys():
            temporalExposure += 1
            objArea += frame[objId]['numPix']
            if step == -1:
                step = enum
    spatialExposure = objArea/totalArea
    return step,totalSteps,temporalExposure,spatialExposure

np.load.__defaults__=(None, True, True, 'ASCII')
questionAnnotations = []
annId = 0
cursor.execute("SELECT id,workerId,hitId,questionset_id FROM amthits where status = 'finished'")
rows = cursor.fetchall()
for done, row in enumerate(rows):
    annId = row[0]
    workerId = row[1]
    hitId = row[2]
    qset = row[3]
    cursor.execute("select * from questionset where qSetId = " + qset)
    questionSet = cursor.fetchone()
    qSetId = questionSet[0]
    pathList = questionSet[1].split(';')
    questionIdList = questionSet[2].split(';')
    questionList = questionSet[3].split(';')
    ogAnswerList = questionSet[4].split(';')
    answerList = questionSet[5].split(';')
    questionTypeList = questionSet[6].split(';')
    imgIdList = questionSet[7].split(';')
    locationNameList = questionSet[8].split(';')
    scan = questionSet[9]
    
    cursor.execute("select answersGuess from submission where workerId = '" + workerId + "' and hitId = '" + hitId + "'")
    answersGuess = cursor.fetchone()[0].split(',')
    for i in range(0,4):
        if questionTypeList[i] not in questions_type_used:
            continue
        question = questionList[i]
        answer = answerList[i]
        mainObj = ''
        for obj in objectTypes:
            if obj in question:
                mainObj = obj
                break
        qId = questionIdList[i]
        
        requestedAssist = False
        cursor.execute("select * from assistance where workerId = '" + workerId + "' and hitId = '" + hitId + "' and questionId = '" + qId + "'")
        if len(cursor.fetchall()) > 0: requestedAssist = True
        
        answeredCorrect = False
        if answersGuess[i] in answerList[i].split(','): answeredCorrect=True
        
        location = imgIdList[i]         
        if 'exist' in questionTypeList[i]:
            roomId = qId_objId[qId]['roomId']
            roomName = qId_objId[qId]['roomId']
            exposureStep,totalSteps,temporalExposure,spatialExposure = get_exposureMetricRoom(location,qSetId)
        else:
            objId = qId_objId[qId]['objId']
            exposureStep,totalSteps,temporalExposure,spatialExposure = get_exposureMetricObj(objId,qSetId)
        
        # 0 = wrongNoAssist, 1 = correctNoAssist, 2 = wrongAssist, 3 =correctAssist
        classY = -1
        if answeredCorrect:
            if requestedAssist:
                classY = 3
            else:
                classY = 2
        else:
            if requestedAssist:
                classY = 2
            else:
                classY = 0
        questionAnnotations.append({
            'qsetId': qSetId,
            'qId': qId,
            'qType': questionTypeList[i],
            'objName': mainObj,
            'exposureStep': exposureStep,
            'totalSteps': totalSteps,
            'temporalExposure': temporalExposure,
            'spatialExposure': spatialExposure,
            'requestedAssist': requestedAssist,
            'answeredCorrect': answeredCorrect,
            'classY': classY
        })
    if done % 100 == 0:
        print(str(done) + ' out of ' + str(len(rows)))

csv_columns = questionAnnotations[0].keys()
print(csv_columns)
csv_file = 'questionFeatures.csv'
with open(csv_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in questionAnnotations:
        writer.writerow(data)
        

