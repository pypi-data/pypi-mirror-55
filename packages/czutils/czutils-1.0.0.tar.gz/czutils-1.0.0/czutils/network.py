# _*_ encoding=utf-8 _*_
#!/usr/bin/env python3

import re, logging
import requests as req
from utils.exceptions import LoadFileException

def is_url( path ):
    return re.match(r'^https?:/{2}\w.+\.\w.+$', path)

def load_network_image( path ):
    timeout = 2
    time = 0
    while True:
        try:
            response = req.get(path, timeout=timeout)
            if response.status_code != 200:
                msg = "net error:" + str(response.status_code)
                raise LoadFileException( path, msg )
            break
        except req.exceptions.Timeout as e:
            logging.warning( path + str(e) )
            timeout += 1
            if timeout > 15:
                break
            continue;
        except req.exceptions.RequestException as e:
            logging.warning( path + str(e) )
            time += 1
            if time > 10:
                break
            continue

    return response.content