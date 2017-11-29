import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PATH = "/root/watchme/"
FILE = "hello"

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        #print event.event_type
        #print event.is_directory
        #print event.src_path
        if (event.is_directory == False) & (event.src_path == PATH+FILE ):
            print("Do something with our file")


if __name__ == "__main__":

    path = PATH
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()