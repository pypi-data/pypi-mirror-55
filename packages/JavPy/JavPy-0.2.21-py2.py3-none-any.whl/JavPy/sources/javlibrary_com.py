from JavPy.sources.BaseSource import INewlyReleased, IGetBrief
import cfscrape
from JavPy.utils.requester import spawn_many, Task
import re
from JavPy.functions.datastructure import AV, Brief
import datetime
import bs4


class JavLibraryCom(INewlyReleased, IGetBrief):

    __client = cfscrape.create_scraper()

    @classmethod
    def get_newly_released(cls, page):
        major_info_req = Task(cls.__client.get, "http://www.javlibrary.com/cn/vl_newrelease.php?mode=2&page=%d" % page)
        dates_req = Task(cls.__client.get, "http://www.javlibrary.com/cn/vl_newrelease.php?list&mode=2&page=%d" % page)
        major_info_rsp, dates_rsp = spawn_many((major_info_req, dates_req)).wait_for_all_finished()
        major_info = cls.parse_major_info(major_info_rsp)
        dates = map(lambda d: datetime.datetime.strptime(d, "%Y-%m-%d"), filter(
            lambda x: "-" in x, re.findall("<td>(.+?)</td>", dates_rsp.text)
        ))

        for i, date in enumerate(dates):
            major_info[i].release_date = date
        return major_info

    @staticmethod
    def parse_major_info(rsp):
        items = re.findall("<div class=\"video\".+?</div></div>", rsp.text, re.S)
        res = []
        for item in items:
            av = AV()
            img_url = re.search("<img src=\"(.+?)\"", item).group(1).replace("ps.jpg", "pl.jpg")
            if not img_url.startswith("http"):
                img_url = "http:" + img_url
            av.preview_img_url = img_url
            av.code = re.search("<div class=\"id\">(.+?)</div>", item).group(1)
            av.title = re.search("<div class=\"title\" >(.+?)</div>", item).group(1)
            res.append(av)
        return res

    @classmethod
    def get_brief(cls, code):
        html = cls.__client.get("http://www.javlibrary.com/ja/vl_searchbyid.php?keyword=" + code).text
        match = re.search(r"\"og:url\" content=\"//(.+?)\">", html)
        if not match:
            return None
        url = match.group(1)
        html = cls.__client.get("http://" + url).text
        brief = Brief()
        bs = bs4.BeautifulSoup(html, "lxml")
        brief.title = bs.select(".post-title")[0].text
        brief.preview_img_url = bs.select("#video_jacket_img")[0].attrs['src']
        if not brief.preview_img_url.startswith("http"):
            brief.preview_img_url = "http:" + brief.preview_img_url
        brief.code = code
        date = bs.select("#video_date")[0].select("td")[-1].text
        brief.set_release_date(date)
        brief.actress = ", ".join((span.text for span in bs.select(".cast")))
        return brief


if __name__ == '__main__':
    JavLibraryCom.get_brief("ABP-123")
