from threading import Thread
import time


# 요구 해상도로 올려져 있을 경우 해당 카메라가 추가되는 리스트
HighResolution = []
Maxcount = 0
MaxBandwidth = 100
total = 0
threadstate = False

# fps를 낮춰주는 스레드
def lowerfps_thread():
    global threadstate, Maxcount, MaxBandwidth
    index = 0
    while threadstate:
        try:
            if index == Maxcount:
                index = 0
            print(str(HighResolution[index]) + " down")
            time.sleep(2)
            print(str(index) + " up")
            index += 1
        except IndexError:
            threadstate = False

# 수용 대역폭이 한정 대역폭을 초과 하였을때
while True:
    # 리스트에 넣는 부분 추가(리스트에 높아진게 없을 경우 추가, 리스트에 낮춰진게 있을 경우 삭제)
    if MaxBandwidth < total and not threadstate:
        # 리스트 sorting 하는 부분 추가
        Maxcount = len(HighResolution)
        threadstate = True
        t1 = Thread(target=lowerfps_thread)
        t1.start()






