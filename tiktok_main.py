import requests, time, logging, colorlog
import json
from title_generator import getRandomTitle
from video_ids_random import getRandomVidId
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


def uploadVidToTiktok():
    logger.info("Start upload video to tiktok")
    vid_id = getRandomVidId(1)[0]
    title = getRandomTitle()
    tags = " #douyin #hotgirls #cutegirls #beautiful #dance #beauty #cosplay #streetfashion #tiktok #gaixinh #chandai #quyenru #nongbong"
    title = title + tags
    prefix = "https://www.douyin.com/video/"
    logger.info("Start fetch video data")
    video_info = get_video_info(prefix, vid_id)
    video_url = video_info["medias"][0]["url"]
    logger.info("Fetch video data DONE")
    logger.info("Start upload to Tiktok")
    return tiktok.upload_video(
        "quangdangver02",
        video_url,
        title,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        None,
    )


if __name__ == "__main__":
    for i in range(10):
        logger.info("Upload video #" + str(i))
        retryAttemps = 0
        while True:
            result = uploadVidToTiktok()
            if result:
                logger.info("[+++++]Upload Success video #" + str(i))
                break
            else:
                retryAttemps += 1
                logger.error(
                    "Upload video FAILED, will retry"
                    + str(retryAttemps)
                    + " #"
                    + str(i)
                )
        time.sleep(60)
