import requests, time, logging, colorlog


def get_video_info(prefix, vid_id):
    url = "https://snaptikapp.me/wp-json/aio-dl/video-data/"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {"url": prefix + vid_id}
    result = requests.post(url, body, headers)
    status_code = result.status_code
    data = result.json()
    retryAttemps = 0
    while status_code != 200:
        print("retry with status code", status_code, vid_id)
        result = requests.post(url, body, headers)
        status_code = result.status_code
        retryAttemps += 1
        if retryAttemps >= 5:
            print("Reach max attemp retry times when Fetch video data")
            return None
        if status_code != 200:
            continue
        data = result.json()
    return data
