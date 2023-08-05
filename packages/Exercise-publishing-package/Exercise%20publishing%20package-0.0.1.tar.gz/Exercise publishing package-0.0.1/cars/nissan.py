class Nissan:

    def __init__(self):
        self.models = ["3", "4"]

    def get_models(self):
        for i in self.models:
            print('\t%s' % i)
