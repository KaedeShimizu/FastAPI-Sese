# main.py
# Made by KaedeShimizu
from fastapi import FastAPI
import json
import random


# 直接返回一个可用链接
# 需要传入一些参数，具体参数见文档
def getARandomLink(db, proxy, size, r18, keywords):
    with open(f"data\\{db}", "r", encoding="utf-8") as f:
        json_data = json.load(f)
        # R18判断
        if r18 == 1:
            # 创建一个临时数组
            tmp_data = []
            # 开始便利json文件，筛选出所有的r18内容
            for i in json_data:
                if i["r18"]:
                    tmp_data.append(i)
            json_data = tmp_data

        if r18 == 0:
            # 创建一个临时数组
            tmp_data = []
            # 开始便利json文件，筛选出所有的r18内容
            for i in json_data:
                if not i["r18"]:
                    tmp_data.append(i)
            json_data = tmp_data

        # keywords判断
        if keywords:
            tmp_data = []
            # 如果有的话开始遍历判断
            for i in json_data:
                if keywords in i["tags"]:
                    tmp_data.append(i)
            json_data = tmp_data

        length = len(json_data)
        link = json_data[random.randint(0, length)]["urls"][size]
        return link.replace("i.pximg.net", proxy)


# 重定向页面
from fastapi.responses import RedirectResponse

app = FastAPI()


# 如果直接访问，跳转到文档页面就行
@app.get("/")
def root():
    return RedirectResponse("https://kaedeshimizu.gitee.io/docs/")


@app.get("/pixiv")
def pixivDefault(
    # 使用的数据库，放在data目录下，用json文件
    db: str = "setu.json",
    # 代理地址
    proxy: str = "pixiv.yuki.sh",
    # 图片尺寸
    size: str = "original",
    # 是否用r18图片 2是随机
    r18: int = 2,
    # 请求次数，默认是1，如果是其他数字那么返回一个json
    num: int = 1,
    # 关键词，可有可无
    keywords: str = None,
):
    default_dict = {}
    for i in range(num):
        default_dict.update(
            {f"link_{i}": getARandomLink(db, proxy, size, r18, keywords)}
        )
    return default_dict


# json的方法get
@app.get("/pixiv/json")
def json_get(
    # 使用的数据库，放在data目录下，用json文件
    db: str = "setu.json",
    # 代理地址
    proxy: str = "pixiv.yuki.sh",
    # 图片尺寸
    size: str = "original",
    # 是否用r18图片 2是随机
    r18: int = 2,
    # 请求次数，默认是1，如果是其他数字那么返回一个json
    num: int = 1,
    # 关键词，可有可无
    keywords: str = None,
):
    default_dict = {}
    for i in range(num):
        default_dict.update(
            {f"link_{i}": getARandomLink(db, proxy, size, r18, keywords)}
        )
    return default_dict


# 如果是direct的话，没有什么参数，直接返回一张就行
@app.get("/pixiv/direct")
def direct(
    # 使用的数据库，放在data目录下，用json文件
    db: str = "setu.json",
    # 代理地址
    proxy: str = "pixiv.yuki.sh",
    # 图片尺寸
    size: str = "original",
    # 是否用r18图片 2是随机
    r18: int = 2,
    # 关键词，可有可无
    keywords: str = None,
):
    return RedirectResponse(getARandomLink(db, proxy, size, r18, keywords))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)