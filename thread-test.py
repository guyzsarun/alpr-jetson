import time

import threading
import cv2
'''
A Dummy function that accepts 2 arguments i.e. Filename and encryption type
and sleeps for 5 seconds in a loop while printing few lines.
This is to simulate a heavey function that takes 10 seconds to complete
'''
def loadContents(fileName, encryptionType):
    print('Started loading contents from file : ', fileName)
    print('Encryption Type : ', encryptionType)
    for i in range(5):
       print('Loading ... ')
       time.sleep(1)
    print('Finished loading contents from file : ', fileName)

def check_thread_alive(thr):
    thr.join(timeout=0.0)
    return thr.is_alive()

def main():
    cap = cv2.VideoCapture(0)
    # Create a thread from a function with arguments
    th = threading.Thread(target=loadContents, args=('users.csv','ABC' ))
    # Start the thread
    # print some lines in main thread
    th.start()
    while(1):
        ret_val, img = cap.read()

        if not check_thread_alive(th):
            print('THread DEAD')
            th = threading.Thread(target=loadContents, args=('users.csv','ABC' ))
            th.start()
        else:
            pass

        cv2.imshow("CSI Camera", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    # Wait for thread to finish

if __name__ == '__main__':
   main()