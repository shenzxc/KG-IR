#!/usr/bin/env python3
# coding: utf-8
# File: query_classifier.py

import os
import ahocorasick


class QueryClassifier(object):

    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # 　特征词路径
        #self.movie_title_path = os.path.join(cur_dir, 'dict/entity2id.txt')
        self.person_name_path = os.path.join(cur_dir, 'dict/entity2id.txt')

        # 加载特征词
        #self.movie_title_wds = [
        #    i.strip()
         #   for i in open(self.movie_title_path, 'r', encoding='utf-16')
         #   if i.strip()
       # ]
        self.person_name_wds = [
            i.strip()
            for i in open(self.person_name_path, 'r', encoding='utf-16')
            if i.strip()
        ]
        # 类别特征
        self.region_words = set(self.person_name_wds)
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))

        # 构建字典
        self.wdtype_dict = self.build_wdtype_dict()
        print('model init finished ......')

        # 关系
        ## 深度学习
        ## 规则匹配
        self.isa = ['isa']
        self.interacts_with = ['interacts_with']
        self.treats = ['treats','cure','remedy']
        self.affects = ['affects']
        self.diagnoses = ['diagnoses','recognize','verify','confirm']
        self.ingredient_of = ['ingredient_of']
        self.causes = ['causes','lead to','result','bring about','give rise to']
        self.associated_with = ['associated_with','related','correlative','confederative']
        self.measurement_of = ['measurement_of','bigness','dimension','magnitude']
        self.manifestation_of = ['manifestation_of','​evidence','demonstration','manifestation']
        self.part_of = ['part_of','component','unit']
   
        return

    '''分类主函数'''

    def classify(self, query):
        # 吴京导演的战狼电影 －>  吴京{person}  导演｛director｝ 战狼｛movie｝
        data = {}

        # 实体
        data['query'] = query
        _dict = self.check_query(query)
        data['query_ner'] = _dict

        # 关系
        types = []
        for type_ in _dict.values():
            types += type_

        query_type = 'other'
        if self.check_words(self.isa, query) and ('entity2id'
                                                         in types):
            query_type = 'isa'
        if self.check_words(self.interacts_with, query) and ('entity2id'
                                                            in types):
            query_type = 'interacts_with'
        if self.check_words(self.treats, query) and ('entity2id'
                                                            in types):
            query_type = 'treats'
        if self.check_words(self.affects, query) and ('entity2id'
                                                            in types):
            query_type = 'affects'
        if self.check_words(self.diagnoses, query) and ('entity2id'
                                                            in types):
            query_type = 'diagnoses'
        if self.check_words(self.ingredient_of, query) and ('entity2id'
                                                            in types):
            query_type = 'ingredient_of'
        if self.check_words(self.causes, query) and ('entity2id'
                                                            in types):
            query_type = 'causes'
        if self.check_words(self.associated_with, query) and ('entity2id'
                                                            in types):
            query_type = 'associated_with'
        if self.check_words(self.measurement_of, query) and ('entity2id'
                                                            in types):
            query_type = 'measurement_of'
        if self.check_words(self.manifestation_of, query) and ('entity2id'
                                                            in types):
            query_type = 'manifestation_of'
        if self.check_words(self.part_of, query) and ('entity2id'
                                                            in types):
            query_type = 'part_of'                                

        data['query_type'] = query_type
        return data

    '''构造词对应的类型'''

    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            #if wd in self.movie_title_wds:
            #    wd_dict[wd].append('entity2id')
            if wd in self.person_name_wds:
                wd_dict[wd].append('entity2id')
        return wd_dict

    '''构造actree，加速过滤'''

    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''

    def check_query(self, query):
        # 1.
        # NER: BiLSTM+CRF
        # Bert + CRF

        #2. ac

        ## 获取实体后续数据集合
        region_wds = []
        for i in self.region_tree.iter(query):
            wd = i[1][1]
            region_wds.append(wd)

        # 获取最长匹配串
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds
                     if i not in stop_wds]  #[word1,word2,word3]

        #<word,word_type> －> <战狼,movie> | < 吴京,person>
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}
        return final_dict

    '''基于特征词进行分类'''

    def check_words(self, wds, query):
        for wd in wds:
            if wd in query:
                return True
        return False


if __name__ == '__main__':
    handler = QueryClassifier()
    query = "calcium isa diet"
    data = handler.classify(query)
    print(data)
