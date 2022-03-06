

import os
import os.path
from PIL import Image
import tkinter as tk       
import itertools
import math
import time
import datetime
import random



def GetX(ptX : int, box=(-0.5, 0.0, 1.0)):
    return (box[0] + (float(ptX)-720.)/2./720.*4.0/box[2])

def GetY(ptY : int, box=(-0.5, 0.0, 1.0)):
    return (box[1] - (float(ptY)-540.)/2./540.*4.0*1080./1440./box[2])
    
    


def process(box=(-0.5, 0.0, 1.0), fn="2.png", k_num = 256):


    # Program "mandel.x86" is compiled from the code at :
    #       https://github.com/skeeto/mandel-simd
    #
    os.system("./mandel.x86 -w 1440 -h 1080 -d 256 -x {0}:{2} -y {3}:{1} -k {4} > m.txt".format(
                      GetX(0, box),
                      GetY(0, box),
                      GetX(1439, box),
                      GetY(1079, box),
                      k_num))




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
    # Program "mandel_mpfr" is compiled from code provided online at:
    #     https://github.com/josch/mandelbrot
    #
    # See "build_josch.py"
  
  
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




USE_SKEETO = False
USE_JOSCH = False



USE_BOX = False
  # If True, the user "lassos" a rectangle on the render that defines the extent
  #   of the next render.
  #
  # If False, the user simply clicks somewhere on the render. The next render will
  #   be a fixed magnification larger, centered on the point of the click.





if os.path.isfile("mandel_mpfr"):
    USE_JOSCH = True
elif os.path.isfile("mandel.x86"):
    USE_SKEETO = True
else:
    raise Exception("Need either mandel_mpfr or mandel.x86 program to work")





down_pos = None
up_pos = None




old_box = (-0.5, 0.0, 1.0)
  # A thruple, consisting of the following data:
  #    - X-coord, center of rendering
  #    - Y-coord, center of rendering
  #    - Magnification; relative to width of rendering being 4.0 and height
  #               being 3.0
  #



new_box = None

kk = 256




for i in itertools.count(1):


    new_box = None
    
    file_name = None

    if USE_SKEETO:
        # Fast, but only to 10^5 magnification
        file_name = "{0}.png".format(i)
        process(old_box, file_name, k_num = kk )
    elif USE_JOSCH:
        # Slow, but arbitrary magnification
        file_name = "{0:07x}".format(random.randint(0,0xFFFFFFF))
        process_josch(center=(old_box[0], old_box[1]), magn=old_box[2], fn_root=file_name)
        file_name += ".png"
    


    def __btnDown(event):
        global down_pos
        down_pos = (event.x, event.y)
        
        
        
        
    def __btnUp(event):
        global down_pos
        global up_pos
        
        
        if down_pos is not None:
            up_pos = (event.x, event.y)
        


    def __pos(event):
      
      
        print("   (  {0:f} ,   {1:f}   )".format(
                      GetX(event.x, old_box),
                      GetY(event.y, old_box)))




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

    down_pos = None
    up_pos = None


    ws.mainloop()
    
    
    new_box = None
    
    if USE_BOX:
        # New rendering based on the box traced out with the mouse
        
        if down_pos is not None and up_pos is not None:
            
            
            if up_pos[0] > down_pos[0] and up_pos[1] > down_pos[1]:
            
            
                     
                
            
                # Fix the aspect ratio to 1440:1080
                m_1 = (up_pos[0] - down_pos[0])/1440.
                m_2 = (up_pos[1] - down_pos[1])/1080.
          
                m_max = max(m_1, m_2)
                
                x_cent = GetX(    float(up_pos[0] + down_pos[0])/2.0,   old_box)
                y_cent = GetY(    float(up_pos[1] + down_pos[1])/2.0,   old_box)
                
                new_magn = old_box[2] / m_max
                
                new_box = (x_cent, y_cent, new_magn)
            
        
    else:
      
        # New rendering is a fixed multiple of the last magnification, at the
        # center point clicked on with the mouse.
      
        FIXED_MAGN_FACTOR  = 5.
      
        if down_pos is not None:
          
            new_box = (   GetX(down_pos[0], old_box),
                          GetY(down_pos[1], old_box),
                          old_box[2] * FIXED_MAGN_FACTOR  )
    
    
    
    
    print(new_box)
    
    if new_box is None:
        break
    else:
        
        old_box = new_box
        
        
        mag = math.log10( new_box[2] )
        if mag > 4:
            kk = 1024
        if mag > 6:
            kk = 4196
        
        print("    Magnification = 10^{0:0.3f}".format(mag))
        
        
        new_box = None
    







