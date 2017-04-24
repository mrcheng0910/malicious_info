# encoding: utf-8
"""
解决电话验证的思路
1. 使用香农熵，计算电话号码的随机性

2. 使用编辑距离，计算其相似性

3. “好念”（gibberish detection） 基于马尔科夫模型的

注意：
如何讲位置信息考虑到算法中是最重要的
"""

from collections import Counter
import math
main_domain = 'fryjntzfvti'
main_domain = '17763101025'
main_domain = '1234567890'
main_domain = '60000000'
count = Counter(i for i in main_domain).most_common()

f_len = float(len(main_domain))

entropy = -sum(j/f_len*(math.log(j/f_len)) for i, j in count)#shannon entropy
print entropy

