import random, os


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


def getRandomVidId(number):
    folder_path = "videos_quality/"
    full_path = os.path.join(os.getcwd(), folder_path)
    file_names = list_files_in_folder(full_path)

    file_name = folder_path + random.choice(file_names)

    print("Prcess file", file_name)
    with open(file_name, "r", encoding="utf8") as file:
        # Read all lines into a list
        vid_ids = file.readlines()
    vid_id = []
    for i in range(number):
        vid_id.append(random.choice(vid_ids).replace("\n", ""))
    print("Will upload ids:", vid_id, "of", file_name)
    return vid_id


if __name__ == "__main__":
    # print(list_files_in_folder("video_ids"))
    getRandomVidId(5)
