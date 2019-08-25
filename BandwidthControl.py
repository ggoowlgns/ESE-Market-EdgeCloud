import sys
from threading import Thread
import time
import update_bandwidth
import paho.mqtt.publish as publish
import urllib.request
import paho.mqtt.client as mqtt



priority = {"face_recognition": 3, "object_detection": 2, "qr_code": 1, "face_recognition2" : 4, "qr_code2" : 5}
HighResolution = []  # 요구 해상도로 올려져 있을 경우 해당 카메라가 추가되는 리스트
Maxcount = 0
MaxBandwidth = 190
total = 0
threadstate = False

Objectstate = False
Facestate = False
QRstate = False
Facestate2 = False
QRstate2 = False

total_prev = 0
error_occured = False

channel_down = False


class ObjectMQTT(Thread):
    def __index__(self):
        Thread.__init__(self)

    def run(self):
        def on_connect(client, userdata, flags, rc):
            print("Connected with Object code " + str(rc))
            client.subscribe("object_detection")

        def on_message(client, userdata, msg):
            global HighResolution, Objectstate
            x = str(msg.payload.decode('utf-8'))
            if x == 'change_low_res' and Objectstate:
                print(x)
                HighResolution.remove("object_detection")
                Objectstate = False
            elif x == 'change_high_res' and not Objectstate:
                print(x)
                HighResolution.append("object_detection")
                Objectstate = True

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("192.168.0.17")

        client.loop_forever()


class FaceMQTT(Thread):
    def __index__(self):
        Thread.__init__(self)

    def run(self):
        def on_connect(client, userdata, flags, rc):
            print("Connected with Face " + str(rc))

            client.subscribe("face_recognition")

        def on_message(client, userdata, msg):
            global HighResolution, Facestate
            x = str(msg.payload.decode('utf-8'))
            if x == 'change_low_res' and Facestate:
                HighResolution.remove("face_recognition")
                Facestate = False
                print(x)
            elif x == 'change_high_res' and not Facestate:
                HighResolution.append("face_recognition")
                Facestate = True
                print(x)

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("192.168.0.17")

        client.loop_forever()


class QrMQTT(Thread):
    def __index__(self):
        Thread.__init__(self)

    def run(self):
        def on_connect(client, userdata, flags, rc):
            print("Connected with QR " + str(rc))

            client.subscribe("qr_code")


        def on_message(client, userdata, msg):
            global HighResolution, QRstate
            x = str(msg.payload.decode('utf-8'))
            if x == 'change_low_res' and QRstate:
                HighResolution.remove("qr_code")
                QRstate = False
                print(x)
            elif x == 'change_high_res' and not QRstate:
                HighResolution.append("qr_code")
                QRstate = True
                print(x)

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("192.168.0.17")

        client.loop_forever()


class FaceMQTT2(Thread):
    def __index__(self):
        Thread.__init__(self)

    def run(self):
        def on_connect(client, userdata, flags, rc):
            print("Connected with Face2 " + str(rc))

            client.subscribe("face_recognition2")

        def on_message(client, userdata, msg):
            global HighResolution, Facestate2
            x = str(msg.payload.decode('utf-8'))
            if x == 'change_low_res' and Facestate2:
                HighResolution.remove("face_recognition2")
                Facestate2 = False
                print(x)
            elif x == 'change_high_res' and not Facestate2:
                HighResolution.append("face_recognition2")
                Facestate2 = True
                print(x)

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("192.168.0.17")

        client.loop_forever()


class QrMQTT2(Thread):
    def __index__(self):
        Thread.__init__(self)

    def run(self):
        def on_connect(client, userdata, flags, rc):
            print("Connected with QR2 " + str(rc))

            client.subscribe("qr_code2")

        def on_message(client, userdata, msg):
            global HighResolution, QRstate2
            x = str(msg.payload.decode('utf-8'))
            if x == 'change_low_res' and QRstate2:
                HighResolution.remove("qr_code2")
                QRstate2 = False
                print(x)
            elif x == 'change_high_res' and not QRstate2:
                HighResolution.append("qr_code2")
                QRstate2 = True
                print(x)

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("192.168.0.17")

        client.loop_forever()

class Control(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global threadstate, Maxcount, MaxBandwidth, total_prev, total, Objectstate, Facestate, QRstate
        index = 0
        temp_channel = ""
        try:
            while threadstate:
                if index == Maxcount:
                    index = 0
                temp_channel = HighResolution[index]
                if temp_channel in HighResolution:
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
            if channel_down and Objectstate:
                msgs = \
                    [
                        {
                            'topic': "object_detection",
                            'payload': "up"
                        }
                    ]
                print("up Channel Final: " + "object_detection")
                publish.multiple(msgs, hostname="192.168.0.17")
            elif channel_down and Facestate:
                msgs = \
                    [
                        {
                            'topic': "face_recognition",
                            'payload': "up"
                        }
                    ]
                print("up Channel Final: " + "face_recognition")
                publish.multiple(msgs, hostname="192.168.0.17")
            elif channel_down and QRstate:
                msgs = \
                    [
                        {
                            'topic': "qr_code",
                            'payload': "up"
                        }
                    ]
                print("up Channel Final: " + "qr_code")
                publish.multiple(msgs, hostname="192.168.0.17")
            elif channel_down and Facestate2:
                msgs = \
                    [
                        {
                            'topic': "face_recognition2",
                            'payload': "up"
                        }
                    ]
                print("up Channel Final: " + "face_recognition2")
                publish.multiple(msgs, hostname="192.168.0.17")
            elif channel_down and QRstate2:
                msgs = \
                    [
                        {
                            'topic': "qr_code2",
                            'payload': "up"
                        }
                    ]
                print("up Channel Final: " + "qr_code2")
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
    Object = ObjectMQTT()
    Face = FaceMQTT()
    Qr = QrMQTT()
    Face2 = FaceMQTT2()
    Qr2 = QrMQTT2()
    Object.start()
    Face.start()
    Qr.start()
    Face2.start()
    Qr2.start()
    f = open("nosol.txt", "w")
    while True:
        try:
            UB = update_bandwidth.UpdateBandwidth()
            UB.update_page()
            in_bw, stream_meta = UB.get_data()
            if "kilo" in in_bw[1]:
                total = in_bw[0]
            elif "mega" in in_bw[1]:
                total = in_bw[0] * 2**10
            if total_prev != total:
                print("current In Bandwidth : " + str(total))
                f.write(str(total))
                f.write("\n")

                # #사람 동작하다가 빠질때 아무거나 하나라도 빠지면 -> HighResolution 에서 제거 -> IndexError 유도
                # for camera in stream_meta.keys():
                #     if stream_meta[camera][0] == '160':
                #         if camera in HighResolution:
                #             # msgs = \
                #             #     [
                #             #         {
                #             #             'topic': camera,
                #             #             'payload': "reset"
                #             #         }
                #             #     ]
                #             # publish.multiple(msgs, hostname="192.168.0.17")
                #             HighResolution.remove(camera)
                #             threadstate = False
                #     elif camera not in HighResolution:
                #         HighResolution.append(camera)

                # total 값이 넘어갈때 제어 -> Thread로 들어감
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
        except KeyboardInterrupt:
            f.close()
            print("사용 종료")
            sys.exit()
# 수용 대역폭이 한정 대역폭을 초과 하였을때







