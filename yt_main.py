import requests, time, logging, colorlog
import json
from title_generator import getRandomTitle
from video_ids_random import getRandomVidId
from youtube_uploader import youtubeUploader
from tiktok_uploader import tiktok
from common import get_video_info

# Create a logger
logger = colorlog.getLogger()
logger.setLevel(logging.DEBUG)

# Create a handler
handlerLog = colorlog.StreamHandler()
handlerLog.setFormatter(
    colorlog.ColoredFormatter(
        "[%(asctime)s] - %(log_color)s%(levelname)s:%(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
)
logger.addHandler(handlerLog)


def handler(vid_list):
    r = []
    prefix = "https://www.douyin.com/video/"
    list_vid_id = vid_list
    for id in list_vid_id:
        print("Fetch data video #", id)
        result = get_video_info(prefix, id)
        r.append(result)
        print("Done fetch data video #", id)
    # Export the data for use in future steps
    return r


def uploadToYouTube():
    data = {"video_ids": getRandomVidId(1)}
    video_info = {
        "tag": [
            "douyin",
            "chinesegirl",
            "hotgirls",
            "beautifulgirls",
            "cutegirls",
            "beautifulchinesegirls",
            "bodygoals",
            "fashionstyle",
            "model",
            "dance",
            "beauty",
            "cosplay",
            "sexylegs",
            "asianbeauty",
            "streetfashion",
            "chinesebeauty",
            "tiktok",
            "gaixink",
            "chandai",
            "quyenru",
            "nongbong",
        ],
        "des": "Kênh chuyên về tiktok, douyin gái xink Trung Quốc. #douyin #chinesegirl #hotgirls #beautifulgirls #cutegirls #beautifulchinesegirls #bodygoals #fashionstyle #model #dance #beauty #cosplay #sexylegs #asianbeauty #streetfashion #chinesebeauty #tiktok",
    }
    video_datas_fetch = handler(data["video_ids"])
    video_datas_transform = []
    for video in video_datas_fetch:
        title = getRandomTitle()
        temp = {
            "url": video["url"],
            "origin_title": video["title"],
            "thumb": video["thumbnail"],
            "source": video["source"],
            "link_download": video["medias"][0]["url"],
            "tags": video_info["tag"],
            "title": title,
            "des": video_info["des"],
        }
        print("DONE generate data", video["url"])
        video_datas_transform.append(temp)
    print("Trigger Upload YouTube Video")
    youtubeUploader(video_datas_transform)


def uploadMultiTimesYT(times):
    for i in range(times):
        print("Upload video #", i)
        uploadToYouTube()
        logger.info("Success upload video #" + str(i))
        # print("Success upload video #" + i)
        time.sleep(10)


if __name__ == "__main__":
    for i in range(20):
        logger.info("START Upload video # " + str(i))
        uploadToYouTube()
        logger.info("SUCCESSFUL upload video #" + str(i))
        time.sleep(10)
