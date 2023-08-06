from pathlib import Path
import os
import yaml
import time
import readline


home = str(Path.home())+"/.tnotes/"


def setup():
    defconfig = {
        "dir": "/tnotes/",
        "note": "firstnote"
    }
    if not os.path.isdir(home):
        os.mkdir(home)
        os.mkdir(str(Path.home())+"/tnotes/")
    else:
        print("Already done, cancelling")
        return
    f = open(home+"config.yaml", "w+")
    f.write(yaml.dump(defconfig))
    open(str(Path.home())+"/tnotes/firstnote", "w+")


if not os.path.isdir(home):
    setup()
config = yaml.safe_load(open(home+"config.yaml"))


def write(text):
    file = str(Path.home())+config["dir"]+config["note"]
    os.makedirs(os.path.dirname(file), exist_ok=True)
    f = open(file, "a+")
    f.write(yaml.safe_dump([{str(time.time()): text}]))


def edit(index, text):
    with open(str(Path.home())+config["dir"]+config["note"], "r") as f:
        y = yaml.safe_load(f)
        y[-(index+1)][str(time.time())] = text
    with open(str(Path.home())+config["dir"]+config["note"], "w") as z:
        z.write(yaml.safe_dump(y))


def read(index):
    with open(str(Path.home())+config["dir"]+config["note"], "r") as f:
        y = yaml.safe_load(f)
        y = y[-(index+1)]
        return y[max(y.keys())]


def edit_config(dictionary):
    with open(home+"config.yaml", "r") as f:
        y = yaml.safe_load(f)
    with open(home+"config.yaml", "w") as z:
        y.update(dictionary)
        z.write(yaml.safe_dump(y))


def enter(text=""): #Code taken from https://stackoverflow.com/questions/2533120/show-default-value-for-editing-on-python-input-possible and written by sth
    readline.set_startup_hook(lambda: readline.insert_text(text))
    try:
        return input()
    finally:
        readline.set_startup_hook()


def save(file):
    with open(str(Path.home())+config["dir"]+config["note"], "r") as f:
        y = yaml.safe_load(f)
        text = ""
        for x in y:
            text += "\n" + x[max(x.keys())]
        with open(file, "w+") as f:
            f.write(text)
        return
