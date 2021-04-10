import cv2
import numpy as np
from pyzbar.pyzbar import decode
import mysql.connector
import time

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="bem"
)

# img = cv2.imread('1.png')
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

data = 0
while True:
    Data =""
    success, img = cap.read()
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        print(myData)
        Data = myData.split(", ")
        warehouse = Data[0]
        tenant = Data[1]
        po = Data[2]
        invoice = Data[3]
        mcode = Data[4]
        status = Data[5]
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, (255, 0, 255), 5)
        pts2 = barcode.rect
        cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,0.9, (255, 0, 255), 2)

        mycursor = mydb.cursor()

        sql = "INSERT INTO tesship (warehouse, tenant, po, invoice, mcode, status) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (warehouse, tenant, po, invoice, mcode, status)
        run = mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")

        if Data != "":
            time.sleep(3)

    cv2.imshow('Result', img)
    cv2.waitKey(1)