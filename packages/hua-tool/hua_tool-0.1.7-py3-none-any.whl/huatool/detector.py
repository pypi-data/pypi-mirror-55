import huatool as HT

class Timer(HT.ContextDecorator):
    '''函数执行时间侦测'''
    def __init__(self, title='Function', context='executing time: %.2f seconds.', enter_msg='', exit_msg=''):
        self.title = title
        self.context = context
        self.enterMsg = enter_msg
        self.exitMsg = exit_msg
    def __enter__(self):
        self.enterTime = HT.DateTime.datetime.now()
        if self.enterMsg and self.enterMsg != '': print(self.enterMsg)
    def __exit__(self, *args):
        self.exitTime = HT.DateTime.datetime.now()
        if self.exitMsg and self.exitMsg != '': print(self.exitMsg)
        self.elapseTime = (self.exitTime - self.enterTime).total_seconds()
        print('[%s] %s' % (self.title, self.context % (self.elapseTime)))

def timer(funct, kwargs, title='Function', context='executing time: %.2f seconds.', enter_msg='', exit_msg=''):
    '''函数执行时间侦测'''
    @Timer(title=title, context=context, enter_msg=enter_msg, exit_msg=exit_msg)
    def inner(funct, kwargs):
        funct(**kwargs)
    inner(funct, kwargs)
