import weakref

class Base(type):
    meta_data = {}
    def __init__(cls,classname,bases,dict_):
        type.__init__(cls,classname,bases,dict_)
        if 'register' not in cls.__dict__:
            cls.meta_data[classname] = cls
        print cls.meta_data

    @classmethod
    def getEvent(cls,name,*args,**kwargs):
        return cls.meta_data[name](*args,**kwargs)


class_dict = dict(register=True)

base = Base("Base",(object,),class_dict)



class A(base):
    def __init__(self,*args,**kwargs):
        print "hello"

    pass

class B(base):
    pass

if __name__ == '__main__':
    print(Base.getEvent("A"))