class FunctionKeyDict (dict):
    """Container class for kvp's where the key is a function.
    
    Lookup characteristics:
        Linear in the number of keys 
    
    Addition of kvps: constant time

    The primary function of this class is to map an argument matching certain 
    conditions to the appropriate value. An argument is said to be in 
    a FunctionKeyDict iff there exists a condition in the container's keys for
    which condition(event) is true. 
 
    The condition given can be any function of one argument (most
    likely returning a boolean).

    Note: this container does not guarantee in any way that only one condition will
    return true for any key being looked up. This is entirely on the programmer.
    When two or more conditions are satisfied, the first one added to the collection
    takes precedence.    
    """

    def __init__ (self, args=None):
        super(FunctionKeyDict, self).__init__()
        if args:
            if not all((len(pair) == 2 for pair in args)):
                raise ValueError("Key without value in %s" % args)

            elif not all((callable(key) for key, val in args)):
                raise ValueError("All keys must be callable")

            self._kvps = args

        else:
            self._kvps = []

    def get(self, key):
        """Find the """
        for test, val in self._kvps:
            if test(key):
                return val
        return None

    def __iter__ (self):
        return (key for key, val in self._kvps)

    def keys (self):
        return [key for key, val in self._kvps]

    def values(self):
        return [val for key, val in self._kvps]

    def items (self):
        return self._kvps

    def __getitem__ (self, key):
        val = self.get(key)
        if val:
            return val
        else:
            raise ValueError("%s not in FunctionKeyDict" % key)

    def __contains__ (self, key):
        return self.get(key) != None
    
    def __setitem__(self, key, val):
        if not callable(key):
            raise ValueError("Key %s is not callable" % key)
        else:
            self._kvps.append((key, val))

    def get_all_matching(self, key):
        """Return a list of values for whom condition(key) is true"""
        return [val for condition, val in self._kvps
                if condition(key)]

class EventHandlerDict(dict):
    """Container mapping events to handler functions.

    The purpose of this container is to provide a user friendly and transparent 
    way to map events to handler functions, either by event type or by some arbitrary 
    condition on the event. If the event being looked up matches both a contained
    event type and a condition, the value for the event type takes precedence. 
    Conditions should be callable.
    
    Usage:
       d = EventHandlerDict()
       
       #Event type
       d[MOUSEBUTTONDOWN] =  lambda x: 2
       d[MOUSEBUTTONDOWN](1) # ==> 2
       
       #Arbitrary function
       d[lambda event: event.type % 2 == 0] = lambda x: "foo"
       e = Event()
       e.type = 4
       d[e] # ==> "foo"
       e.type = 5
       d[e] # throws KeyError              
    """

    def __init__(self, args=None):
        if args:
            self._dict = dict(args)
            self._fdict = FunctionKeyDict(args)
        else:
            self._dict = dict()
            self._fdict = FunctionKeyDict()

    def __getitem__ (self, key):
        val = self.get(key)        
        if val:
            return val
        else:
            raise KeyError()

    def __setitem__(self, key, val):
        if not callable(key):
            self._dict[key] = val
        else:
            self._fdict[key] = val

    def __iter__ (self):
        for key in self._dict.keys():
            yield key
        for key in self._fdict.keys():
            yield key

    def keys(self):
        return self._dict.keys() + self._fdict.keys()

    def values(self):
        return self._dict.values() + self._fdict.values()

    def items(self):
        return self._dict.items() + self._fdict.items()
    
    def __contains__ (self, event):
        return event.type in self._dict or event in self._fdict

    def get(self, event):
        if event.type in self._dict:
            return self._dict[event.type]
        elif event in self._fdict:
            return self._fdict[event]
        else: 
            return None
            
    def get_all_matching(self, event):
        """Return all values matching event in self"""
        _dict_val = self._dict.get(event)        
        _dict_matching = [_dict_val] if _dict_val else []
        return _dict_matching + self._fdict.get_all_matching(event)
        
