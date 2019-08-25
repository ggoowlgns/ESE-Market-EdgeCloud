#asdsansldasd
import sys
import time
import update_bandwidth
import urllib.request
total = 0

if __name__ == "__main__":
    UB = update_bandwidth.UpdateBandwidth()
    f = open("nosol.txt", "w")
    while True:
        try:
            UB.update_page()
            in_bw, stream_meta = UB.get_data()
            if "kilo" in in_bw[1]:
                total = in_bw[0]
            elif "mega" in in_bw[1]:
                total = in_bw[0] * 2**10
            f.write(str(total))
            f.write("\n")
            time.sleep(0.1)
        except AttributeError:
            print("로딩중 입니다.")
        except TimeoutError:
            print("연결이 끊겼습니다. 잠시만 기다려주세요")
        except urllib.error.URLError:
            print("연결이 끊겼습니다. 잠시만 기다려주세요22")
        except KeyboardInterrupt:
            f.close()
            print("사용 종료")
            sys.exit()