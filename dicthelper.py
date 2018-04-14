# Adapted: https://stackoverflow.com/questions/29033259/how-to-iterate-over-dict-in-class-like-if-just-referring-to-dict
class DictHelper(dict):
        def __init__(self, *arg, **kw):
            super(DictHelper, self).__init__(*arg, **kw)
            self.choosebettername = super(DictHelper, self).keys()

        def __iter__(self):
            return iter(self.choosebettername)

        def keys(self):
            return self.choosebettername

        def itervalues(self):
            return (self[key] for key in self)