class Terminal256(object):
    def __init__(self, functionality):
        self.exposable = functionality

    def parse_uri(self, string) -> (Function, Params):
        pass

    def take_input(self, fp):
        pass

    def print_output(self, string):
        pass

    def print_error(self, string):
        pass
