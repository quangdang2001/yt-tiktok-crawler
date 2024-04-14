import glob, os
from moviepy.editor import VideoFileClip, concatenate_videoclips
import cloudinary, requests
import uuid, json
from natsort import natsorted
from moviepy.video.fx.resize import resize
from PIL import Image
from video_ids_random import getRandomVidId
from Logger import logger
from common import get_video_info

# Import the cloudinary.api for managing assets
import cloudinary.api, PIL

# Import the cloudinary.uploader for uploading assets
import cloudinary.uploader

cloudinary.config(
    cloud_name="quangdangcloud",
    api_key="738222114899535",
    api_secret="V37UHtOmQ62U1VH-kXyd7kRLgf4",
    secure=False,
)

# video_file_list = [
#     "https://v5-dy-o-abtest.zjcdn.com/8fe2320d58780ca6be2452f4324fbdc0/6607a791/video/tos/cn/tos-cn-ve-15/osPeD9hLST99npDJA8A5Q4gIztAAfAMzMB1yKE/?a=1128&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=581&bt=581&cs=0&ds=6&ft=iusdFLqoQmo0PDpQj4naQ950U4i6JE.C~&mime_type=video_mp4&qs=0&rc=NTQ3Z2Q8ZTQ2Ozo6Zzk6aUBpam07eTY6ZnZucTMzNGkzM0AuMl4tYmNeNjIxNGM2LjQtYSM0bS9ycjRvLWhgLS1kLTBzcw%3D%3D&btag=10e00088000&cc=46&cquery=103R_103S_100d_104i_103Q&dy_q=1711774071&feature_id=f0150a16a324336cda5d6dd0b69ed299&l=20240330124750DFCDCD02A7C1BC71D455",
#     "https://v5-dy-o-abtest.zjcdn.com/6fd965c19785015192818f4dd33e1ee6/6607a865/video/tos/cn/tos-cn-ve-15/oUVbEeLsA0g9BnN7IAQAlsrKfwDAzlnDgNBMQX/?a=1128&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=570&bt=570&cs=0&ds=6&ft=iusdFLqoQmo0PD6Uj4naQ950U4i6JE.C~&mime_type=video_mp4&qs=0&rc=ZWRlOjxnaTNoNzo0Z2g7NUBpM3dvNTk6ZnM3cTMzNGkzM0AvL18vNC0tNS0xNS8yXzBiYSNkLXBvcjRfMjNgLS1kLTBzcw%3D%3D&btag=50e00088000&cc=46&cquery=104i_103Q_103R_103S_100d&dy_q=1711774288&feature_id=f0150a16a324336cda5d6dd0b69ed299&l=20240330125128D797F0FCA824C07685CF",
#     "https://v3-dy-o.zjcdn.com/c186267fc29713da6337938c6a3ffca5/6607a8d7/video/tos/cn/tos-cn-ve-15c001-alinc2/ogK9nDg5QflgM4AfIBJB0D8DBR4nQAbKkLABBr/?a=1128&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1278&bt=1278&cs=0&ds=6&ft=4iuxFMZj8Zmo0A_NF-4jV~m9FAWrKsd.&mime_type=video_mp4&qs=0&rc=ODM4ZmlkNzg1PDU7N2doOUBpM3Rscjw6ZnRkbzMzNGkzM0BiMzYyXjIxNmAxL14xYC42YSNiYDQ0cjRvLS9gLS1kLTBzcw%3D%3D&btag=50e00088000&cc=1f&cquery=104i_103Q_103R_103S_100d&dy_q=1711774398&feature_id=f0150a16a324336cda5d6dd0b69ed299&l=202403301253183623CA292DE6BC771739",
# ]


# loaded_video_list = []

# for video in video_file_list:
#     print(f"Adding video file:{video}")
#     video_file_clip = VideoFileClip(video)
#     loaded_video_list.append(video_file_clip)

# final_clip = concatenate_videoclips(loaded_video_list, method="compose")
# merged_video_name = "test_vid"

# final_clip.write_videofile(f"result/{merged_video_name}.mp4")

# randome_vid_id = str(uuid.uuid4())

# upload_resp = cloudinary.uploader.upload_large(
#     f"result/{merged_video_name}.mp4",
#     resource_type="video",
#     public_id=randome_vid_id,
#     folder="yt",
#     chunk_size=6000000,
# )
# print(json.dumps(upload_resp))


# delete_resp = cloudinary.api.delete_resources(
#     f"yt/{randome_vid_id}", resource_type="video", type="upload"
# )
# print(json.dumps(delete_resp))
merged_video_name = "result_vid"


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


def fetch_videos(number):
    final_video_fetch = []
    while len(final_video_fetch) < number:
        video_ids = getRandomVidId(1)
        video_datas_fetch = handler(video_ids)
        if len(video_datas_fetch) == 0:
            print("Fetch video failed will retry")
            continue
        video_data = video_datas_fetch[0]
        if video_data["medias"][0]["size"] < 11264000:
            print("Video quality is lower than 11MB, skipp")
            continue
        final_video_fetch.append(video_datas_fetch[0])
        logger.info(
            "[++++++++++++] DONE"
            + str(len(final_video_fetch))
            + "/"
            + str(number)
            + "[++++++++++++]"
        )
    urls = []
    thumbnails = []

    for video in final_video_fetch:
        print("Append Link", video["url"])
        urls.append(video["medias"][0]["url"])
        thumbnails.append(video["thumbnail"])
    return urls


def merge_vid():
    max_vid_fetch = 3
    videos = fetch_videos(max_vid_fetch)
    loaded_video_list = []
    loaded_video_list.append(VideoFileClip(videos[0]).resize(height=1920))
    loaded_video_list.append(VideoFileClip(videos[1]).resize(height=1920))
    loaded_video_list.append(VideoFileClip(videos[2]).resize(height=1920))
    final_clip = concatenate_videoclips(loaded_video_list, method="compose")
    final_clip.write_videofile(f"result/1.mp4")

    videos = fetch_videos(max_vid_fetch)
    loaded_video_list = []
    loaded_video_list.append(VideoFileClip(videos[0]).resize(height=1920))
    loaded_video_list.append(VideoFileClip(videos[1]).resize(height=1920))
    loaded_video_list.append(VideoFileClip(videos[2]).resize(height=1920))
    final_clip = concatenate_videoclips(loaded_video_list, method="compose")
    final_clip.write_videofile(f"result/2.mp4")

    videos = fetch_videos(max_vid_fetch)
    loaded_video_list = []
    loaded_video_list.append(VideoFileClip(videos[0]).resize(height=1920))
    loaded_video_list.append(VideoFileClip(videos[1]).resize(height=1920))
    loaded_video_list.append(VideoFileClip(videos[2]).resize(height=1920))
    final_clip = concatenate_videoclips(loaded_video_list, method="compose")
    final_clip.write_videofile(f"result/3.mp4")

    videos = fetch_videos(max_vid_fetch)
    loaded_video_list = []
    loaded_video_list.append(VideoFileClip(videos[0]).resize(height=1920))
    loaded_video_list.append(VideoFileClip(videos[1]).resize(height=1920))
    loaded_video_list.append(VideoFileClip(videos[2]).resize(height=1920))
    final_clip = concatenate_videoclips(loaded_video_list, method="compose")
    final_clip.write_videofile(f"result/4.mp4")

    videos = fetch_videos(max_vid_fetch)
    loaded_video_list = []
    loaded_video_list.append(VideoFileClip(videos[0]).resize(height=1920))
    loaded_video_list.append(VideoFileClip(videos[1]).resize(height=1920))
    loaded_video_list.append(VideoFileClip(videos[2]).resize(height=1920))
    final_clip = concatenate_videoclips(loaded_video_list, method="compose")
    final_clip.write_videofile(f"result/5.mp4")

    videos = fetch_videos(max_vid_fetch)
    loaded_video_list = []
    loaded_video_list.append(VideoFileClip(videos[0]).resize(height=1920))
    loaded_video_list.append(VideoFileClip(videos[1]).resize(height=1920))
    loaded_video_list.append(VideoFileClip(videos[2]).resize(height=1920))
    final_clip = concatenate_videoclips(loaded_video_list, method="compose")
    final_clip.write_videofile(f"result/6.mp4")

    loaded_video_list = []
    loaded_video_list.append(VideoFileClip("result/1.mp4").resize(height=1920))
    loaded_video_list.append(VideoFileClip("result/2.mp4").resize(height=1920))
    loaded_video_list.append(VideoFileClip("result/3.mp4").resize(height=1920))
    loaded_video_list.append(VideoFileClip("result/4.mp4").resize(height=1920))
    loaded_video_list.append(VideoFileClip("result/5.mp4").resize(height=1920))
    loaded_video_list.append(VideoFileClip("result/6.mp4").resize(height=1920))
    final_clip = concatenate_videoclips(loaded_video_list, method="compose")
    final_clip.write_videofile(f"result/{merged_video_name}.mp4")


def create_summary_video():
    # loaded_video_list = []

    # for video in video_file_list:
    #     print(f"Adding video file:{video}")
    #     # root_vid = VideoFileClip(f"result/{merged_video_name}.mp4")
    #     loaded_video_list.append(VideoFileClip(video).resize(height=1080))
    # final_clip = concatenate_videoclips(loaded_video_list, method="compose")

    # final_clip.write_videofile(f"result/{merged_video_name}.mp4")
    merge_vid()
    randome_vid_id = str(uuid.uuid4())

    upload_resp = cloudinary.uploader.upload_large(
        f"result/{merged_video_name}.mp4",
        resource_type="video",
        public_id=randome_vid_id,
        folder="yt",
        chunk_size=6000000,
    )
    url = upload_resp["url"]
    public_id = upload_resp["public_id"]
    if url == None:
        print("Upload summary video to cloudinary FAILED")
        return None
    print("Upload summary video to cloudinary SUCCESS")
    return {"url": url, "public_id": public_id}


def delete_resource(public_id):
    delete_resp = cloudinary.api.delete_resources(
        public_id, resource_type="video", type="upload"
    )
    print("Deleted summary video in cloudinary SUCCESS")


new_width = 1920
new_height = 1080


def concatVideos(path):
    # currentVideo = None
    # # List all files in the directory and read points from text files one by one

    # for filePath in natsorted(os.listdir(path)):
    #     if filePath.endswith(".mp4"):
    #         if currentVideo == None:
    #             currentVideo = VideoFileClip(path + filePath).resize(height=1920)
    #             continue
    #         video_2 = VideoFileClip(path + filePath).resize(height=1920)
    #         width, height = video_2.size
    #         print(width, height)
    #         currentVideo = concatenate_videoclips([currentVideo, video_2])
    # # currentVideo = concatenate_videoclips(list_video)
    # currentVideo.write_videofile("export.mp4")
    loaded_video_list = []

    for video in path:
        print(f"Adding video file:{video}")
        loaded_video_list.append(VideoFileClip(video).resize(height=1080))
    final_clip = concatenate_videoclips(loaded_video_list, method="compose")
    final_clip.write_videofile("export.mp4")


if __name__ == "__main__":
    # create_summary_video(["video_test"])
    # concatVideos(["video_test/download (3).mp4", "video_test/download (4).mp4"])
    # create_summary_video2(
    #     [
    #         "https://v11-o.douyinvod.com/c46c19aa7e023d10a3e3604b4e28fbc7/66085cd5/video/tos/cn/tos-cn-v-0015c002-alinc2/okB4AcO2BfCAgAbAEyhzIwtLEAsYgmGZACzFZe/?a=1128&ch=0&cr=0&dr=0&cd=0%7C0%7C0%7C0&cv=1&br=30558&bt=30558&ft=iusdFLqoQmo0PDNe5NnaQ950U4i6JE.C~&mime_type=video_mp4&qs=13&rc=amhzOTs6ZjVxcDMzNGkzM0BpamhzOTs6ZjVxcDMzNGkzM0AyZjVkcjRvM21gLS1kLS9zYSMyZjVkcjRvM21gLS1kLS9zcw%3D%3D&btag=10e00048000&cc=3e&cquery=100y&dy_q=1711820473&l=202403310141135AC2A4ECCB3BFCD39685",
    #         "https://v11-o.douyinvod.com/14409f23af5dedb2709bfe400ae4d60e/66085ee9/video/tos/cn/tos-cn-v-0015c800/13e6045afec241e2bb9c937e5a46d9d9/?a=1128&ch=0&cr=0&dr=0&cd=0%7C0%7C0%7C0&cv=1&br=9650&bt=9650&ds=4&ft=iusdFLqoQmo0PD6zYNnaQ950U4i6JE.C~&mime_type=video_mp4&qs=13&rc=ajx4NWY6ZmwzOjMzNGkzM0Bpajx4NWY6ZmwzOjMzNGkzM0BmZ2hmcjQwbzVgLS1kLWFzYSNmZ2hmcjQwbzVgLS1kLWFzcw%3D%3D&btag=10e00048000&cc=3e&cquery=100y&dy_q=1711821008&l=202403310150087EE6153A3FA44ED9C777",
    #     ]
    # )
    merge_vid()
