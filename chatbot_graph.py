#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py

from query_classifier import *
from query_parser import *
from query_searcher import QuerySearcher


class ChatBotGraph:

    def __init__(self):
        self.classifier = QueryClassifier()
        self.parser = QueryPaser()
        self.searcher = QuerySearcher()

    def chat_main(self, query):
        answer = '您好，我是艾文教教编程'

        # query 实体＋关系
        res_classify = self.classifier.classify(query)
        print('res_classify = ', res_classify)
        if not res_classify:
            return answer

        # query 解析
        res_sql = self.parser.parser_main(res_classify)
        print(res_sql)

        # 根据SQL语句，通过Neo4j 数据检索结果
        final_answers = self.searcher.search_main(res_sql)
        return final_answers


if __name__ == '__main__':
    handler = ChatBotGraph()
    #query = input("用户：")
    query = '成龙主演的警察故事'
    results = handler.chat_main(query)
    #print(results)
    #while 1:
    # 成龙主演的电影
    # 成龙导演的电影
    # 成龙创作的电影
    # 速度与激情
    # 成龙
    # query = input("用户：")
    # results = handler.chat_main(query)
