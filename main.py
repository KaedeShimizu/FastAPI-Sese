from fastapi import FastAPI
import json
import random
from fastapi.responses import RedirectResponse

app = FastAPI()

# Init
default_proxy = "i.pixiv.re"
# 默认的数据库（data文件夹下）
default_data = "Kaede.json"
# 默认r18选项
default_r18 = 0


def use_proxy(proxy: str, url: str) -> str:
    """这个函数是用来把链接修改为代理后的链接用的

    Args:
        proxy (str): 代理地址
        url (str): 需要修改的链接

    Returns:
        str: 修改后的链接
    """
    # 链接的标准格式是：https://i.pixiv.re/img-original/
    # 通过find查找从而确认index
    index_start = url.find("/") + 1
    index_end = url.find("/", index_start + 1)
    url = url.replace(url[index_start + 1 : index_end], proxy)
    return url


def get_rand_link(db: str, proxy: str, r18: int, tags: str) -> str:
    """获取一个随机的链接

    Args:
        db (str): 传入的数据库
        proxy (str): 代理地址
        r18 (int): 是否是r18
        tags (str): 查询的关键字

    Returns:
        str: 修改好的链接
    """
    with open(f"data/{db}", "r", encoding="utf-8") as f:
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

        # tags
        if tags:
            tmp_data = []
            # 如果有的话开始遍历判断
            for i in json_data:
                if tags in i["tags"]:
                    tmp_data.append(i)
            json_data = tmp_data
        length = len(json_data)
        link = json_data[random.randint(0, length)]["url"]
        # 这里判断一下是否需要代理，不需要的话就是默认随机
        if proxy != None:
            return use_proxy(proxy, link)
        return link


def get_rand_json(db: str, r18: int, tags: str, num: int) -> list:
    """获取一个json数据

    Args:
        db (str): 使用的数据库
        r18 (int): 是否是r18
        tags (str): 关键字
        num (int): 数量

    Returns:
        list: json列表
    """
    # 先对数量进行一个判断，如果超出去了或者不在范围内直接翻译空数组就是
    if num < 1 or num > 20:
        return []
    with open(f"data/{db}", "r", encoding="utf-8") as f:
        json_data = json.load(f)
        # R18判断
        if r18 == 1:
            # 创建一个临时数组
            tmp_data = []
            # 开始便利json文件，筛选出所有的r18内容
            for i in json_data:
                if i["r18"] == 1:
                    tmp_data.append(i)
            json_data = tmp_data

        if r18 == 0:
            # 创建一个临时数组
            tmp_data = []
            # 开始便利json文件，筛选出所有的r18内容
            for i in json_data:
                if i["r18"] == 0:
                    tmp_data.append(i)
            json_data = tmp_data

        # tags
        if tags:
            tmp_data = []
            # 如果有的话开始遍历判断
            for i in json_data:
                if tags in i["tags"]:
                    tmp_data.append(i)
            json_data = tmp_data

        length = len(json_data)
        # 临时数组
        temp_arr = []
        for i in range(num):
            temp_arr.append(json_data[random.randint(0, length)])
        return temp_arr


@app.get("/")
def pixiv_get(
    # 使用的数据库，放在data目录下，用json文件
    db: str = default_data,
    # 是否用r18图片 2是随机
    r18: int = default_r18,
    proxy: str = default_proxy,
    # 关键词，可有可无
    tags: str = None,
):
    # 直接返回302跳转的图片就好
    return RedirectResponse(get_rand_link(db, proxy, r18, tags))


@app.post("/")
def pixiv_post(
    # 使用的数据库，放在data目录下，用json文件
    db: str = default_data,
    # 是否用r18图片 2是随机
    r18: int = default_r18,
    # 请求次数，默认是1，如果是其他数字那么返回一个json
    num: int = 1,
    # 关键词，可有可无
    tags: str = None,
):
    return get_rand_json(db, r18, tags, num)


# json的方法get
@app.get("/json")
def json_get(
    # 使用的数据库，放在data目录下，用json文件
    db: str = default_data,
    # 是否用r18图片 2是随机
    r18: int = default_r18,
    # 请求次数，默认是1，如果是其他数字那么返回一个json
    num: int = 1,
    # 关键词，可有可无
    tags: str = None,
):
    return get_rand_json(db, r18, tags, num)


# 如果是direct的话，没有什么参数，直接返回一张就行
@app.get("/direct")
def direct(
    # 使用的数据库，放在data目录下，用json文件
    db: str = default_data,
    # 代理地址
    proxy: str = default_proxy,
    # 是否用r18图片 2是随机
    r18: int = default_r18,
    # 关键词，可有可无
    tags: str = None,
):
    return RedirectResponse(get_rand_link(db, proxy, r18, tags))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
