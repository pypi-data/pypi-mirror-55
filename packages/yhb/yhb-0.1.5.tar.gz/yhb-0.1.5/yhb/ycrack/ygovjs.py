import re
import requests
from yhb.ycrack.yjiasule import prepare_cookie


def get_csrc_page_info(html):
    try:
        current_page = int(re.findall("var currentPage = (\d+?);", html).pop())
        count_page = int(re.findall("var countPage = (\d+?)/", html).pop())
    except Exception as e:
        return {
            # "page": html,
            "current_page": None,
            "count_page": None,
            "next_page": None
        }

    if current_page < count_page - 1:
        next_page = current_page + 1
        res = {
            # "page": html,
            "current_page": current_page,
            "count_page": count_page,
            "next_page": "/index_" + str(next_page) + ".html"
        }
        return res
    else:
        return {
            # "page": html,
            "current_page": current_page,
            "count_page": count_page,
            "next_page": None
        }


def get_cbrc_cookie_info(html):
    return prepare_cookie(html)


def get_ndrc_page_info(html):
    try:
        count_page, current_page = re.findall("createPageHTML\((\d+), (\d+), .*?\);", html).pop()
        count_page = int(count_page)
        current_page = int(current_page)
    except Exception as e:
        return {
            # "page": html,
            "current_page": None,
            "count_page": None,
            "next_page": None
        }

    if current_page < count_page - 1:
        next_page = current_page + 1
        res = {
            # "page": html,
            "current_page": current_page,
            "count_page": count_page,
            "next_page": "/index_" + str(next_page) + ".html"
        }
        return res
    else:
        return {
            # "page": html,
            "current_page": current_page,
            "count_page": count_page,
            "next_page": None
        }


def get_mof_page_info(html):
    try:
        current_page = int(re.findall("var currentPage = (\d+?);", html).pop())
        count_page = int(re.findall("var countPage = (\d+?)/", html).pop())
    except Exception as e:
        return {
            # "page": html,
            "current_page": None,
            "count_page": None,
            "next_page": None
        }

    if current_page < count_page - 1:
        next_page = current_page + 1
        res = {
            # "page": html,
            "current_page": current_page,
            "count_page": count_page,
            "next_page": "/index_" + str(next_page) + ".html"
        }
        return res
    else:
        return {
            # "page": html,
            "current_page": current_page,
            "count_page": count_page,
            "next_page": None
        }


def get_sac_page_info(html):
    try:
        current_page = int(re.findall("var currentPage = (\d+?);", html).pop())
        count_page = int(re.findall("var countPage = (\d+?);", html).pop())
    except Exception as e:
        return {
            # "page": html,
            "current_page": None,
            "count_page": None,
            "next_page": None
        }

    if current_page < count_page - 1:
        next_page = current_page + 1
        res = {
            # "page": html,
            "current_page": current_page,
            "count_page": count_page,
            "next_page": "/index_" + str(next_page) + ".html"
        }
        return res
    else:
        return {
            # "page": html,
            "current_page": current_page,
            "count_page": count_page,
            "next_page": None
        }


def get_mee_page_info(html):
    try:
        current_page = int(re.findall("var currentPage=(\d+?);", html).pop())
        count_page = int(re.findall("var countPage=(\d+?)\n", html).pop())
    except Exception as e:
        return {
            # "page": html,
            "current_page": None,
            "count_page": None,
            "next_page": None
        }

    if current_page < count_page - 1:
        next_page = current_page + 1
        res = {
            # "page": html,
            "current_page": current_page,
            "count_page": count_page,
            "next_page": "/index_" + str(next_page) + ".shtml"
        }
        return res
    else:
        return {
            # "page": html,
            "current_page": current_page,
            "count_page": count_page,
            "next_page": None
        }


if __name__ == '__main__':
    session = requests.Session()

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
    })
    resp = session.post("http://www.cbrc.gov.cn/chinese/newShouDoc/BB8E3EEC78EA4281ADF4A55325AFE271.html")
    a = resp.content.decode("utf-8")
    # a = resp.content.decode("gbk")
    # print(get_csrc_page_info(a))
    print(get_cbrc_cookie_info(a))
    # print(get_ndrc_page_info(a))
    # print(get_mof_page_info(a))
    # print(get_sac_page_info(a))
    # print(get_mee_page_info(a))
