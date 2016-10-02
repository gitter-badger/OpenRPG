
class Component(object):
    '''
        Interface for a renderable component of a character
    '''

    def getCode(self):
        '''
            Must return JavaScript code for rendering the component
        '''
        raise NotImplementedError()
