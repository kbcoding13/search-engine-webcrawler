class QueryOutput:
    def __init__(self):
        pass

    def output(self, rank:list, content:list):
        url_list = [content[r] for r in rank]
        return url_list
