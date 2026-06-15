class QueryOutput:
    def __init__(self):
        pass

    def output(self, rank:list, content:list):
        url_list = [content[r] for r in rank]
        return url_list

    def paginate(self, url_list:list, page:int, results:int):
        i = results * (page - 1)
        j = i + results
        return url_list[i:j]
    
    

#[i: results - `1`]
