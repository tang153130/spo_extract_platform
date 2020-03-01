# -*- coding: utf-8 -*-
# author: Jclian91
# place: Pudong Shanghai
# time: 2020-02-27 01:04
import json
import requests

import pandas as pd

from pyltp import SentenceSplitter

with open('./corpus/bailuyuan.txt', 'r', encoding='utf-8') as f:
    content = f.read()

sents = [_.strip().replace(" ", "") for _ in list(SentenceSplitter.split(content)) if _.strip()]

texts = []
subjs, preds, objs = [], [], []

for line in sents:

    req = requests.post("http://localhost:12308/spo_extract", data={"text": line} )
    res = json.loads(req.content)

    if res:
        print("原文: %s" % line)
        print("SPO: %s\n" % res)

        for item in res:
            subj = item["subject"]
            pred = item["predicate"]
            obj = item["object"]

            if subj != obj:
                subjs.append(subj)
                preds.append(pred)
                objs.append(obj)
                texts.append(line)

# 将抽取的三元组结果保存成EXCEL文件

df = pd.DataFrame({"S": subjs,
                   "P": preds,
                   "O": objs,
                   "text": texts
                   })

df.to_excel("bailuyuan.xlsx", index=False)
