# -*- encoding=utf-8 -*-
# !/usr/bin/env python3

import multiprocessing, logging
import utils.network as nw

class ImageLoader():
    def __init__( self, count ):
        self.queue = multiprocessing.Queue()
        self.processes = []
        for i in range(count):
            process = multiprocessing.Process(target=self._load)
            self.processes.append(process)        
            process.start()

    def _load(self):
        while True:
            args = self.queue.get();
            
            if args[0] == 'stop':
                print( "stop process" )
                return args[1]

            image = args[0]
            path = args[1]
            err_func = args[2]
            arg = args[3]
            try:
                image_content = nw.load_network_image( image )
                with open( path, 'wb' ) as f:
                    f.write( image_content )
            except Exception as e:
                if err_func != None:
                    err_func(arg)
                logging.warning( "loading image %s failed. %s " %( image, str(e) ) )

    def load_image(self, image, save_path, fun=None, *args):
        self.queue.put((image, save_path, fun, args))

    def destroy(self):
        for p in self.processes:
            self.queue.put(('stop', 0))
        for p in self.processes:
            p.join()

if __name__ == '__main__':
    image_loader = ImageLoader(6)
    for i in range(30): 
        image_loader.load_image("http://mtime-1252014125.file.myqcloud.com/img/goods/fdc33d11d8694d90b6b314c78a69025c.png", str(i)+"123.txt")
    image_loader.destroy()