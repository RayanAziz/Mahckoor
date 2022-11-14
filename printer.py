from colorama import Fore, Back, Style, init
import datetime

INFO = ("    " + Back.GREEN + Style.BRIGHT + "[INFO]" + Style.RESET_ALL)
ALERT = ("   " + Back.RED + Style.BRIGHT + "[ALERT]" + Style.RESET_ALL)
WARNING = (" " + Back.YELLOW + Style.BRIGHT + "[WARNING]" + Style.RESET_ALL)
ERROR = ("   " + Back.MAGENTA + Style.BRIGHT + "[ERROR]" + Style.RESET_ALL)

isConnected = False

def cyan(text):
    return (Fore.CYAN + text + Style.RESET_ALL)
def cyan_b(text):
    return (Back.CYAN + Style.BRIGHT + text + Style.RESET_ALL)
def blue(text):
    return (Fore.BLUE + text + Style.RESET_ALL)
def red(text):
    return (Fore.RED + text + Style.RESET_ALL)
def green(text):
    return (Fore.GREEN + text + Style.RESET_ALL)
def grey(text):
    return (Style.DIM + text + Style.RESET_ALL)
def time_now(raw=False):
    if raw: # = Don't format
        return (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        return (" " + Style.DIM + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " - " + Style.RESET_ALL)
    
def print_logo(version):
    logo = """
                 @@@@@@@@@@@@@@                                  
            @@@@@@@@@@@@@@@@@@@@@@@                            
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                        
      @@@@@  @@@               @@@@@@@@@@@@@                    
             @@@            @@@     @@@@@@@@@@                 
              @@          @@@    ###  ##@@@@@@@@               
              @@@         @@       ###  @@@@@@@@@            
               @@@        @@@     ###    @@@  @@@@@@@@         
                @@@@      @@@   ##  ###   @@    @@@@@@@@@      
                  @@@       @@@@       @@@@       @@@@@@@@@@@
                   @@@@@      @@@@@@@@@@@       @@@@@@@@@@   
                     @@@@@@                 @@@@@@@            
                        @@@@@@@@@@@@@@@@@@@@@@@                
                             @@@@@@@@@@@@                      
                                                            
    @@@@@@@@          @@             @                         
    @  @@ @@   @@@@   @@@@    @@@@   @  @@   @@@     @@@    @@@
    @  @@ @@   @  @@  @@ @@  @@      @@@@   @   @   @   @  @@  
    @  @@ @@   @@@ @  @@ @@   @@@@   @  @@   @@@     @@@   @@
    
    """
    print(cyan(logo))
    print("    " + cyan_b(version + " BY RAYAN AZIZ") + "\n")