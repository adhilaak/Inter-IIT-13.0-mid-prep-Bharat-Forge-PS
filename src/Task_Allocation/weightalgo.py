import numpy as np

#Parameters
distancemax=200
urgencymax=10
backlogmax=20
weightmax=2

trainingset=10000
testset=20


def weightcalculator(distance,urgency,backlog):

    if(urgency==urgencymax):
        return weightmax
    
    distance=np.exp(np.exp(distance/distancemax))
    urgency=np.exp(urgency/3)
    backlog=np.exp(np.exp(backlog/backlogmax))
    
    sum=distance+urgency+backlog

    distance/=sum
    urgency/=sum
    backlog/=sum

    weight=(pow(pow(weightmax,3),urgency)-backlog*weightmax-distance)/weightmax
    
    if(weight<0):
        weight=0

    return weight


def getparameters():
    return np.random.randint(distancemax+1),np.random.randint(urgencymax+1),np.random.randint(backlogmax+1)


if __name__=="__main__":
    X_train=[]
    Y_train=[]
    X_test=[]
    Y_test=[]

    for i in range(trainingset):
        distance,urgency,backlog=getparameters()
        weight=weightcalculator(distance,urgency,backlog)
        X_train.append([distance,urgency,backlog])
        Y_train.append([weight])
    
    for i in range(testset):
        distance,urgency,backlog=getparameters()
        weight=weightcalculator(distance,urgency,backlog)
        X_test.append([distance,urgency,backlog])
        Y_test.append(weight)
    
    X_train=np.array(X_train)
    Y_train=np.array(Y_train)
    X_test=np.array(X_test)
    Y_test=np.array(Y_test)

for i in range(testset):
    print(X_train[i],Y_train[i])


import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras import layers

model=Sequential()
model.add(layers.Dense(5,input_shape=(3,),activation='sigmoid'))
model.add(layers.Dense(5,activation='relu'))

model.compile(optimizer="adam",loss="mean_absolute_error",metrics=['accuracy'])
model.summary()

model.fit(X_train,Y_train,epochs=20)


for i in range(testset):
    print("Model Output=",model.predict(np.array([X_test[i]]))[0][0])
    print("Expected Output=",Y_test[i])


model.save('Weight_Model.keras')
