#!/usr/bin/env python3
# coding: utf-8
# File: query_parser.py
class QueryPaser(object):
    '''构建实体节点'''

    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''

    def parser_main(self, res_classify):
        query = res_classify['query']
        query_ner = res_classify['query_ner']
        entity_dict = self.build_entitydict(query_ner)
        query_type = res_classify['query_type']
        sql_ = {}
        sql_['query_type'] = query_type
        sql = []
        if query_type == 'isa':
            # 成龙主演的电影
            sql = self.sql_transfer(query_type, entity_dict.get('entity2id'))
        elif query_type == 'interacts_with':
            # 成龙创作的电影
            sql = self.sql_transfer(query_type, entity_dict.get('entity2id'))
        elif query_type == 'treats':
            # 成龙创作的电影
            sql = self.sql_transfer(query_type, entity_dict.get('entity2id'))
        elif query_type == 'affects':
            # 成龙创作的电影
            sql = self.sql_transfer(query_type, entity_dict.get('entity2id'))
        elif query_type == 'diagnoses':
            # 成龙创作的电影
            sql = self.sql_transfer(query_type, entity_dict.get('entity2id'))
        elif query_type == 'ingredient_of':
            # 成龙创作的电影
            sql = self.sql_transfer(query_type, entity_dict.get('entity2id'))
        elif query_type == 'causes':
            # 成龙创作的电影
            sql = self.sql_transfer(query_type, entity_dict.get('entity2id'))
        elif query_type == 'associated_with':
            # 成龙创作的电影
            sql = self.sql_transfer(query_type, entity_dict.get('entity2id'))
        elif query_type == 'measurement_of':
            # 成龙创作的电影
            sql = self.sql_transfer(query_type, entity_dict.get('entity2id'))
        elif query_type == 'manifestation_of':
            # 成龙创作的电影
            sql = self.sql_transfer(query_type, entity_dict.get('entity2id'))
        elif query_type == 'part_of':
            # 成龙创作的电影
            sql = self.sql_transfer(query_type, entity_dict.get('entity2id'))    
        else:
            # 速度与激情
            if entity_dict.get('entity2id', None) is not None:
                params = entity_dict.get('entity2id')
            else:
                params = [query]
            sql = self.sql_transfer(query_type, params)

        if sql:
            sql_['sql'] = sql
        return sql_

    '''针对不同的问题，分开进行处理'''

    def sql_transfer(self, query_intent, entities):
        if not entities:
            return []
        # 查询语句
        sql = []
        # 查询疾病的原因
        if query_intent == 'isa':
            sql = [
                "MATCH (p:Entity)-[r:_isa_]-(m:Entity) where p.name = '{0}' return m.name, m.title, m.url limit 20"
                .format(i) for i in entities
            ]
        elif query_intent == 'interacts_with':
            sql = [
                "MATCH (p:Entity)-[r:_interacts_with_]-(m:Entity) where p.name = '{0}' return m.name, m.title, m.url limit 20"
                .format(i) for i in entities
            ]
        elif query_intent == 'treats':
            sql = [
                "MATCH (p:Entity)-[r:_treats_]-(m:Entity) where p.name = '{0}' return m.name, m.title, m.url limit 20"
                .format(i) for i in entities
            ]
        elif query_intent == 'affects':
            sql = [
                "MATCH (p:Entity)-[r:_affects_]-(m:Entity) where p.name = '{0}' return m.name, m.title, m.url limit 20"
                .format(i) for i in entities
            ]
        elif query_intent == 'diagnoses':
            sql = [
                "MATCH (p:Entity)-[r:_diagnoses_]-(m:Entity) where p.name = '{0}' return m.name, m.title, m.url limit 20"
                .format(i) for i in entities
            ]
        elif query_intent == '_ingredient_of_':
            sql = [
                "MATCH (p:Entity)-[r:_ingredient_of_]-(m:Entity) where p.name = '{0}' return m.name, m.title, m.url limit 20"
                .format(i) for i in entities
            ]
        elif query_intent == 'causes':
            sql = [
                "MATCH (p:Entity)-[r:_causes_]-(m:Entity) where p.name = '{0}' return m.name, m.title, m.url limit 20"
                .format(i) for i in entities
            ]
        elif query_intent == 'associated_with':
            sql = [
                "MATCH (p:Entity)-[r:_associated_with_]-(m:Entity) where p.name = '{0}' return m.name, m.title, m.url limit 20"
                .format(i) for i in entities
            ]
        elif query_intent == 'measurement_of':
            sql = [
                "MATCH (p:Entity)-[r:_measurement_of_]-(m:Entity) where p.name = '{0}' return m.name, m.title, m.url limit 20"
                .format(i) for i in entities
            ]
        elif query_intent == 'manifestation_of':
            sql = [
                "MATCH (p:Entity)-[r:_manifestation_of_]-(m:Entity) where p.name = '{0}' return m.name, m.title, m.url limit 20"
                .format(i) for i in entities
            ] 
        elif query_intent == 'part_of':
            sql = [
                "MATCH (p:Entity)-[r:_part_of_]-(m:Entity) where p.name = '{0}' return m.name, m.title, m.url limit 20"
                .format(i) for i in entities
            ]
        else:
            # 按照电影名称模糊查询
            sql = ["MATCH (m:Entity) where toLower(m.name) CONTAINS toLower('{0}') " \
                   "return m.name, m.title, m.url limit 20"
                       .format(i) for i in entities]
            # 按照人名精准查询
            sql += [
                "MATCH (p:Entity)-[]-(m:Entity) where p.name = '{0}' return m.name, m.title, m.url limit 20"
                .format(i) for i in entities
            ]

        return sql


if __name__ == '__main__':
    handler = QueryPaser()
