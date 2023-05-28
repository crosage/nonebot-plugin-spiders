from nonebot import on_command
from nonebot.adapters.onebot.v11.message import Message,MessageSegment
from nonebot.params import CommandArg
import requests
import base64
import time
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Event

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/99.0.4844.82 Safari/537.36"
    ),
    "authority":"soutubot.moe",
    "accept":"application/json, text/plain, */*",
    "origin":"https://soutubot.moe",
    "referer":"https://soutubot.moe/",
    "x-requested-with":"XMLHttpRequest"
}
proxy={
    "http":"http://127.0.0.1:7890",
    "https":"http://127.0.0.1:7890"
}
downloadPath="D:\\bot\\awesomebot\\awesomebot\\plugins\\imagetmp\\"

searchHentai=on_command("搜本")
@searchHentai.handle()
async def searchHentaiHandler(event:Event,args:Message=CommandArg()):
    _,group,qq=str(event.get_session_id()).split("_")
    searchBot="https://soutubot.moe/api/search"
    for arg in args:
        if arg.type!="image":
            await searchHentai.finish("你没有发送图片")
        resp=requests.get(arg.data["url"],proxies=proxy)
        h=hash(resp.content)
        print(resp)

        with open(downloadPath+str(h)+".png","w+b") as f:
            f.write(resp.content)
            f.close
            Q=str(int(pow(time.time(),2))+int(pow(len(DEFAULT_HEADERS["User-Agent"]),2)))
            encoded_data = str(base64.b64encode(Q.encode()).decode())[::-1].replace("=","")
            fr=open(downloadPath+str(h)+".png","rb")
            DEFAULT_HEADERS.update({"x-api-key":encoded_data})
            data={"factor":1.2}
            resp=requests.post(searchBot,headers=DEFAULT_HEADERS,files={"file":fr},data=data,proxies=proxy)
            print(resp.status_code)
            _json=resp.json()
            url=_json["data"][0]["previewImageUrl"]
            title=_json["data"][0]["title"]
            page=_json["data"][0]["pagePath"]
            msg=(
                MessageSegment.at(user_id=qq),
                MessageSegment.image(url),
                MessageSegment.text("标题:"+title),
                MessageSegment.text("https://nhentai.net/"+page)
            )
            await searchHentai.send(msg)
            
            