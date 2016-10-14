import sys
import math
import cmath

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

IfKnowBase = False
Base = 0


def quadratic(a, b, c):
	return (math.sqrt((b**2)-(4*a*c))-b)/(2*a)

def normalizedVector(vector):
    return [vector[0]/math.hypot(vector[0],vector[1]), vector[1]/math.hypot(vector[0],vector[1])]

def dotProduct(vector1, vector2):
    return vector1[0]*vector2[0]+vector1[1]*vector2[1]

def mirrorVector(vectorA, vectorB):
    normalizedVectorB = normalizedVector(vectorB)
    product = dotProduct(vectorA, vectorB)
    centerVector = [normalizedVectorB[0]*product, normalizedVectorB[1]*product]
    mirroredVector = [2*centerVector[0]-vectorA[0], 2*centerVector[1]-vectorA[1]]
    return mirroredVector

def intersect(pt, vector, borderN):
    #upper
    if borderN == 1;
        intersecX = pt[0] - pt[1]*vector[0]/vector[1]
        intersecY = 0
        return [intersecX, intersecY]
    #bottom
    if borderN == 2:
        intersecX = pt[0] + (8000-pt[1])*vector[0]/vector[1]
        intersecY = 8000
        return [intersecX, intersecY]
    #Left
    if borderN == 3:
        intersecX = 0
        intersecY = pt[1] - pt[0]*vector[1]/vector[0]
        return [intersecX, intersecY]
    #right
    if borderN == 4:
        intersecX = 10000;
        intersecY = pt[1] + (10000-pt[0])*vector[1]/vector[0]
        return [intersecX, intersecY]
    return [0,0]




def reflect_coord(coord, border):
	return 2 * border - coord

def getAngle( posE, posM):
	return math.atan2( (posE[1] - posM[1]), (posE[0] - posM[0]) )


def returnToBase(base, Pod, enemyPods):







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



def captureFlag(base, Pod, flagX, flagY):
    position = [Pod[0], Pod[1]]
    speedVector = [Pod[2], Pod[3]]
    if math.hypot(speedVector[0], speedVector[1]) > 100:
        vectorDirect = [flagX-Pod[0], flagY-Pod[1]]
        vectorUpper = [flagX-Pod[0], -flagY-Pod[1]]
        vectorBottom = [flagX-Pod[0], 16000-flagY-Pod[1]]
        vectorLeft = [-flagX-Pod[0], flagY-Pod[1]]
        vectorRight = [20000-flagX-Pod[0], flagY-Pod[1]]

        directionVectors = [vectorDirect, vectorUpper, vectorBottom, vectorLeft, vectorRight]

        directionVectorsNormalized = [ normalizedVector(x) for x in directionVectors]

        dotProducts = [dotProduct(speedVector, x) for x in directionVectorsNormalized]

        maxDotProduct = max(dotProducts)

        maxDotProductIndex = [i for i, j in enumerate(dotProducts) if j == maxDotProduct]

        routeVector = directionVectorsNormalized[maxDotProductIndex[0]]

        thrustVector = mirroredVector(speedVector, routeVector)

        targetDirectionVector = [];

        if maxDotProductIndex == 0:
            targetDirectionVector[0] = min(max( int(round(thrustVector[0]*200)) + Pod[0], 0), 10000)
            targetDirectionVector[1] = min(max( int(round(thrustVector[0]*200)) + Pod[1], 0), 8000)
        else:
            targetDirectionVector = intersect(position, thrustVector, maxDotProductIndex)

        return [ targetDirectionVector[0], targetDirectionVector[1], "BOOST"]
    else:
        if base == 0:
            return [10000, Pod[1], 100]
        else:
            return [[0], Pod[1], 100]





DIAMETER_POD = 800
DIAMETER_FLAG = 300
BOOST_VALUE = 500
MAX_THRUST = 100
MAX_X = 10000
MAX_Y = 8000

MAX_THRUST_TRIGGER_ETA = 4
TARGET_TOO_NEAR_DISTANCE = DIAMETER_POD * 1.5
DISTANCE_TRIGGER_BOOST = DIAMETER_POD + BOOST_VALUE - MAX_THRUST


def attackPod(base, myPod, enemyPod):
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
    	outputThrust = max(0, min(MAX_THRUST, enemyVelocity - myVelocity + enemyVelocity * 1))
    	outputThrust = MAX_THRUST;
    	#enemy faster, full speed
    	if enemyVelocity >= myVelocity:
    		outputThrust = 'BOOST'
    	#
    	elif distanceMeToEnemy/( myVelocity - enemyVelocity) > MAX_THRUST_TRIGGER_ETA:
    		outputThrust = 'BOOST'

    # approching, aim 1 steps before
    else:
    	predict_factor = 1
    	outputX = enemyPodx + predict_factor * enemyPodVx
    	outputY = enemyPody + predict_factor * enemyPodVy
    	outputThrust = MAX_THRUST

    if outputX > MAX_X:
    	if base == 0:
    		outputX = 9000 - DIAMETER_POD / 2
    	else:
    		outputX = reflect_coord(outputX, MAX_X)
    elif outputX < 0:
    	if base == 1:
    		outputX = 1000 + DIAMETER_POD / 2
    	else:
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


def defendFlag(base, Pod, enemyPod1, enemyPod2, flag_x, flag_y):
	if math.hypot(enemyPod1[0]-flag_x, enemyPod1[1]-flag_y) <= math.hypot(enemyPod2[0]-flag_x, enemyPod2[1]-flag_y):
		output = attackPod(base, Pod, enemyPod1)
		output[2] = MAX_THRUST
		return output
	else:
		output = attackPod(base, Pod, enemyPod2)
		output[2] = MAX_THRUST
		return output


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

    if myPods[0][4]==1:
        output[0] = returnToBase(myPods[0])
    else:
        output[0] = captureFlag(Pod, flag_x, flag_y)

    if(EnemyFlagCarry!=-1):
                output[1] = attackPod(Base, myPods[1], enemyPods[EnemyFlagCarry])
            else:
                output[1] = defendFlag(Base, myPods[1], enemyPods[0],  enemyPods[1], flag_x, flag_y)





    #Output
    for i in xrange(2):

        # Write an action using print
        # To debug: print >> sys.stderr, "Debug messages..."

        print ' '.join([str(x) for x in output[i]])
