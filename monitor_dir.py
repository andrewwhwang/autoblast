#!/usr/bin/python
import time
import ctypes
import fasta
import lineage
import makeTree
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import Popen, PIPE

db_path = 'C:/Users/Andrew.Hwang/Desktop/fastaq2phylo/db/viruses'
directory = 'C:/data/reads/downloads/'

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        pipeline(event)

def makePic(lineage_txt):
    if os.stat(lineage_txt).st_size > 0:
        makeTree.createImg(lineage_txt)

def pipeline(event):
    #if the file is a fast5 file run the pipeline
    if event.src_path.split('.')[-1] == 'fast5':
        #convert fast5 into fasta format strings
        reads = fasta.run(event.src_path.encode('utf8'),)
        for read in reads:
            #blast the read
            blast = Popen(['sh','blast.sh', db_path, read.seq], stdout=PIPE)
            out, err = blast.communicate()
            #record the blasted result on lineage log
            lineage_str = lineage.getLinage(out[:-2], db_path.split('/')[-1])
            lineage_txt.write(lineage_str + '\n')
            lineage_txt.flush()

if __name__ == "__main__":
    #create new lineage log file
    lineage_txt = open(directory+'lineage.log', 'w')
    #create listener that does monitors folder
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()

    # initialize mouse objects
    mouse_event = ctypes.windll.user32.mouse_event
    MOUSEEVENTF_MOVE = 0x0001

    #move mouse and update phylo.png every minute
    try:
        while True:
            mouse_event(MOUSEEVENTF_MOVE, 0, 0, 0, 0)
            time.sleep(60)
            #check lineage log
            makePic(directory+'lineage.log')
    except KeyboardInterrupt:
        observer.stop()
    #stop processes when stopping
    observer.join()
    lineage_txt.close()
