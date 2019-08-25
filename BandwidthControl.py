from threading import Thread
import time
import update_bandwidth
import paho.mqtt.publish as publish
import urllib.request


priority = {"face_recognition" : 3, "object_detection" : 2, "qr_code" : 1}
HighResolution = [] # 요구 해상도로 올려져 있을 경우 해당 카메라가 추가되는 리스트
Maxcount = 0
MaxBandwidth = 100
total = 0
threadstate = False

total_prev = 0
error_occured = False

channel_down = False

class Control(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        global threadstate, Maxcount, MaxBandwidth,total_prev,total
        index = 0
        temp_channel = ""
        try:
            while threadstate and (total_prev != total):
                if index == Maxcount:
                    index = 0


                if temp_channel in HighResolution:
                    temp_channel = HighResolution[index]
                    msgs = \
                        [
                            {
                                'topic': HighResolution[index],
                                'payload': "down"
                            }
                        ]
                    print("down Channel : " + HighResolution[index])
                    publish.multiple(msgs, hostname="192.168.0.17")
                    channel_down = True

                time.sleep(3)

                if temp_channel in HighResolution:
                    msgs = \
                        [
                            {
                                'topic': HighResolution[index],
                                'payload': "up"
                            }
                        ]
                    print("up Channel : " + HighResolution[index])
                    publish.multiple(msgs, hostname="192.168.0.17")
                    channel_down = False
                    index += 1

                time.sleep(0.1)
        except IndexError:
            if channel_down:
                msgs = \
                    [
                        {
                            'topic': temp_channel,
                            'payload': "up"
                        }
                    ]
                print("up Channel : " + temp_channel)
                publish.multiple(msgs, hostname="192.168.0.17")

            print("Thread explode")
            threadstate = False


# fps를 낮춰주는 스레드
# def controll_fps_thread():
#     global threadstate, Maxcount, MaxBandwidth
#     index = 0
#     while threadstate:
#         try:
#             if index == Maxcount:
#                 index = 0
#             msgs = \
#             [
#                 {
#                     'topic': HighResolution[index],
#                     'payload': "down"
#                 }
#             ]
#             print("down Channel : " + HighResolution[index])
#             publish.multiple(msgs, hostname="192.168.0.17")
#             time.sleep(3)
#             msgs = \
#                 [
#                     {
#                         'topic': HighResolution[index],
#                         'payload': "up"
#                     }
#                 ]
#             publish.multiple(msgs, hostname="192.168.0.17")
#             index += 1
#
#             time.sleep(0.1)
#         except IndexError:
#             threadstate = False

if __name__ == "__main__":
    global total, total_prev
    while True:
        try:
            UB = update_bandwidth.UpdateBandwidth()
            UB.update_page()
            in_bw, stream_meta = UB.get_data()
            total = in_bw[0]
            if total_prev != total:
                print("current In Bandwidth : " + str(total))

                #사람 동작하다가 빠질때 아무거나 하나라도 빠지면 -> HighResolution 에서 제거 -> IndexError 유도
                for camera in stream_meta.keys():
                    if stream_meta[camera][0] == '160':
                        if camera in HighResolution:
                            # msgs = \
                            #     [
                            #         {
                            #             'topic': camera,
                            #             'payload': "reset"
                            #         }
                            #     ]
                            # publish.multiple(msgs, hostname="192.168.0.17")
                            HighResolution.remove(camera)
                            threadstate = False
                    elif camera not in HighResolution:
                        HighResolution.append(camera)

                #total 값이 넘어갈때 제어 -> Thread로 들어감
                if ((MaxBandwidth < total) and (not threadstate)):
                    templist = []
                    for x in priority.keys():
                        if x in HighResolution:
                            templist.append(x)
                    for y in range(len(templist)):
                        HighResolution[y] = templist[y]
                    Maxcount = len(HighResolution)
                    threadstate = True
                    t1 = Control()
                    t1.start()

                total_prev = total
                error_occured = False

            time.sleep(0.1)
        except AttributeError:
            if not error_occured:
                print("Loading 중 입니다.")
            error_occured = True
        except TimeoutError:
            if not error_occured:
                print("연결이 끊겼습니다. 잠시만 기다려주세요")
            error_occured = True
        except urllib.error.URLError:
            if not error_occured:
                print("연결이 끊겼습니다. 잠시만 기다려주세요22")
            error_occured = True
# 수용 대역폭이 한정 대역폭을 초과 하였을때







