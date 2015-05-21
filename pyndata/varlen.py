from .field import Field
from .linkedfield import LinkedField

class VariableLength(object):

    def __init__(self, length, *args, **kwargs):
        super(VariableLength, self).__init__(*args, **kwargs)
        if issubclass(type(length), Field):
            self.length = LinkedField(length)
            self.linked_fields.append(self.length)
            self.varies = True
        else:
            self.length =  lambda: length
            self.varies = False

    def __set__(self, obj, value):
        super(VariableLength, self).__set__(obj, value)
        if self.varies:
            self.length.set(len(value))