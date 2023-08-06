# _*_ encoding=utf-8 _*_
#!/usr/bin/env python3

import functools, time

def time_cost( info ):
    def decorator(fn):
        @functools.wraps(fn)
        def print_time(*args, **kw):
            start = time.time()
            r = fn(*args, **kw)
            print( "%s cost time %d s" %(info, time.time()-start))
            return r
        return print_time
    return decorator


def singleton(obj):
    objs = {}
    @functools.wraps(obj)
    def decorator(*args, **kw):
        if obj not in objs:
            objs[obj] = obj(*args, **kw)
        return objs[obj]
    return decorator


if __name__ == '__main__':
    @time_cost( "if you test")
    def test():
        print( ">>>>>>>>>>>" );
        return 1, 2
    print(test())

