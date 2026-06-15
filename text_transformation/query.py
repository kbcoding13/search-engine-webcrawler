import datetime as dt

class QueryOutput:
    def __init__(self):
        self.last_requested = None

    def output(self, rank:list, content:list):
        url_list = [content[r] for r in rank]
        return url_list

    def paginate(self, url_list:list, page:int, results:int):
        i = results * (page - 1)
        j = i + results
        return url_list[i:j]
    
    def check_time(self):
        current_requested = dt.datetime.now()
        if self.last_requested is None:
           self.last_requested = current_requested
           return 'request success'
        else:
            time_difference = current_requested - self.last_requested
            seconds = time_difference.total_seconds()
            if seconds >= 10:
                self.last_requested = current_requested
                return 'request success'
        return f"too many requests, try again in {10 - seconds} seconds."

query_output = QueryOutput()

print(query_output.check_time())
print(query_output.check_time())
print(query_output.check_time())
print(query_output.check_time())
print(query_output.check_time())
print(query_output.check_time())
print(query_output.check_time())
print(query_output.check_time())
print(query_output.check_time())
print(query_output.check_time())
print(query_output.check_time())
print(query_output.check_time())
print(query_output.check_time())
print(query_output.check_time())

