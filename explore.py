

import os
from PIL import Image
import tkinter as tk       
import itertools






def process(box=(-2.5, 1.5, 1.5, -1.5), fn="2.png"):


    # Program "mandel.x86" is compiled from the code at :
    #       https://github.com/skeeto/mandel-simd
    #
    os.system("./mandel.x86 -w 1440 -h 1080 -d 256 -x {0}:{2} -y {3}:{1} -k 256 > m.txt".format(*box))




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





last_pos = None

old_box = (-2.5,1.5,1.5,-1.5)

new_box = None


for i in itertools.count(1):


    new_box = None

    process(old_box, "{0}.png".format(i))


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


    img = tk.PhotoImage(file='{0}.png'.format(i))
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
        old_box = new_box
        new_box = None
    







