import pynput
from pynput.keyboard import Listener  as KeyboardListener
from pynput.mouse    import Listener  as MouseListener
from pynput.keyboard import Key
from datetime import datetime
import time
import pyuac
import string
  
keys = []
start_time = time.time()
CURRENT_TIME = 0

def on_press(key):
     
    keys.append(key)
    write_file(key)
     
    try:
       #print('alphanumeric key {0} pressed'.format(key.char))
       pass #no need to bring things out when things are working fine, increases runtime
         
    except AttributeError:
       print('special key {0} pressed'.format(key))

def update_current_time():
      global CURRENT_TIME
      CURRENT_TIME = time.time()

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
    
    elif( k.isupper() ): #Just here to convert entries like "T" -> "Shift + t" for readability
            return ("Shift + " + k.lower())
    
    elif(k == "|"): #very specific key in my STO Keybinds file so I can do a video sychronization mark 
            global start_time  #ugly but it works and I don't care enough
            start_time = time.time()
            with open('Keyboard_Inputs_Log.log', 'w') as f:
                  f.write("Logging Session On: " + str(datetime.now()) +  " Local Time Zone" + "\nVideo Synchronization Marker")
            return "| Video Synchronization Marker"
    
    else:
         return k
          
def write_file(key): #key may not always be a 'Key' Object, it may also be a string such as in the case of the mosue listener. 
    update_current_time()
    set_log_entry_event_length_limiter = 35 #used to format the log so that we can easily read it. This is *fixed* length all log entries will be. 
    with open('Keyboard_Inputs_Log.log', 'a') as f: #original code had it re-write the entire file each time with a list, which seemed very in-efficient and like it would cause memory issues. I am not sure though, how this append works. If it accepts the entire .txt file into memory, the original implemention might have been superior. 
       # removing ''
       k = str(key).replace("'", "")
       k = check_special_keys(k)

       if((len(k) < set_log_entry_event_length_limiter)): #only doing this to format the k string to be set_log_entry_event_length_limiter chars long
              for i in range(0,set_log_entry_event_length_limiter-len(k)): #if string is < set_log_entry_event_length_limiter long, then we will fill it up with a bunch of extra white spaces to format it for the log file. 
                    k = k+" "
       if(len(k)> set_log_entry_event_length_limiter):
             k = k[0:set_log_entry_event_length_limiter] #ensures that very large strings will simply be trimmed to fit the desired length of a log entry
       f.write("\n   " + k + " - Time: " + ("%.7f" % round(CURRENT_TIME-start_time, 2)) ) #only need so much data here about the time stamps, and this will be a 'greedy' source of storage for the log file
       # explicitly adding a space after 
       # every keystroke for readability
       f.write(' ') 
                         
def on_release(key):          
    #print('{0} released'.format(key))
    if key == Key.page_down:
        # Stop listener
        return False

def on_click(x, y, button, pressed):
       if pressed:
              mouse_singal_string = ""
              if(str(button) == "Button.left" or str(button) == "Button.right"):#only really care about coordinates here when left or right pressing, so this only sends over 
                    mouse_singal_string = str(button) + "@x=" + str(x) + "y=" + str(y) 
              else:
                    mouse_singal_string = button

              write_file(mouse_singal_string)
              #note, that write_file() takes a key object input, but it can still be accepted as a string, and the function automatically converts said inputs to string anyways

#Running as Admin is nessecary in many games for whatever unknown reason. Cursory research seems to indicate issues with DirectX and Windows but honestly who knows :shrugs_non-chalantly:
def main():
       with MouseListener(on_click=on_click) as listener:
              with KeyboardListener(on_press = on_press, on_release = on_release) as listener:
                     listener.join()
    
if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
    else:        
        main()  # Already an admin here.
