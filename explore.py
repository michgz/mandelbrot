

import os
from PIL import Image
import tkinter as tk       
import itertools
import math
import time
import datetime
import random






def process(box=(-2.5, 1.5, 1.5, -1.5), fn="2.png", k_num = 256):


    # Program "mandel.x86" is compiled from the code at :
    #       https://github.com/skeeto/mandel-simd
    #
    os.system("./mandel.x86 -w 1440 -h 1080 -d 256 -x {0}:{2} -y {3}:{1} -k {4} > m.txt".format(*box, k_num))




    b = open("m.txt", "rb").read()
    b = b[17:]

    i = 0
    j = 0

    SS = set()

    while i < len(b):
        c = b[i:i+3]
        if not (c[0] == c[1] and c[1] == c[2]):
            print(c.hex(" "))
        else:
            SS.add(c[0])
        i += 3
        j += 1

    #print(SS)


    #print(f"Total {j}")





    p = Image.new("L", (1440,1080))

    for x in range(1440):
        for y in range(1080):
            p.putpixel((x,y), b[3 * (x + 1440*(1079-y))])


    p.save(fn)
    #p.show()




def process_josch(center=(0.,0.), magn=1., fn_root="1"):
  
    t_1 = time.monotonic()
  
    os.system("./mandel_mpfr 1440 1080 {0:f} {1:f} {2} > tmp.ppm".format(center[0], center[1], magn))

    t_2 = time.monotonic()
    
    with open(fn_root + "_Info.txt", "w") as f1:
        f1.write("Calculated {0}\n".format(datetime.datetime.now().isoformat()))
        f1.write("Time taken: {0:f} second\n".format(t_2 - t_1))
        f1.write("Center: ( {0:f}, {1:f} )\n".format(*center))
        f1.write("Magnification: {0:f}\n".format(magn))
        
    img = Image.open("tmp.ppm")
    img.save(fn_root + ".png")






last_pos = None

old_box = (-2.5,1.5,1.5,-1.5)

new_box = None

kk = 256


for i in itertools.count(1):


    new_box = None
    
    file_name = None

    if False:
        # Fast, but only to 10^5 magnification
        file_name = "{0}.png".format(i)
        process(old_box, file_name, k_num = kk )
    else:
        # Slow, but arbitrary magnification
        file_name = "{0:07x}".format(random.randint(0,0xFFFFFFF))
        process_josch(center=((old_box[1]+old_box[0])/2., (old_box[3]+old_box[2])/2.), magn=4./(old_box[1]-old_box[0]), fn_root=file_name)
        file_name += ".png"
    


    def __btnDown(event):
        global last_pos
        last_pos = (event.x, event.y)
        
        
    def __btnUp(event):
        global last_pos
        global new_box
        if last_pos is not None:
            if event.x > last_pos[0] and event.y > last_pos[1]:
              
                new_box_ = [0.,0.,0.,0.]
                
                new_box_[0] = old_box[0] + (old_box[2] - old_box[0])*float(last_pos[0] - 0)/(1440.)
                new_box_[1] = old_box[3] + (old_box[1] - old_box[3])*float((1079-last_pos[1]) - 0)/(1080.)
                new_box_[2] = old_box[0] + (old_box[2] - old_box[0])*float(event.x - 0)/(1440.)
                new_box_[3] = old_box[3] + (old_box[1] - old_box[3])*float((1079-event.y) - 0)/(1080.)
                
                new_box = tuple(new_box_)
                
                print("(X={0}, Y={1})  --  (X={2}, Y={3})".format(*new_box))
                
              
            last_pos = None


    def __pos(event):
        new_box_ = [0., 0.]
        
        new_box_[0] = old_box[0] + (old_box[2] - old_box[0])*float(event.x - 0)/(1440.)
        new_box_[1] = old_box[1] + (old_box[3] - old_box[1])*float((1079-event.y) - 0)/(1080.)
        
        print("X: {0}, Y: {1}".format(new_box_[0] ,new_box_[1] ))


    ws = tk.Tk()
    ws.title('Mandelbrot Explorer')


    img = tk.PhotoImage(file=file_name)
    p = tk.Label(
        ws,
        image=img
    )

    p.pack()

    p.bind('<Button-1>', __btnDown)
    p.bind('<ButtonRelease-1>', __btnUp)
    #p.bind('<Motion>', __pos)

    ws.mainloop()
    
    
    print(new_box)
    
    if new_box is None:
        break
    else:
        # Fix the aspect ratio to 1440:1080
        
        m_1 = (new_box[2] - new_box[0])/1440.
        m_2 = (new_box[1] - new_box[3])/1080.
      
        m_max = max(m_1, m_2)
      
        x_cent = (new_box[2] + new_box[0])/2.
        y_cent = (new_box[1] + new_box[3])/2.
        
        
      
      
        old_box = ( x_cent-m_max*720.,  y_cent+m_max*540.  , x_cent+m_max*720. ,   y_cent-m_max*540.)
        
        
        mag = math.log10(0.002777778/m_max)
        if mag > 4:
            kk = 1024
        if mag > 6:
            kk = 4196
        
        print("    Magnification = 10^{0:0.3f}".format(mag))
        
        
        new_box = None
    







