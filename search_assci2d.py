from nonebot import on_command
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.params import CommandArg
import requests
from nonebot.adapters.onebot.v11 import Bot, Event
from bs4 import BeautifulSoup

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/99.0.4844.82 Safari/537.36"
    )
}

proxies={
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}

downloadPath = "D:\\bot\\awesomebot\\awesomebot\\plugins\\imagetmp\\"


class Ascii2dImg:
    def __init__(self, name, thumbUrl, url, source):
        self.name = name
        self.thumbUrl = thumbUrl
        self.url = url
        self.source = source


def dealer(data):
    infos = data.find("div", {"detail-box gray-link"})
    thumbUrl = data.find("img")
    thumbUrl = "https://ascii2d.net" + thumbUrl["src"]
    if infos:
        h6 = infos.find("h6")
        if h6:
            # 图片来源
            small = h6.find("small")
            print(small.string)
            # 图片来源链接
            links = h6.find("a")
            name = links.string

            print(links["href"])
            print(name)
            print("******")
            return Ascii2dImg(name, thumbUrl, links["href"], small.string)


searchImage = on_command("搜图")


@searchImage.handle()
async def searchImageHandler(event: Event, args: Message = CommandArg()):
    _, group, qq = str(event.get_session_id()).split("_")
    ascii2d_url = "https://ascii2d.net/search/uri"
    data = {
    }
    for arg in args:
        if arg.type != "image":
            await searchImage.finish("你没有发送图片")
        data.update({"uri": arg.data["url"]})
        print(data)
        resp = requests.post(
            url=ascii2d_url,
            data=data,
            proxies=proxies,
            headers=DEFAULT_HEADERS)
        bovw = requests.get(
            resp.url.replace("color", "bovw"),
            proxies=proxies,
            headers=DEFAULT_HEADERS
        )
        print(bovw.url)
        soup = BeautifulSoup(bovw.text, features="html.parser")
        blocks = soup.find_all("div", {'class': 'row item-box'})
        for i in blocks:
            ascii2dImg = dealer(i)
            if ascii2dImg == None:
                continue
            msg = (
                MessageSegment.at(user_id=qq),
                MessageSegment.image(ascii2dImg.thumbUrl),
                MessageSegment.text("来源:" + ascii2dImg.source),
                MessageSegment.text(ascii2dImg.url)
            )
            await searchImage.send(msg)
            break
