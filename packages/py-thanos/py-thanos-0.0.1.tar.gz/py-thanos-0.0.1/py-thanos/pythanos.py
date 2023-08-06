import subprocess
import sys
from termcolor import colored
   

def inside_venv():
    return sys.base_prefix != sys.prefix
    
    
def pythanos():
    if not inside_venv():
        # Check if you are inside a virtual environment
        print(colored("Warning! You are outside a virtual environment. This will erase all system wide packages!", 'red'))
        sys.exit(1)
    else:
        curr_packages = subprocess.getoutput('pip --disable-pip-version-check freeze').split('\n')
        
    print("Found {} installed packages in the current virtual environment".format(len(curr_packages)))

    # TODO - add an argument to get the packages before removing them
    # TODO - ask for confirmation
    
    c = input('Press enter to continue')
        
    for package in curr_packages:
        print("Removing {}".format(package))
        command = 'pip --disable-pip-version-check uninstall {} -y'.format(package)
        print(subprocess.getoutput(command))

    print('Done! Your virtual environment is a better place now')
      
if __name__ == '__main__':
    pythanos()
