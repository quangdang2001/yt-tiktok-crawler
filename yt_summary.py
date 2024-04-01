from Logger import logger
from video_utils import create_summary_video, delete_resource
from youtube_uploader import youtubeUploader, pinedream_config

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


def upload_load_summary_video(config):
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
    upload_load_summary_video(pinedream_config["quangdang20013"])
    upload_load_summary_video(pinedream_config["ledat3002"])
    upload_load_summary_video(pinedream_config["quangdang2001ver2"])
    upload_load_summary_video(pinedream_config["nmy786646"])
    upload_load_summary_video(pinedream_config["threeguytravel"])
