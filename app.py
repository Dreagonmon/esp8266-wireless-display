import gc

# debug function
def free():
    gc.collect()
    # print('Mem Remain:', gc.mem_free(), 'Bytes')
    return gc.mem_free()

def timed_function(f, *args, **kwargs):
    myname = str(f)
    def new_func(*args, **kwargs):
        import utime
        print('Function [{}] Start'.format(myname))
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        print('Function [{}] Time = {:6.3f}ms'.format(myname, delta/1000))
        return result
    return new_func

def timed_function_async(f, *args, **kwargs):
    myname = str(f)
    async def new_func(*args, **kwargs):
        import utime
        print('Function [{}] Start'.format(myname))
        t = utime.ticks_us()
        result = await f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        print('Function [{}] Time = {:6.3f}ms'.format(myname, delta/1000))
        return result
    return new_func
