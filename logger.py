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
    set_log_entry_event_length_limiter = 35 #used to format the log so that we can easily read it. This is *fixed* length all log entries will be. 
    with open('log.txt', 'a') as f: #original code had it re-write the entire file each time with a list, which seemed very in-efficient and like it would cause memory issues. I am not sure though, how this append works. If it accepts the entire .txt file into memory, the original implemention might have been superior. 
       # removing ''
       k = str(key).replace("'", "")
       k = check_special_keys(k)
       ts = time.time()

       if((len(k) < set_log_entry_event_length_limiter)): #only doing this to format the k string to be set_log_entry_event_length_limiter chars long
              for i in range(0,set_log_entry_event_length_limiter-len(k)): #if string is < set_log_entry_event_length_limiter long, then we will fill it up with a bunch of extra white spaces to format it for the log file. 
                    k = k+" "
       if(len(k)> set_log_entry_event_length_limiter):
             k = k[0:set_log_entry_event_length_limiter] #ensures that very large strings will simply be trimmed to fit the desired length of a log entry
       f.write("\n" + k + " - Time: " + ("%.5f" % round(ts-start_time, 2)) ) #only need so much data here about the time stamps, and this will be a 'greedy' source of storage for the log file
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
