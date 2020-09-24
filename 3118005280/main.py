# -*- coding:utf-8 -*-
from sys import argv
import math
import jieba
import jieba.analyse
from simhash import Simhash


class GetHash(object):
    '''
    获取hash值
    '''
    def get_bin_str(self, source):
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]
            return str(x)

    def get_str_hash(self, rawstr):
        seg = jieba.cut(rawstr)
        keywords = jieba.analyse.extract_tags(
            "|".join(seg), topK=100, withWeight=True)
        ret = []
        for keyword, weight in keywords:
            binstr = self.get_bin_str(keyword)
            keylist = []
            for c in binstr:
                weight = math.ceil(weight)
                if c == "1":
                    keylist.append(int(weight))
                else:
                    keylist.append(-int(weight))
            ret.append(keylist)
        row_list = len(ret)  # 对列表进行"降维"
        column = len(ret[0])
        result = []
        for i in range(column):
            tmp = 0
            for j in range(row_list):
                tmp += int(ret[j][i])
            if tmp > 0:
                tmp = "1"
            elif tmp <= 0:
                tmp = "0"
            result.append(tmp)
        return "".join(result)


def similarHash(text1, text2):
    '''
    获取文章相似度
    '''

    simhash = GetHash()

    hash1 = simhash.get_str_hash(text1)  # 计算hash
    hash2 = simhash.get_str_hash(text2)  # 计算hash

    t1_simhash = Simhash(hash1)
    t2_simhash = Simhash(hash2)

    distince = t1_simhash.distance(t2_simhash)
    max_hashbit = max(len(bin(t1_simhash.value)), (len(bin(t2_simhash.value))))
    if max_hashbit == 0:
        return 0
    else:
        ssimilar = 1 - distince / max_hashbit
        return (ssimilar)


def check(argv):
    '''
    相似度对比函数
    '''

    try:
        f = open(argv[1], 'r', encoding='utf-8')  # 打开源文件
        g = open(argv[2], 'r', encoding='utf-8')  # 打开检测文件
        answer = open(argv[3], 'a+', encoding='utf-8')

        f1 = f.read()  #读取文件--字符串
        g1 = g.read()  #读取文件--字符串

        similar = similarHash(f1, g1)  # 计算相似度
        real_similar = round(similar, 2)  # 保留小数

        strs = "相似率为："
       
        answer.write(strs + str(real_similar)+"\n")
        f.close()
        g.close()
        print("文章相似率为：%.2f\n" % real_similar)
    
        answer.close()  # 关闭文件
    except IndexError:
        print("输入错误！")
    except FileNotFoundError:
        print("没找到文件，！")
    return 0


if __name__ == '__main__':
    
    check(argv)
