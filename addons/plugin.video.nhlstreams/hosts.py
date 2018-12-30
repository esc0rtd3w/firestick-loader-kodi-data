__author__ = 'Jason Vanzin'
import sys #used to get commandline arguments
import re #used for regular expressions
hostname = 'mf.svc.nhl.com'
ipaddress = '104.251.218.27'
def exists(hostname):
    try:
        if 'darwin' in sys.platform:
            filename = '/private/etc/hosts'
        elif 'linux' in sys.platform:
            filename = '/etc/hosts'
        elif 'win' in sys.platform:    
            filename = 'c:\windows\system32\drivers\etc\hosts'
        else:
            return
        f = open(filename, 'r')
        hostfiledata = f.readlines()
        f.close()
        for item in hostfiledata:
            if hostname in item:
                return True
        return False
    except:
        return

def update(ipaddress, hostname):
    try: 
        if 'darwin' in sys.platform:
            try:
                filename = '/private/etc/hosts'
                outputfile = open(filename, 'a')
                entry = "\n" + ipaddress + "\t" + hostname + "\n"
                outputfile.writelines(entry)
                outputfile.close()
                return
            except:
                cmd = "echo '104.251.218.27'+'\t'+'mf.svc.nhl.com'+'\n' | sudo tee -a /etc/hosts"
                os.system(cmd)
                return
        elif 'linux' in sys.platform:
            filename = '/etc/hosts'
        elif 'win' in sys.platform:    
            filename = 'c:\windows\system32\drivers\etc\hosts'
        else:
            return
        outputfile = open(filename, 'a')
        entry = "\n" + ipaddress + "\t" + hostname + "\n"
        outputfile.writelines(entry)
        outputfile.close()
    except:
        return

def validIP(ipaddress):
    try: 
        parts = ipaddress.split(".")
        if len(parts) != 4:
            return False
        if ipaddress[-2:] == '.0': return False
        if ipaddress[-1] == '.': return False
        for item in parts:
            if not 0 <= int(item) <= 255:
                return False
        return True
    except:
        return

def isValidHostname(hostname):
    try:  
        if len(hostname) > 255:
            return False
        if hostname[0].isdigit(): return False
        if hostname[-1:] == ".":
            hostname = hostname[:-1] # strip exactly one dot from the right, if present
        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))
    except:
        return

def main():
    
    hostname = 'mf.svc.nhl.com'
    ipaddress = '104.251.218.27'
    try:
        if not validIP(ipaddress): #checks the IP address to see if it's valid.
            print(ipaddress, "is not a valid IP address. Usage: hostfileupdate.py [ipadddress] [hostmame]")
            sys.exit(2)

        if not isValidHostname(hostname): #checks the host name to see if it's valid.
            print(hostname, "is not a valid hostname. Usage: hostfileupdate.py [ipadddress] [hostmame]")
            sys.exit(2)

        if exists(hostname): #checks to see if the host name already exists in the host file and exits if it does.
            print(hostname, 'already exists in the hostfile.')
            sys.exit(2)

        update(ipaddress, hostname) #Calls the update function.
    except:
        return

if __name__ == '__main__':
    main()
