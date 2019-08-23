#asdsansldasd
import update_bandwidth
if __name__ == "__main__":
    UB = update_bandwidth.UpdateBandwidth()
    UB.update_page()
    in_bw , stream_meta = UB.get_data()
    print(in_bw)
    print( stream_meta)