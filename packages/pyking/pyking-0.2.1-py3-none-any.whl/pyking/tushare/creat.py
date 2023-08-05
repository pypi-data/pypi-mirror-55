import pyking.docs.tutext as tut
import pyking.docs.matext as matext


def creat():
    with open('TuJson.py', 'wt', encoding='utf-8') as f:
        f.write(tut.text1)
    with open('TuSdk.py', 'wt', encoding='utf-8') as f:
        f.write(tut.text2)
    with open('Tu普通接口.py', 'wt', encoding='utf-8') as f:
        f.write(tut.text3)
    with open('Tu常用接口文档.md', 'wt', encoding='utf-8') as f:
        f.write(tut.text4)
    with open('matdoc.md', 'wt', encoding='utf-8') as f:
        f.write(matext.text1)

    return
