import pynput
from pynput.keyboard import Key, Listener
import time
  
keys = []
start_time = time.time()

def on_press(key):
     
    keys.append(key)
    write_file(key)
     
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
         
    except AttributeError:
        print('special key {0} pressed'.format(key))


def check_special_keys(k):
    if(k == "!"):
           return "Shift + 1"
    
    elif(k == "@"):
           return "Shift + 2"
    
    elif(k == "#"):
           return "Shift + 3"
    
    elif(k == "$"):
           return "Shift + 4"
    
    elif(k == "%"):
           return "Shift + 5"
    
    elif(k == "^"):                                        
           return "Shift + 6"
    
    elif(k == "&"):
           return "Shift + 8"
    
    elif(k == "("):
           return "Shift + 9"
    
    elif(k == ")"):
           return "Shift + 0"
    elif(k == "`"): #invalid in the general case but its the same key in sto keybinds so meh
            return "` or ~"
    elif(k == "|"): #very specific key in my STO Keybinds file so I can do a video sychronization mark 
            global start_time  #ugly but it works and I don't care enough
            start_time = time.time()
            with open('log.txt', 'w') as f:
                  f.write("Video Synchronization Marker")
            return "| Video Synchronization Marker"
    else:
         return k
          
def write_file(key):
    with open('log.txt', 'a') as f: #original code had it re-write the entire file each time with a list, which seemed very in-efficient and like it would cause memory issues. I am not sure though, how this append works. If it accepts the entire .txt file into memory, the original implemention might have been superior. 
        # removing ''
        k = str(key).replace("'", "")
        k = check_special_keys(k)
        ts = time.time()
      
        if((len(k) < 20)): #only doing this to format the k string to be 20 chars long
              for i in range(0,35-len(k)):
                    k = k+" "

        f.write("\n" + k + " - Time: " + str(ts-start_time)) 
        # explicitly adding a space after 
        # every keystroke for readability
        f.write(' ') 
                         
def on_release(key):          
    print('{0} released'.format(key))
    if key == Key.esc:
        # Stop listener
        return False
  
with Listener(on_press = on_press,
              on_release = on_release) as listener:
    listener.join()