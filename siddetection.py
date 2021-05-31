import cv2
import numpy as np
import time
from sid import utilsize # custom file
from PIL import Image
# first of all we need to load the YOLO wait,Configurations and objects name 
# We don't need to write our owan loaing function
# This function returns model objects that we can use later on for prediction

def detect(filename,go):
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

    # Extract the objects name from coco.name and put everything into list
    classes = []
    with open("coco.names",'r') as f:
        classes = f.read().splitlines()

    #print(classes)

    #from google.colab.patches import cv2_imshow

    #cap = cv2.VideoCapture('/content/drive/My Drive/ObjectDetectionv2/Road_traffic_video2.mp4') # from video
    #cap = cv2.VideoCapture(0) # from webcam
    img = cv2.imread("static/uploads/"+filename) # from image traffic.jpg cycle.jpg     traffic image imagesize:1800X1200
    if go:
        img = cv2.imread("static/sample/"+filename) # from image traffic.jpg cycle.jpg     traffic image imagesize:1800X1200
        
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    #img = cv2.resize(img, None,fx=0.4, fy=0.4)
    start_time = time.time()
    height, width, _ = img.shape

    fontthick,rectsize,fontscale,ymargin = utilsize(height,width)
            
            
    img_id = 1
    # we need to resize the image in a square 416x416 that can be fit into the Yolo3
    # and also we normalize it by dividing the pixel value by 255
    # here we use dimension 32xX here X=13 so the input size w,h=(416,416) and it's work better the bigger X is.

    blob = cv2.dnn.blobFromImage(img,1/255,(320,320),(0,0,0),swapRB=True,crop=False)
    # first image,second normalization,third dimension,fourth no any means of substraction
    # fifth swapRb = true that convert BGR to RGB,sixth no croping

    # passing this blob into our model inside a net
    net.setInput(blob)

    # get output layersname ['yolo_82', 'yolo_94', 'yolo_106']
    output_layers_names = net.getUnconnectedOutLayersNames() 

    output_all = net.getLayerNames() # to get names of all layers
    # print(output_layers_names)
    # print(output_all)

    # forward propogation
    # passing output layers names to get output at that layers
    layersOutputs = net.forward(output_layers_names)
    # we need to extract the bounding boxes
    # confidences and the predicted classes
    boxes = []
    confidences = []
    class_ids = []

    #print(layersOutputs)

    #3 boxes with box co-ordinates,confidence score,class score
    for output in layersOutputs:
        # 4 box co-ordinates + 1 confidence score + 80 class score = 85
        for detection in output:
            scores = detection[5:] # store 80 class predeictions
            class_id = np.argmax(scores) #extract highest scores indexes
            confidence = scores[class_id] 

            if confidence > 0.5:
                # Object detected
                # we have normalized img by scalefactor 1/255 
                # so co-ordinates are appropriate to that img
                # to get original, denormalize by multiplying it's original width,height 
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
            
                # Rectangle coordinates
                # extract the upper left corners positions in order to present them with use of opencv
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
            
                # append everything to draw boxes
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    #print(len(boxes))
    #third parameter is set under the confidence,last is NMS
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    #print(indexes)



    if len(indexes)>0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i],2))
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, rectsize)
            #cv2.putText(img, label, (x, y + 50), font, 5, color, 3)
            #color = colors[class_ids[i]]
            #cv2.rectangle(img, (x, y), (x + w, y + h), color, 6)
            cv2.putText(img, label + " " + confidence, (x, y + ymargin), font, fontscale, color, fontthick)

    # cv2.imshow('Image',img)  DisabledFunctionError: cv2.imshow() is disabled in Colab, 
    # because it causes Jupyter sessions to crash;
    elapsed_time = time.time() - start_time
    fps = img_id/elapsed_time
    #cv2.putText(img,"FPS: "+str(round(fps,2)),(10,30),font,3,(0,0,0),1)
    #cv2_imshow(img)
    img1 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img1 = Image.fromarray(img1)
    img1.save("static/uploads/"+filename)
    #cv2.imshow('Image',img)
    #cv2.waitKey(0)
    