import sys
import math


class GlobalCounters:
    pass

globalcounters = GlobalCounters()

DIAMETER_POD = 800
DIAMETER_FLAG = 300
BOOST_VALUE = 500
MAX_THRUST = 100
MAX_X = 10000
MAX_Y = 8000

MAX_THRUST_TRIGGER_ETA = 4
DISTANCE_TRIGGER_BOOST = DIAMETER_POD + BOOST_VALUE - MAX_THRUST
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


def getTopMirror(pos):
    return [pos[0] , reflect_coord(pos[1], 0)]
def getBottomMirror(pos):
    return [pos[0] , reflect_coord(pos[1], 8000)]
def getLeftMirror(pos):
    return [reflect_coord(pos[0], 0), pos[1]]
def getRightMirror(pos):
    return [reflect_coord(pos[1], 10000), pos[1]]

def getDirectionScore(pod, target):
    vectPodTarget = [target[0] -pod[0], target[1] - pod[1]]
    angle_distance =  math.atan2(vectPodTarget[1], vectPodTarget[0])
    angle_velocity = math.atan2(pod[3] - pod[1], pod[2] - pod[0])
    return abs(angle_velocity - angle_distance)

# pod[0] = x pod[1] = y
def chooseDirection(pod, flag):
    flag_mirror_top = getTopMirror(flag)
    flag_mirror_bottom = getBottomMirror(flag)
    flag_mirror_left = getLeftMirror(flag)
    flag_mirror_right = getRightMirror(flag)
    mirror_coords = [flag_mirror_top, flag_mirror_bottom, flag_mirror_left, flag_mirror_right]
    scores = [ getDirectionScore(pod, x) for x in mirror_coords]
    print scores
    scores_tmp = list(scores)
    print scores_tmp
    scores.sort()
    minval = scores[0]
    print minval
    return mirror_coords[scores_tmp.index(minval)]

# the aiming point of the pod, if target is off border,
# return the intersection with border
def aimPoint(pod, target):
    outputX = target[0]
    outputY = target[1]

    if 0< target[0] and target[0] < MAX_X and 0 < target[1] and target[1] < MAX_Y:
        pass
    #target off left border
    elif target[0] < 0:
        outputX = 0
        outputY = (outputX - pod[0])* float(pod[1] - target[1])/(pod[0] - target[0]) + pod[1]
    elif target[0] > MAX_X:
        outputX = MAX_X
        outputY = (outputX - pod[0])* float(pod[1] - target[1])/(pod[0] - target[0]) + pod[1]
    elif target[1] < 0:
        outputY = 0
        outputX = (outputY - pod[1])* float(pod[0] - target[0])/(pod[1] - target[1]) + pod[0]
    elif target[1] > MAX_Y:
        outputY = MAX_Y
        outputX = (outputY - pod[1])* float(pod[0] - target[0])/(pod[1] - target[1]) + pod[0]

    outputX = int(outputX)
    outputY = int(outputY)
    return [outputX, outputY]

# chase the flag with full speed, always follow the minimal turning angel
# bounce off the border when the angle is right
def captureFlag(Podx, Pody, flagX, flagY):
    return [flagX, flagY, 100]


def main():
    my_pod = [50, 50, 150, 200]
    flag = [90 , 90]
    #print getDirectionScore(my_pod, flag) * 180 / 3.14
    targetpoint = chooseDirection(my_pod,flag)
    print 'targetpoint = %s' % (str(targetpoint),)
    aimpoint = aimPoint(my_pod, targetpoint)
    print 'aimpoint = %s' % (str(aimpoint),)

    enemy_pod = [30,8000, 100, 180]




#   print attackPod(my_pod, enemy_pod)

#   enemy_pod = [9888,1500, 100, 180]

#   print attackPod(my_pod, enemy_pod)

#   enemy_pod = [100,1600, 100, 180]

#   print attackPod(my_pod, enemy_pod)

#   enemy_pod = [30,500 , 100, 180]

#   print attackPod(my_pod, enemy_pod)

if __name__ == "__main__":
    main()
