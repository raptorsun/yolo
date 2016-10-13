import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

IfKnowBase = False
Base = 0

def returnToBase(base, Podx, Pody, enemyPodx, enemyPody):
	if base==0:
		if enemyPodx <= Podx:
			if enemyPody > Pody:
				return [1000, 0, 100]
			else:
				return [1000, 1, 100]
		else:
			y = (1000*(enemyPody-Pody) + enemyPodx*Pody - Podx*enemyPody)/(enemyPodx-Podx)
			if y > 8000 :
				y= 8000
			elif y< 0:
				y=0
			else:
				y = int(round(y))
			return [1000, y, 100]
	else:
		if enemyPodx >= Podx:
			if enemyPody > Pody:
				return [9000, 0, 100]
			else:
				return [9000, 1, 100]
		else:
			y = (9000*(enemyPody-Pody) + enemyPodx*Pody - Podx*enemyPody)/(enemyPodx-Podx)
			if y > 8000 :
				y= 8000
			elif y< 0:
				y=0
			else:
				y = int(round(y))
			return [9000, y, 100]

def captureFlag(Podx, Pody, flagX, flagY):
	return [flagX, flagY, 100] 

DIAMETER_POD = 800
DIAMETER_FLAG = 300
BOOST_VALUE = 500
MAX_THRUST = 100
MAX_X = 10000
MAX_Y = 8000

MAX_THRUST_TRIGGER_ETA = 4
DISTANCE_TRIGGER_BOOST = 2 * DIAMETER_POD + BOOST_VALUE
TARGET_TOO_NEAR_DISTANCE = DIAMETER_POD * 1.5
def reflect_coord(coord, border):
	return 2 * border - coord

def attackPod(myPod, enemyPod):
    myPodx = myPod[0]
    myPody = myPod[1]
    myPodVx = myPod[2]
    myPodVy = myPod[3]
    myVelocity = math.hypot(myPodVx, myPodVy)
    enemyPodx = enemyPod[0]
    enemyPody = enemyPod[1]
    enemyPodVx = enemyPod[2]
    enemyPodVy = enemyPod[3]
    enemyVelocity = math.hypot(enemyPodVx, enemyPodVy)
    outputX = enemyPodx
    outputY = enemyPody
    outputThrust = MAX_THRUST
    distanceMeToEnemy = math.hypot(enemyPodx - myPodx, enemyPody - myPody)
    if distanceMeToEnemy == 0:
    	distanceMeToEnemy = 1
    vectMeToEnemy = [float(enemyPodx - myPodx)/distanceMeToEnemy, float(enemyPody - myPody)/distanceMeToEnemy]

    # far away, aim 3 steps before enemy
    if distanceMeToEnemy > DISTANCE_TRIGGER_BOOST:
    	predict_factor = 3
    	outputX = enemyPodx + predict_factor * enemyPodVx
    	outputY = enemyPody + predict_factor * enemyPodVy
    	outputThrust = min(MAX_THRUST, enemyVelocity - myVelocity + enemyVelocity * 0.5)
    	#enemy faster, full speed
    	if enemyVelocity >= myVelocity:
    		outputThrust = MAX_THRUST
    	#
    	elif distanceMeToEnemy/( myVelocity - enemyVelocity) > MAX_THRUST_TRIGGER_ETA:
    		outputThrust = MAX_THRUST

    # approching, aim 1 steps before
    else:
    	predict_factor = 1
    	outputX = enemyPodx + predict_factor * enemyPodVx
    	outputY = enemyPody + predict_factor * enemyPodVy
    	outputThrust = 'BOOST'

    if outputX > MAX_X:
    	outputX = reflect_coord(outputX, MAX_X)
    elif outputX < 0:
    	outputX = reflect_coord(outputX, 0)
    if outputY > MAX_Y:
    	outputY = reflect_coord(outputY, MAX_Y)
    elif outputY < 0:
    	outputY = reflect_coord(outputY, 0)
    distanceMeToTarget = math.hypot(outputX - myPodx, outputY -myPody)
    if distanceMeToTarget < TARGET_TOO_NEAR_DISTANCE:
    	outputX = enemyPodx
    	outputY = enemyPody
    return [outputX, outputY, outputThrust]


# def attackPod(Podx, Pody, enemyPodx, enemyPody):
# 	return [enemyPodx, enemyPody, 'BOOST']

def defendFlag(base, Podx, Pody, enemyPodx1, enemyPody1, enemyPodx2, enemyPody2, flag_x, flag_y):
	if base==0:
		if math.hypot(enemyPodx1-flag_x, enemyPody1-flag_y) <= math.hypot(enemyPodx2-flag_x, enemyPody2-flag_y):
			return [enemyPodx1, enemyPody1, 100]
		else:
			return [enemyPodx2, enemyPody2, 100]
	else:
		if math.hypot(enemyPodx1-flag_x, enemyPody1-flag_y) <= math.hypot(enemyPodx2-flag_x, enemyPody2-flag_y):
			return [enemyPodx1, enemyPody1, 100]
		else:
			return [enemyPodx2, enemyPody2, 100]


EnemyFlagCarry = -1
myPods = [[],[]]
enemyPods = [[],[]]

# game loop
while True:
	#Input
    flag_x, flag_y = [int(i) for i in raw_input().split()]
    enemy_flag_x, enemy_flag_y = [int(i) for i in raw_input().split()]
    
    
    for i in xrange(2):
        myPods[i] = [int(j) for j in raw_input().split()]
    for i in xrange(2):
        enemyPods[i] = [int(j) for j in raw_input().split()]

    
    if(IfKnowBase==False):
    	if (myPods[0][0]<=1000):
    		Base = 0 # left side
    		IfKnowBase= True
    	else:
    		Base = 1 # right side
    		IfKnowBase = True
    
	#EnemyFlagCarry = -1
    if(enemyPods[0][4]==1):
    	EnemyFlagCarry = 0
    elif(enemyPods[1][4]==1):
    	EnemyFlagCarry = 1
    

    output=[[0,0,0],[0,0,0]]
    if(enemy_flag_x == -1):
    	for i in xrange(2):
    		if(myPods[i][4]==1):
    			if EnemyFlagCarry!=-1:				
    				output[i] = returnToBase(Base, myPods[i][0], myPods[i][1], enemyPods[1-EnemyFlagCarry][0],enemyPods[1-EnemyFlagCarry][1])
    			else:
    				x1 = (enemyPods[0][0]+enemyPods[1][0])/2
    				y1 = (enemyPods[0][1]+enemyPods[1][1])/2
    				output[i] = returnToBase(Base, myPods[i][0], myPods[i][1], x1, y1)
    		else:
    			if(EnemyFlagCarry!=-1):
    				output[i] = attackPod(myPods[i], enemyPods[EnemyFlagCarry])
    			else:
    				output[i] = defendFlag(Base, myPods[i][0],myPods[i][1], enemyPods[0][0], enemyPods[0][1], enemyPods[1][0], enemyPods[1][1], flag_x, flag_y)
    			
    else:
    	if(math.hypot(myPods[0][0]-enemy_flag_x, myPods[0][1]-enemy_flag_y) <= math.hypot(myPods[1][0]-enemy_flag_x, myPods[1][1]-enemy_flag_y) ):
    		output[0] = captureFlag(myPods[0][0], myPods[0][1], enemy_flag_x, enemy_flag_y )
    		if(EnemyFlagCarry!=-1):
    			output[1] = attackPod(myPods[1], enemyPods[EnemyFlagCarry])
    		else:
    			output[1] = defendFlag(Base, myPods[1][0],myPods[1][1], enemyPods[0][0], enemyPods[0][1], enemyPods[1][0], enemyPods[1][1], flag_x, flag_y)
    	else:
    		output[1] = captureFlag(myPods[1][0], myPods[1][1], enemy_flag_x, enemy_flag_y )
    		if(EnemyFlagCarry!=-1):
    			output[0] = attackPod(myPods[0], enemyPods[EnemyFlagCarry])
    		else:
    			output[0] = defendFlag(Base, myPods[0][0],myPods[0][1], enemyPods[0][0], enemyPods[0][1], enemyPods[1][0], enemyPods[1][1], flag_x, flag_y)
    		



    #Output
    for i in xrange(2):

        # Write an action using print
        # To debug: print >> sys.stderr, "Debug messages..."

        print ' '.join([str(x) for x in output[i]])
