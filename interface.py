import tkinter
import tkinter.filedialog
from PIL import Image,ImageTk
from torchvision import transforms as transforms
import os
import cv2
import numpy as np




win = tkinter.Tk()
win.title("Image Process")
win.geometry("1280x700")


original = Image.new('RGB', (480, 640))
save_img = Image.new('RGB', (480, 640))
count =0
img2 = tkinter.Label(win)


pointsCount = 0
tpPointsChoose = []
lsPointsChoose = []
tpPointsChoose_display = []
lsPointsChoose_display = []
roi=np.array([])
points=[]


def choose_file():
    select_file = tkinter.filedialog.askopenfilename(title='Select Image')
    e.set(select_file)
    global load
    load = Image.open(select_file)
    load_vision = transforms.Resize((512,512))(load)

    global original
    original = load_vision
    global im
    im = np.asarray(original)
    global im_mark
    im_mark=np.copy(im)

    global output
    output = np.zeros(im.shape, np.uint8)
    
    render = ImageTk.PhotoImage(load_vision)
    img  = tkinter.Label(win,image=render)
    img.image = render
    img.place(x=20,y=90)
    img2.destroy()


    
#draw circle
def draw_mark(event,x,y,flags,param):
    global points,Cur_point,Start_point,pointsCount,im_mark
    global lsPointsChoose, tpPointsChoose,lsPointsChoose_display,tpPointsChoose_display,output
    #Circle
    if event==cv2.EVENT_LBUTTONDBLCLK:
        pointsCount = pointsCount + 1
        cv2.circle(im_mark, (x,y), 2, (255, 255, 255), -1)
        if roi.size>0:
            tpPointsChoose_display.append([x,y])
            lsPointsChoose_display.append((x,y))
            lsPointsChoose.append([x+crop_Start_point[0], y+crop_Start_point[1]])  # 用于转化为darry 提取多边形ROI
            tpPointsChoose.append((x+crop_Start_point[0], y+crop_Start_point[1]))           
        else:
            tpPointsChoose_display.append([x,y])
            lsPointsChoose_display.append((x,y))
            lsPointsChoose.append([x, y]) 
            tpPointsChoose.append((x, y))
        
        
    if event==cv2.EVENT_MBUTTONDOWN:
        draw_mask()
        lsPointsChoose = []
        lsPointsChoose_display = []   
        
    if event == cv2.EVENT_RBUTTONDOWN:  # 右键点击
        if  roi.size>0:
            pointsCount = 0
            tpPointsChoose_display= []
            lsPointsChoose_display = []
            tpPointsChoose = []
            lsPointsChoose = []
            output=np.zeros(im.shape, np.uint8)
            im_mark=np.copy(roi)
        else:
            pointsCount = 0
            tpPointsChoose_display = []
            lsPointsChoose_display = []
            tpPointsChoose = []
            lsPointsChoose = []
            output=np.zeros(im.shape, np.uint8)
            im_mark=np.copy(im)  

            
    '''if event==cv2.EVENT_MBUTTONDDWON: 
        global radius    
        cv2.circle(im_mark,(x,y),radius,(255,255,255),-1)
 
    if  event == cv2.EVENT_LBUTTONDOWN:
        pointsCount = pointsCount + 1
        Start_point = [x,y]
        tpPointsChoose.append((x, y))
        points.append(Start_point)

    if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        pointsCount = pointsCount + 1
        Cur_point = [x,y]
        tpPointsChoose.append((x, y))
        # print(points)
        cv2.line(im_mark,tuple(points[-1]),tuple(Cur_point),(255,255,255),2)
        tpPointsChoose.append((x, y))
        points.append(Cur_point)
        
    if event == cv2.EVENT_LBUTTONUP:
        Cur_point=Start_point
        cv2.line(im_mark,tuple(points[-1]),tuple(Cur_point),(255,255,255),2)'''
          
def draw_mask():
    global pts,display,im_mark,output,output_mask
    
    pts = np.array([lsPointsChoose], np.int32)  # pts是多边形的顶点列表（顶点集）
    pts = pts.reshape((-1, 1, 2))
    
    pts_display = np.array([lsPointsChoose_display], np.int32)  
    pts_display = pts_display.reshape((-1, 1, 2))
    
    display = cv2.fillPoly(im_mark, [pts_display], (255, 255, 255))
    output_mask = cv2.fillPoly(output, [pts], (255, 255, 255))
    
        
def roi_crop(event,x,y,flags,param): 
    global roi,im_mark,crop_Start_point,crop_Cur_point,crop_End_point
    global im_crop

    
    if  event == cv2.EVENT_LBUTTONDOWN:
        crop_Start_point = [x,y]
        #points.append(Start_point)

    if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        crop_Cur_point = [x,y]
        #print(points)
        #points.append(Cur_point)
        
    if event == cv2.EVENT_LBUTTONUP:
        crop_End_point=crop_Cur_point
        cv2.rectangle(im_crop,(crop_Start_point[0],crop_Start_point[1]),(crop_Cur_point[0],crop_Cur_point[1]),(255,255,255),1)
        roi=im_crop[(crop_Start_point[1]+1):(crop_End_point[1]-1),(crop_Start_point[0]+1):(crop_End_point[0]-1)]
        im_mark=np.copy(roi)
    
    if event== cv2.EVENT_RBUTTONDOWN:
        im_crop=np.copy(im)
        
'''def circle_radius(x):
    global radius
    radius=x'''



#mark
def mark(): 
    global img2
    global save_img

    cv2.namedWindow('mark',cv2.WINDOW_NORMAL)
    #cv2.createTrackbar('mark_r','mark',5,50,circle_radius)
    cv2.setMouseCallback('mark',draw_mark)
    while(1):
        cv2.imshow('mark',im_mark)
        if cv2.waitKey(20) & 0xFF==27:
            break
    cv2.destroyAllWindows() 
    save= Image.fromarray(output.astype('uint8')).convert('RGB')
    save=transforms.Resize((load.size[1],load.size[0]))(save)
    vision = Image.fromarray(output.astype('uint8')).convert('RGB')
    render = ImageTk.PhotoImage(vision)
    img2.destroy()  
    img2 = tkinter.Label(image=render)
    img2.image = render
    img2.place(x=650,y=90)
    save_img = save


        
    
    
def crop():
    global im_crop
    im_crop=np.copy(im)
    
    cv2.namedWindow('crop',cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('crop',roi_crop)
    while(1):
        cv2.imshow('crop',im_crop)
        if cv2.waitKey(20) & 0xFF==27:
            break
    cv2.destroyAllWindows()
    
    im_crop=np.copy(im)
    
    save= Image.fromarray(roi.astype('uint8')).convert('RGB')
    vision = Image.fromarray(roi.astype('uint8')).convert('RGB')
    render = ImageTk.PhotoImage(vision)
    global img2
    img2.destroy()  
    img2  = tkinter.Label(image=render)
    img2.image = render
    img2.place(x=650,y=220)
    global save_img
    save_img = save    
    im_crop=np.copy(im)

'''#def set_bright():
	
	def show_bright(ev=None):
		temp = original
		new_im = transforms.ColorJitter(brightness=scale.get())(temp)
		render = ImageTk.PhotoImage(new_im)
		global img2
		img2.destroy()
		img2  = tkinter.Label(win,image=render)
		img2.image = render
		img2.place(x=650,y=90)
		global save_img
		save_img = new_im
		
	top = tkinter.Tk()
	top.geometry('250x150+420+350')
	top.title('set brightness')
	scale = tkinter.Scale(top, from_=0, to=100, orient=tkinter.HORIZONTAL,command=show_bright)
	scale.set(1)
	scale.pack()
	

#def set_contrast():
	
	def show_contrast(ev=None):
		temp = original
		new_im = transforms.ColorJitter(contrast=scale.get())(temp)
		render = ImageTk.PhotoImage(new_im)
		global img2
		img2.destroy()
		img2  = tkinter.Label(win,image=render)
		img2.image = render
		img2.place(x=650,y=90)
		global save_img
		save_img = new_im
		
	top = tkinter.Tk()
	top.geometry('250x150+420+350')
	top.title('set contrast')
	scale = tkinter.Scale(top, from_=0, to=100, orient=tkinter.HORIZONTAL,command=show_contrast)
	scale.set(1)
	scale.pack()
'''
	

def save():
    global count
    count += 1
    save_img.save('mask_'+str(count)+'.jpg')
    save_successfully()
    print('totally marked',pointsCount, 'points:',[i for i in tpPointsChoose])
    
def save_successfully():
      winNew = tkinter.Toplevel(win)
      winNew.geometry('320x120+420+350')
      winNew.title('Save Image')
      lb2 = tkinter.Label(winNew,text='Save Successfully',font=('Arial',15))
      lb2.place(relx=0.25,rely=0.2)
      btClose=tkinter.Button(winNew,text='OK',command=winNew.destroy)
      btClose.place(relx=0.45,rely=0.5)
	

e = tkinter.StringVar()
e_entry = tkinter.Entry(win,width=68, textvariable=e)
e_entry.pack()

button1 = tkinter.Button(win, text ="Select", font=('Arial',10),command = choose_file)
button1.place(x=300,y=0)

#label
label1 = tkinter.Label(win,text="Original Picture",font=('Arial',10))
label1.place(x=200,y=50)

label2 = tkinter.Label(win,text="Modified Picture",font=('Arial',10))
label2.place(x=900,y=50)



button2 = tkinter.Button(win,text="Mark",font=('Arial',10),command=mark)
button2.place(relx=0.48,rely=0.4)


button3 = tkinter.Button(win,text="Save",font=('Arial',10),command=save)
button3.place(relx=0.48,rely=0.75)

#bightness
#button4 = tkinter.Button(win,text="Brightness",command=set_bright)
#button4.place(relx=0.47,rely=0.5)


#button5 = tkinter.Button(win,text="Contrast",command=set_contrast)
#button5.place(relx=0.475,rely=0.65)

#crop
button6 = tkinter.Button(win,text="Crop",command=crop)
button6.place(relx=0.48,rely=0.25)

win.mainloop()