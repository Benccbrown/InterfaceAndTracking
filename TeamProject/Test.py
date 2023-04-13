#imports nessesary libraries
import cv2 #Image processing
import numpy as np #image representation
import math #maths
import mouse #controllign the mouse through code
import ctypes #getting the computer screen dimentions
import sys #system use
import io #input/output libraries
import speech_recognition as sr #for speach recognition
import threading #allow for threading the speach recognition
import time #manage timeings within the program





#Creates window
frame_wind = 'main';
cv2.namedWindow(frame_wind)

screen = np.ones((512,512,3), np.uint8)



#Captures webcam
camera = cv2.VideoCapture(0)
#initalises speech recorder
r = sr.Recognizer()
#gets the microphone to record (index 2 is my default)
mic = sr.Microphone(device_index=2)



#loads haarcascades needed for object detection within the code.
hand = cv2.CascadeClassifier('palm.xml')
smile = cv2.CascadeClassifier('smile.xml')
#Fist tracking was used as it was more reliable
fist = cv2.CascadeClassifier('Fist.xml')

ret, img = camera.read() #loads data from the webcam
#gets the screans height and width for later
width = camera.get(3)
height = camera.get(4)


#initiates variables
mx = 100; #Mouse x
my = 100; #mouse y

global shift #weather or not the interface keyboard is in shift
shift= False
global code #the code made by the user in a multi line string to be ran.
code= """"""
vcommand = ''#voice command detected

def run_code():#the code being run as a function
    global code
    print('')
    try:
        exec(code)#code executed and ran
        print("*Code Complete*")
    except:
        print("*Invalid Code*")
    code = ""#resets code after running


def button_command(command):
    command = command.lower()#sets command to lower to initialise the speech and button commands together
    global shift
    global code
    cmded = False
    #loops through all the commands and runs appropriate functions
    if (command == 'run'):
        run_code()
        cmded = True
    elif (command == 'hello world'):
        code = code + "print(\"Hello World\")"
        print("print(\"Hello World\")", end = '')
        cmded = True
    elif (command == 'load'):
        File = open("SavedCode.txt", "r")
        code = File.read()
        print(code, end = '')
        File.close()
        cmded = True
    elif (command == 'save'):
        File = open("SavedCode.txt", "w")
        File.write(code)
        print("")
        print("Code Saved")
        File.close()
        cmded = True
    elif (command == 'print(' or command == 'print'):
        code = code + "print("
        print("print(", end = '')
        cmded = True
    elif (command == 'for'):
        code = code + "for i in range("
        print("for i in range(", end = '')
        cmded = True
    elif (command == 'tab'):
        code = code + "   "   
        print("   ", end = '')
        cmded = True
    elif (command == 'line'):
        code = code + "\n"
        print("")
        cmded = True
    elif (command == 'delete'):
        code = code[:-1]
        print("")
        print("==============================")
        print(code, end = '')
        cmded = True
    elif (command == 'new'):
        code = """"""
        print("\n")
        print("=============New===============")
        cmded = True
    elif (command == 'space'):
        code = code + " "
        print(" ", end = '')
        cmded = True
    elif (command == 'shift'):
        if (shift == True):
            shift = False
        else:
            shift = True
        cmded = True
    return cmded

def Speach_Detection(r,mic):
    global vcommand
    global code
    while (True):#loops forever in the background
        try:
            
            with mic as source:
                #gets the microphone recording and adjusts for ambient sound
                r.adjust_for_ambient_noise(source)
                vcommand = ''#resets the voice command
                #gets the audio recorded from mic
                audio = r.listen(source, phrase_time_limit=4)
                #print(r.recognize_google(audio))
                vcommand = r.recognize_google(audio)#analyses the audio
            cmded = button_command(vcommand)#runs command baised off audio
            if (cmded == False):#if nto a command it is used as raw test typed
                code = code + str(vcommand)
                print(vcommand, end = '') 
        except:#voice command reset to blank if unable to be run (no audio detected)
            vcommand = ''
        

def on_mouse_event(evt,x, y,flags, buttons):
    global code
    global shift
    global vcommand
    #on mouse click (works with forced code mouse click)
    if(evt==cv2.EVENT_LBUTTONDOWN):
        #print("Clicked at " + str(x) + " : "+ str(y))
        
        #Cycles through buttons to see if one was clicked
        clicked = 0
        for i in range(len(buttons)):
            #print(buttons[i])
            if (x >= buttons[i][0] and x <= buttons[i][2]):
                if (y >= buttons[i][1] and y <= buttons[i][3]):
                    #if (i < 9):
                        #print("button: " + str(i+1) + " Pressed")
                    clicked = i+1
        
        if (clicked!= 0): #if a button was clicked
            #runs command with button command
            cmded = button_command(buttons[clicked-1][4])
            if (cmded == False):#else types button text (usuably a,b,c... ect)
                code = code + str(buttons[clicked-1][4])
                print(buttons[clicked-1][4], end = '')  
            
                
                
    


def Click(img,x,y,mx,my,clicking):
    #draws circle at mouse click with dot
    img = cv2.circle(img,(mx,my),40,(0,0,255),5)
    img = cv2.circle(img,(mx,my),4,(0,0,255),-1)
    if (clicking == False):#makes sure the user wasnt already clicking
        mouse.click()#makes mouse click when the palm is shown
        clicking = True
    return img,clicking

#function to initialise and draw each individual button
def draw_buttons(screen,x1,y1,x2,y2,buttons,text,i,x,s,text_size):
    buttons.append([x1,y1,x2,y2,text[x][i]])
    screen = cv2.rectangle(screen, (x1-2,y1-2), (x2+s,y2+s),(150,150,150), -1)#border
    screen = cv2.rectangle(screen, (x1,y1), (x2,y2),(200,200,200), -1)#button
    screen = cv2.putText(screen, text[x][i], (int(x1),int(y2-10)), cv2.FONT_HERSHEY_SIMPLEX, text_size, (0,155,255), 1, cv2.LINE_AA,)
    return buttons,screen

#draws the keyboard using its current shifted state and looping through keys
#adds special buttons aswell
def draw_Key_Board(screen, buttons,lines):
    screen = cv2.rectangle(screen, (10,110), (625,370),(60,60,60), -1)#button
    for x in range(4):
        for i in range(12):
            buttons, screen = draw_buttons(screen,20+(i*50),120+(x*50),60+(i*50),160+(x*50),buttons,lines,i,x,2,1)
    lines = [['Space','Run','Shift']]
    buttons, screen = draw_buttons(screen, 220,320,420,360,buttons,lines,0,0,2,1)
    buttons, screen = draw_buttons(screen, 430,320,600,360,buttons,lines,1,0,2,1)
    buttons, screen = draw_buttons(screen, 30,320,210,360,buttons,lines,2,0,2,1)
    return screen, buttons

#draws the rest of the command and function buttons and initalises them to the buttons array
def draw_screen(screen,buttons):
    screen = cv2.rectangle(screen, (0,0), (int(camera.get(3)),int(camera.get(4))),(100,100,100), -1)
    buttons = []
    text = [['New','Delete','For','Tab','Line','print(','7']]
    for i in range(6):
        buttons, screen = draw_buttons(screen,20+(i*100),20,100+(i*100),100,buttons,text,i,0,-2,0.8)
        
    text = [['Hello World','Load','Save']]
    for i in range(3):
        buttons, screen = draw_buttons(screen,30+(i*200),380,200+(i*200),460,buttons,text,i,0,-2,1)

    return screen,buttons



#Initialises more variables
buttons = [[]]
clicking = False
smiling = False
#the lowercase and uppercase keyboards
L_Lines = [['1','2','3','4','5','6','7','8','9','0','-','='],
             ['q','w','e','r','t','y','u','i','o','p','[',']'],
             ['a','s','d','f','g','h','j','k','l',';','\ ','#'],
             ['','z','x','c','v','b','n','m',',','.','/','']]

U_Lines = [['!','"','£','$','%','^','&','*','(',')','_','+'],
             ['Q','W','E','R','T','Y','U','I','O','P','{','}'],
             ['A','S','D','F','G','H','J','K','L',':','@','~'],
             ['','Z','X','C','V','B','N','M','<','>','?','']]


#starts the microphone thread to loop in background
thread = threading.Thread(target=Speach_Detection, args=(r,mic,), daemon=True)
thread.start()

#loops to run program
while camera.isOpened():

    #finds the bounds of the screen
    hwnd = ctypes.windll.user32.FindWindowW(0, 'main')
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))

    #sets these variables to windows relative positions on the screen
    screenX = rect.left
    screenY = rect.top

    #drawes keyboard and buttons acording the the shift state
    screen,buttons = draw_screen(screen,buttons)
    if (shift):
        screen, buttons = draw_Key_Board(screen, buttons, U_Lines)
    else:
        screen, buttons = draw_Key_Board(screen, buttons, L_Lines)
    
    
    #Main Camera
    ret, img = camera.read()

    
    #If the camera is responding
    if(ret):        
        
        cursor = cv2.imread('mouse.png' , -1)
        cursor = cv2.resize(cursor,(50,50),interpolation = cv2.INTER_AREA)
        #cursor = cv2.flip(cursor, 1)
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


        #====attempt to use edge detection to make trackign more reliable=====
        #====It worked but did not work iwth the igven haarcascades=====
        #horizontal_edge = cv2.Sobel(gray, cv2.CV_16S, 1,0, ksize=3, scale=1)
        #vertical_edge = cv2.Sobel(gray, cv2.CV_16S, 0,1, ksize=3, scale=1)
        #absx= cv2.convertScaleAbs(horizontal_edge)
        #absy = cv2.convertScaleAbs(vertical_edge)
        #edge = cv2.addWeighted(absx, 0.5, absy, 0.5,0)

        
        #Fist Tracking drawing circles
        Fists = fist.detectMultiScale(gray, 1.1, 10)
        for (x,y,w,h) in Fists:
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            #if (5 < x and x+w < width - 5):
            mx = x+int(w/2)
            #if (5 < y and y+h < height - 5):
            my = y+int(h/2)
            mouse.move(screenX+mx,screenY+my,True)

        #Palm Tracking drawing squares
        palm = hand.detectMultiScale(img, 1.1, 5)
        for (x,y,w,h) in palm:
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            screen,clicking = Click(screen,int(x+int(w/2)),int(y+int(h/2)),mx-5,my-27,clicking)

        #smile detected then the current program runs
        smiles = smile.detectMultiScale(img, 1.3, 10)
        for (x,y,w,h) in smiles:
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(150,150,0),2)
            if (smiling == False):
                smiling = True 
                run_code()
        if(len(smiles) == 0):#makes sure you carnt spam running the code
            smiling = False    

        
        if(len(palm) == 0):#can not spam clikcing
            clicking = False
        

        #Adds the mouse cursor to the interface screen
        y1, y2 = 50, 50 + cursor.shape[0]
        x1, x2 = 50, 50 + cursor.shape[1]
        y1 = my-25
        y2 = my+25
        x1 = mx-25
        x2 = mx+25
        alpha_s = cursor[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        for c in range(0, 3):
            screen[y1:y2, x1:x2, c] = (alpha_s * cursor[:, :, c] +
                                      alpha_l * screen[y1:y2, x1:x2, c])


        img = cv2.putText(img, vcommand, (20,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 1, cv2.LINE_AA,)
    


        #img = cv2.putText(img, str(str(R)+str(G)+str(B)), (325,445), cv2.FONT_HERSHEY_SIMPLEX,1, (200,200,0), 2, cv2.LINE_AA)

        #flips and resizes camera
        screen = cv2.resize(screen,(int(img.shape[1]),int(img.shape[0])),interpolation = cv2.INTER_AREA)
        


        #displays final images both screen and webcam
        h_img = cv2.hconcat([screen, img])

        cv2.imshow(frame_wind, h_img)
        #oposed too
        #cv2.imshow(frame_wind, img)
        #cv2.imshow(frame_wind, screen)
        
        #cheacks for mouse events
        cv2.setMouseCallback(frame_wind, on_mouse_event, buttons)
        
        

        #Exit function
        k = cv2.waitKey(10)
        if k == 27:  # press ESC to exit
            break
    else:
        break
camera.release() #releases camera and destroys any loose ends
cv2.destroyAllWindows()
