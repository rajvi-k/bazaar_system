import pickle
import os
from threading import Lock

cache_lock = Lock()


# caching for all the requests, this function returns the result if present in cache or otherwise executes the
# function and then returns the response and caches it
def cached(cachefile):
    """
    A function that creates a decorator which will use "cachefile" for caching the results of the decorated function "fn".
    """

    def decorator(fn):  # define a decorator for a function "fn"
        def wrapped(*args, **kwargs):  # define a wrapper that will finally call "fn" with all arguments
            # extract item number from arguments
            item_number = ''
            for k, v in kwargs.items():
                item_number = v

            if item_number =='' and len(args)!=0:

                item_number=args[0]



            # if cache exists -> load it and return its content
            if os.path.exists(cachefile) and os.path.getsize(cachefile) > 0:
                cache_lock.acquire()
                with open(cachefile, 'rb') as cachehandle:
                    c = pickle.load(cachehandle)

                    if item_number in c:
                        print("using cached result from '%s'" % cachefile, args, c)
                        cache_lock.release()
                        print("Returning ", c[item_number])
                        return c[item_number]

                    else:
                        print("Request Not found in cache")
                        # execute the function with all arguments passed
                        res = fn(*args, **kwargs)
                        # write to cache file
                        with open(cachefile, 'wb') as cachehandle:
                            print("saving result to cache '%s'" % cachefile, args, c)
                            c[item_number] = res
                            pickle.dump(c, cachehandle, protocol=pickle.HIGHEST_PROTOCOL)
                        cache_lock.release()
                        print("Returning ", res)
                        return res


            else:
                print("Request Not found in cache")
                c = {}
                res = fn(*args, **kwargs)
                cache_lock.acquire()

                with open(cachefile, 'wb') as cachehandle:
                    print(" create cache '%s'" % cachefile)
                    c[item_number] = res
                    pickle.dump(c, cachehandle, protocol=pickle.HIGHEST_PROTOCOL)
                cache_lock.release()
                print("Returning ", res)
                return res

        # Renaming the function name:
        wrapped.__name__ = fn.__name__
        return wrapped

    return decorator
