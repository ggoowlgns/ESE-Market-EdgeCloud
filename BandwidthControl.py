from threading import Thread
import time
import update_bandwidth

priority = {"face_recognition" : 3, "object_detection" : 2, "qr_code" : 1}
HighResolution = [] # 요구 해상도로 올려져 있을 경우 해당 카메라가 추가되는 리스트
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
            time.sleep(3)
            print(str(index) + " up")
            index += 1
        except IndexError:
            threadstate = False

if __name__ == "__main__":
    while True:
        UB = update_bandwidth.UpdateBandwidth()
        UB.update_page()
        in_bw, stream_meta = UB.get_data()
        total = in_bw[0]
        for camera in stream_meta.keys():
            if stream_meta[camera][0] == '160':
                if priority[camera] in HighResolution:
                    HighResolution.remove(priority[camera])
            else:
                HighResolution.append(priority[camera])
        if MaxBandwidth < total and not threadstate:
            sorted(HighResolution)
            Maxcount = len(HighResolution)
            threadstate = True
            t1 = Thread(target=lowerfps_thread)
            t1.start()

# 수용 대역폭이 한정 대역폭을 초과 하였을때







