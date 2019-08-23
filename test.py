#asdsansldasd
import update_bandwidth
import urllib.request

if __name__ == "__main__":
    UB = update_bandwidth.UpdateBandwidth()

    while True:
        try:
            UB.update_page()
            in_bw, stream_meta = UB.get_data()
            print(in_bw)
            print( stream_meta)
            print()
        except AttributeError:
            print("로딩중 입니다.")
        except TimeoutError:
            print("연결이 끊겼습니다. 잠시만 기다려주세요")
        except urllib.error.URLError:
            print("연결이 끊겼습니다. 잠시만 기다려주세요22")