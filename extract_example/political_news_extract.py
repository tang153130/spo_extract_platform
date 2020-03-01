# -*- coding: utf-8 -*-
# author: Jclian91
# place: Pudong Shanghai
# time: 2020-02-29 16:28
import requests
import pandas as pd
import os, re, json, traceback
from docx import Document
from pyltp import SentenceSplitter

project_dir = './corpus/political_news'

texts = []
file_paths = []
subjs, preds, objs = [], [], []

# 遍历project目录并读取其中的word文档进行SPO提取
for root, dirs, files in os.walk(project_dir):
    for name in files:
        file_path = os.path.join(root, name)

        if file_path.endswith('.docx'):

            # 读物word文档内容，并进行分句
            document = Document(file_path)
            doc_content = ''.join([para.text for para in document.paragraphs])
            sents = list(SentenceSplitter.split(doc_content))

            # 对每一句话进行SPO提取
            for sent in sents:

                sent = sent.replace(" ", "")
                req = requests.post("http://localhost:12308/spo_extract", data={"text": sent})
                res = json.loads(req.content)

                if res:
                    print("原文: %s" % sent)
                    print("SPO: %s\n" % res)

                    for item in res:
                        subj = item["subject"]
                        pred = item["predicate"]
                        obj = item["object"]

                        if subj != obj:
                            subjs.append(subj)
                            preds.append(pred)
                            objs.append(obj)
                            texts.append(sent)
                            file_paths.append(file_path)


# 将抽取的三元组结果保存成EXCEL文件
df = pd.DataFrame({"S": subjs,
                   "P": preds,
                   "O": objs,
                   "text": texts,
                   "file_path": file_paths
                 })

df.to_excel("political_new_extract.xlsx", index=False)