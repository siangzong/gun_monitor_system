import cv2
from Lineapp.func import *

def scan_qr():
    cap = cv2.VideoCapture(0)
    qrcode = cv2.QRCodeDetector() 
    check=0
    while True:
        try:
            ret, frame = cap.read() 
            if not ret:
                print("無法接收畫面，請檢查攝像頭")
                continue  

            
            ok, data, bbox, rectified = qrcode.detectAndDecodeMulti(frame)
            if ok and data: 
                for text in data:
                    if text!=check : 
                        check=text
                        try:
                            qrcode_update(text)  
                            print(check)
                        except Exception as e:
                            print(f"更新資料庫時發生錯誤: {e}")
                        

            cv2.imshow('QR Code Scanner', frame)


            if cv2.waitKey(1) == ord('q'):
                break

        except Exception as e:
            print(f"掃描時發生錯誤: {e}")
       

    cap.release()  
    cv2.destroyAllWindows() 
