from openalpr import Alpr

alpr = Alpr("us", "/etc/openalpr/openalpr.conf","/usr/share/openalpr/runtime_data")

def detect_plate(crop_frame):
    return alpr.recognize_ndarray(crop_frame)

def accum_vote(results,arr):
    for i,plate in enumerate(results[0]['candidates']):
        if plate['confidence']>0.4:
            arr.append(plate['plate'])
            if i>4:
                break
    return arr