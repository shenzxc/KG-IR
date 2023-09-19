# 知识图谱的搜索系统项目，知识库存储
import py2neo
from neo4j import GraphDatabase


class HelloWorldExample:
    # 获取连接图数据库
    def __init__(self, uri, user, password) -> None:
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    # 关闭图数据库资源
    def close(self, ):
        self.driver.close()

    # 清空数据
    def clear_data(self, ):

        def work(tx):
            tx.run("""
                match(n) detach delete n
            """)

        with self.driver.session() as session:
            session.write_transaction(work)

    # 创建节点
    def create_node(self, ):

        def movie_work(tx):
            tx.run("""
            LOAD CSV with headers from 'file:///Users/shenweiming/Downloads/安装包下载/代码/aiwen_learn_kg/data/Movie.csv' as line
            CREATE (:Movie {
                id:line["id:ID"],
                title:line["title"],
                url:line["url"],
                cover:line["cover"],
                rate:line["rate"],
                category:split(line["category:String[]"], ";"),
                language:split(line["language:String[]"], ";"),
                showtime:line["showtime"],
                length:line["length"],
                othername:split(line["othername:String[]"], ";")
                })
            """)

        def person_work(tx):
            tx.run("""
            LOAD CSV with headers from 'file:///Users/shenweiming/Downloads/安装包下载/代码/aiwen_learn_kg/data/Person.csv' as line
            CREATE (:Person {id:line["id:ID"], name:line["name"]})
            """)

        def country_work(tx):
            tx.run("""
            LOAD CSV with headers from 'file:///Users/shenweiming/Downloads/安装包下载/代码/aiwen_learn_kg/data/Country.csv' as line
            CREATE (:Country {id:line["id:ID"], name:line["name"]})
            """)

        with self.driver.session() as session:
            session.write_transaction(movie_work)
            session.write_transaction(person_work)
            session.write_transaction(country_work)

    # 创建索引
    def create_index(self, ):

        def work(tx):
            tx.run("""
              CREATE INDEX IF NOT EXISTS FOR (m:Movie) ON (m.id)
            """)

            tx.run("""
            CREATE INDEX IF NOT EXISTS FOR (p:Person) ON (p.id)
            """)

            tx.run("""
             CREATE INDEX IF NOT EXISTS FOR (c:Country) ON (c.id)
            """)

        with self.driver.session() as session:
            session.write_transaction(work)

    # 创建关系
    def create_relationship(self, ):

        # 提示：大家换成自己的路径
        # 老师微信： vx-aiwen  加入一对一辅导 ，BAT大厂算法专家
        def work(tx):
            tx.run("""
            LOAD CSV with headers from 'file:///Users/shenweiming/Downloads/安装包下载/代码/aiwen_learn_kg/data/actor.csv' as line
            MATCH (a:Movie {id:line[":START_ID"]})
            MATCH (b:Person {id:line[":END_ID"]})
            CREATE (a)-[:actor]->(b)
            """)

            tx.run("""
            LOAD CSV with headers from 'file:///Users/shenweiming/Downloads/安装包下载/代码/aiwen_learn_kg/data/composer.csv' as line
            MATCH (a:Movie {id:line[":START_ID"]})
            MATCH (b:Person {id:line[":END_ID"]})
            CREATE (a)-[:composer]->(b)
            """)

            tx.run("""
            LOAD CSV with headers from 'file:///Users/shenweiming/Downloads/安装包下载/代码/aiwen_learn_kg/data/director.csv' as line
            MATCH (a:Movie {id:line[":START_ID"]})
            MATCH (b:Person {id:line[":END_ID"]})
            CREATE (a)-[:director]->(b)
            """)

            tx.run("""
            LOAD CSV with headers from 'file:///Users/shenweiming/Downloads/安装包下载/代码/aiwen_learn_kg/data/district.csv' as line
            MATCH (a:Movie {id:line[":START_ID"]})
            MATCH (b:Country {id:line[":END_ID"]})
            CREATE (a)-[:district]->(b)
            """)

        with self.driver.session() as session:
            session.write_transaction(work)


if __name__ == '__main__':

    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "123654789"
    app = HelloWorldExample(uri, user, password)
    app.clear_data()

    app.create_node()
    app.create_index()
    app.create_relationship()
    app.close()