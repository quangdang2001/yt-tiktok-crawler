import random, os
from common import get_video_info
import uuid
from Logger import logger


def list_files_in_folder(folder_path):
    files = []
    # Iterate over all the files and directories in the specified folder
    for file_name in os.listdir(folder_path):
        # Join the folder path and the file/directory name to get the full path
        full_path = os.path.join(folder_path, file_name)
        # Check if it's a file (not a directory)
        if os.path.isfile(full_path):
            files.append(file_name)
    return files


prefix = "https://www.douyin.com/video/"


def get_quality_vid():
    folder_path = "video_ids"
    full_path = os.path.join(os.getcwd(), folder_path)
    file_names = list_files_in_folder(full_path)
    print(file_names)
    vid_approved = []
    total_vid = 0
    random_final_file_name = str(uuid.uuid4())

    for file_name in file_names:
        logger.info("File name " + file_name)
        full_path = "video_ids/" + file_name
        with open(full_path, "r", encoding="utf8") as file:
            # Read all lines into a list
            vid_ids = file.readlines()
        total_vid += len(vid_ids)
        for vid_id in vid_ids:
            vid_id = vid_id.replace("\n", "")
            try:
                vid_info = get_video_info(prefix, vid_id)
            except Exception as e:
                logger.error("Fetch Failed for " + vid_id)
                print(e)
                continue
            if vid_info != None and vid_info["medias"][0]["size"] >= 11264000:
                logger.info("APPROVED")
                vid_approved.append(vid_id)
                with open(f"videos_quality/video_ids.txt", "a") as file:
                    # Write each element of the array into the file
                    file.write(str(vid_id) + "\n")
            else:
                logger.error("DENIED")
    logger.info("Video approved:" + str(len(vid_approved)) + "/" + str(total_vid))
    # Open a file in write mode
    # with open(f"videos_quality/{random_final_file_name}.txt", "w") as file:
    #     # Write each element of the array into the file
    #     for item in vid_approved:
    #         file.write(str(item) + "\n")


if __name__ == "__main__":
    get_quality_vid()
