from unittest import TestCase

class ModuleSpecificTestCase(TestCase):
    def __init__(self, test_module):
        super(ModuleSpecificTestCase, self).__init__()
        self.test_module = test_module
        
    def shortDescription(self):
        return "%-81s%-24s" % (self.__class__.__module__ + "." + self.__class__.__name__ + ": ", self.test_module.__name__)
