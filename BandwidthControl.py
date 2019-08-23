from threading import Thread
import time

# 요구 해상도로 올려져 있을 경우 해당 카메라가 추가되는 리스트
HighResolution = []
Maxcount = 0
MaxBandwidth = 100
total = 0
threadstate = False

def lowerfps_thread():
    global threadstate, Maxcount
    index = 0
    while not threadstate:
        if index == Maxcount:
            index = 0
        print(str(HighResolution[index]) + " down")
        time.sleep(2)
        print(str(index) + " up")
        index += 1


if MaxBandwidth < total:
    Maxcount = len(HighResolution)
    t1 = Thread(target=lowerfps_thread)
    t1.start()
    time.sleep(13)
    threadstate = True
    HighResolution.remove(HighResolution.index(0))



