from py2neo import Graph
import json
with open('data/terms_with_meta.json','r') as f:
            s = f.read()
            df = json.loads(s)
class QuerySearcher(object):

    def __init__(self) -> None:
        self.g = Graph("http://localhost:7474",
                       user="neo4j",
                       password="123654789",
                       name="neo4j")

    def search_main(self, sqls):

        #query解析返回的结果
        queryies = sqls['sql']
        # 通过知识图谱返回数据
        results = []
        for query in queryies:
            result = self.g.run(query).data()
            results += result
        # 数据格式化
        results = self.results_prettify(results)
        return results

    def results_prettify(self, results):
        new_results = []
        for record in results:
            data = {
                "name": record["m.name"],
                "title": record["m.title"],
                "url": record["m.url"],


               
                
          
            }
            new_results.append(data)
        return new_results
    
