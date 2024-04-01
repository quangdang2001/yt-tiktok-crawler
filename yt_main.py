import json
import requests, time
from title_generator import getRandomTitle
from video_ids_random import getRandomVidId
from youtube_uploader import youtubeUploader, pinedream_config
from tiktok_uploader import tiktok
from common import get_video_info
from Logger import logger
from video_utils import create_summary_video, delete_resource

des = """
In this captivating video, you'll witness the extraordinary talents of an Asian sensation as she gracefully showcases her dance prowess and stylish street fashion. Hailing as a rising star on Douyin and TikTok, her charismatic presence, along with her striking beauty, will undoubtedly leave you mesmerized.

Don't forget to show your appreciation by giving a like and subscribing to her channel. By subscribing, you'll stay updated with her latest and incredible videos.

#asiangirl #chinesegirl #girl #beautifulgirl #legs #charm #model #sexy #subscribe
#douyin #bodygoals #fashionstyle #model #dance #beauty #cosplay  #streetfashion #tiktok
"""


video_info = {
    "tag": [
        "douyin",
        "chinesegirl",
        "bodygoals",
        "fashionstyle",
        "model",
        "dance",
        "beauty",
        "cosplay",
        "streetfashion",
        "tiktok",
        "gaixink",
        "chandai",
        "quyenru",
        "nongbong",
    ],
    "des": des,
}


def handler(vid_list):
    r = []
    prefix = "https://www.douyin.com/video/"
    list_vid_id = vid_list
    for id in list_vid_id:
        print("Fetch data video #", id)
        result = get_video_info(prefix, id)
        if result == None:
            continue
        r.append(result)
        print("Done fetch data video #", id)
    # Export the data for use in future steps
    return r


def get_randome_yt_vid():
    data = {"video_ids": getRandomVidId(1)}

    video_datas_fetch = handler(data["video_ids"])

    retryAttemps = 0
    while len(video_datas_fetch) == 0:
        data = {"video_ids": getRandomVidId(1)}
        video_datas_fetch = handler(data["video_ids"])
        retryAttemps += 1
        if retryAttemps >= 5:
            return False

    return video_datas_fetch


def uploadToYouTube(config):
    video_datas_fetch = get_randome_yt_vid()
    if video_datas_fetch == False:
        return False
    while video_datas_fetch[0]["medias"][0]["size"] < 11264000:
        print("Video quality is lower than 11MB, skipp")
        video_datas_fetch = get_randome_yt_vid()

    video_datas_transform = []
    for video in video_datas_fetch:
        random_title = getRandomTitle()
        print("Process ", random_title)
        title = random_title
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
    youtubeUploader(video_datas_transform, config)
    return True


def uploadMultiTimesYT(times, config):
    for i in range(times):
        logger.info("START Upload video # " + str(i))
        result = uploadToYouTube(config)
        if result:
            logger.info("SUCCESSFUL upload video #" + str(i))
        else:
            logger.error("FAILED upload video #" + str(i))
        time.sleep(10)


def upload_load_summary_video(config):
    # final_video_fetch = []
    # while len(final_video_fetch) < 10:
    #     video_ids = getRandomVidId(1)
    #     video_datas_fetch = handler(video_ids)
    #     if len(video_datas_fetch) == 0:
    #         print("Fetch video failed will retry")
    #         continue
    #     video_data = video_datas_fetch[0]
    #     if video_data["medias"][0]["size"] < 11264000:
    #         print("Video quality is lower than 11MB, skipp")
    #         continue
    #     final_video_fetch.append(video_datas_fetch[0])
    #     logger.info(
    #         "[++++++++++++] DONE"
    #         + str(len(final_video_fetch))
    #         + "/"
    #         + "30"
    #         + "[++++++++++++]"
    #     )
    # urls = []
    # thumbnails = []

    # for video in final_video_fetch:
    #     print("Append Link", video["url"])
    #     urls.append(video["medias"][0]["url"])
    #     thumbnails.append(video["thumbnail"])
    summary_video = create_summary_video()

    video_datas_transform = {
        "url": "url",
        "origin_title": "title",
        "thumb": "thumb",
        "source": "douyin",
        "link_download": summary_video["url"],
        "tags": video_info["tag"],
        "title": "🎧 NHẠC TIK TOK - Tổng Hợp Những Đoạn Nhạc Chill / Singing Cực Hay Giúp Thư Giãn",
        "des": video_info["des"],
    }
    youtubeUploader([video_datas_transform], config)
    # delete_resource(summary_video["public_id"])
    return summary_video


if __name__ == "__main__":
    logger.info(
        "[++++++++++++++++++++++++++++++++++++++++++++++] PROCESS Douyin Girl (quangdang20013) [++++++++++++++++++++++++++++++++++++++++++++++]"
    )
    uploadMultiTimesYT(10, pinedream_config["quangdang20013"])
    logger.info(
        "[++++++++++++++++++++++++++++++++++++++++++++++] PROCESS Miny Girl (ledat3002) [++++++++++++++++++++++++++++++++++++++++++++++]"
    )
    uploadMultiTimesYT(10, pinedream_config["ledat3002"])
    logger.info(
        "[++++++++++++++++++++++++++++++++++++++++++++++] PROCESS Xinh Mina (quangdang2001ver2) [++++++++++++++++++++++++++++++++++++++++++++++]"
    )
    uploadMultiTimesYT(10, pinedream_config["quangdang2001ver2"])
    logger.info(
        "[++++++++++++++++++++++++++++++++++++++++++++++] PROCESS NyMie (nmy786646) [++++++++++++++++++++++++++++++++++++++++++++++]"
    )
    uploadMultiTimesYT(10, pinedream_config["nmy786646"])
    logger.info(
        "[++++++++++++++++++++++++++++++++++++++++++++++] PROCESS Ana Mie (threeguytravel) [++++++++++++++++++++++++++++++++++++++++++++++]"
    )
    uploadMultiTimesYT(10, pinedream_config["threeguytravel"])
