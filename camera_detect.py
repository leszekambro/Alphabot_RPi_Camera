# import bibliotek
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import cv2.cv as cv
import numpy as np

# inicjalizacja kamery
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# 
time.sleep(0.1)
# pobieranie pojedynczych klatek z obrazu
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# pobierz tablice reprezentujaca obraz
	# 
	image = frame.array
	output = image.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#szukamy okregow na obrazie
	circles = cv2.HoughCircles(gray, cv.CV_HOUGH_GRADIENT, 1.2, 100)
	if circles is not None:
	# przeksztalc wspolrzedne (x, y) i promienie okregow na liczby calkowite
		circles = np.round(circles[0, :]).astype("int")
		# 
		for (x, y, r) in circles:
			# narysuj okrag na obrazie wyjsciowym
			# 
			cv2.circle(output, (x, y), r, (0, 255, 0), 4)
			cv2.circle(output, (x, y), 3, (255, 0, 0), 2)
			# wyswietl wspolrzedne srodka okregu na obrazie
			cv2.putText(output, text="x={}, y= {}".format(x, y), org=(x, y), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 255),thickness=2)
			# wyswietl wspolrzedne srodka okregu w terminalu
			print(x,y)
	# show the frame
	cv2.imshow("Frame", image) # wyswietl surowy obraz RGB
	cv2.imshow("gray", gray)# wyswietl obraz w odcieniach szarosci
	cv2.imshow("output", output)# wyswietl obraz z zaznacoznymi okregami
	
	
	
	key = cv2.waitKey(1) & 0xFF
	# przygotowanie do pobrania nastepnej klatki/czyszczenie strumienia video
	rawCapture.truncate(0)
	# jesli `q` wcisniety, wyjdz z petli
	if key == ord("q"):
		break
