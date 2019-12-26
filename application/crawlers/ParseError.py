class ParseError(Exception):

    parse_result = None

    """Exception during html parsing"""

    def __init__(self, message, parse):
        self.parse_result = parse
        print(parse)
        Exception.__init__(self)
