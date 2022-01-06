import importlib
import os

def installPip():
    #-----INSTALL PIP IF NOT INSTALLED-----
    try: # https://stackoverflow.com/questions/12373563
        if os.system('pip -V') != 0:
            raise Exception
    except:
        print("b")
        os.system("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
        os.system("python3 get-pip.py")
        os.remove("get-pip.py")

def pipin(*mods):
    mods = [m for m in mods]
    unable = []
    for mod in mods:
        try:
            if os.system("pip install "+mod) != 0:
                raise Exception
        except:
            try:
                if os.system("pip3 install "+mod) != 0:
                    raise Exception
            except:
                try:
                    if os.system("python -m pip install "+mod) != 0:
                        raise Exception
                except:
                    try:
                        if os.system("python3 -m pip install "+mod) != 0:
                            raise Exception
                    except:
                        unable.append(mod)

    if (not unable):
        return 0  # print("\nInstallation COMPLETE!\n")
    else:
        print("\nFailed to install: "+" , ".join(unable)+"\n")
        return 1