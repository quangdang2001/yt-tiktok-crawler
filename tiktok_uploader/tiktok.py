import time, requests, datetime, hashlib, hmac, random, zlib, json, datetime
import requests, zlib, json, time, subprocess, string, secrets, os, sys
from fake_useragent import FakeUserAgentError, UserAgent
from requests_auth_aws_sigv4 import AWSSigV4
from tiktok_uploader.cookies import load_cookies_from_file
from tiktok_uploader.Browser import Browser
from tiktok_uploader.bot_utils import *
from tiktok_uploader import Config, Video, eprint
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Constants
_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"


def login(login_name: str):
    # Check if login name is already save in file.
    cookies = load_cookies_from_file(f"tiktok_session-{login_name}")
    session_cookie = next((c for c in cookies if c["name"] == "sessionid"), None)
    session_from_file = session_cookie is not None

    if session_from_file:
        print("Unnecessary login: session already saved!")
        return session_cookie["value"]

    browser = Browser.get()
    response = browser.driver.get("https://www.tiktok.com/upload?lang=vi")

    session_cookies = []
    # while not session_cookies:
    #     for cookie in browser.driver.get_cookies():
    #         if cookie["name"] in ["sessionid", "tt-target-idc"]:
    #             if cookie["name"] == "sessionid":
    #                 cookie_name = cookie
    #             session_cookies.append(cookie)
    time.sleep(60 * 5)
    for cookie in browser.driver.get_cookies():
        if cookie["name"] in ["sessionid", "tt-target-idc"]:
            if cookie["name"] == "sessionid":
                cookie_name = cookie
        session_cookies.append(cookie)
    print(session_cookies)
    # print("Session cookie found: ", session_cookie["value"])
    print("Account successfully saved.")
    browser.save_cookies(f"tiktok_session-{login_name}", session_cookies)
    browser.driver.quit()

    return cookie_name.get("value", "") if cookie_name else ""


def upload_video(
    session_user,
    video,
    title,
    schedule_time=0,
    allow_comment=1,
    allow_duet=0,
    allow_stitch=0,
    visibility_type=0,
    brand_organic_type=0,
    branded_content_type=0,
    ai_label=0,
    proxy=None,
):
    try:
        user_agent = UserAgent().random
    except FakeUserAgentError as e:
        user_agent = _UA
        print("[-] Could not get random user agent, using default")

    cookies = load_cookies_from_file(f"tiktok_session-{session_user}")

    session_id = next((c["value"] for c in cookies if c["name"] == "sessionid"), None)
    dc_id = next((c["value"] for c in cookies if c["name"] == "tt-target-idc"), None)
    csrfToken = next((c["value"] for c in cookies if c["name"] == "csrfToken"), None)
    csrf_session_id = next(
        (c["value"] for c in cookies if c["name"] == "csrf_session_id"), None
    )
    msToken = next((c["value"] for c in cookies if c["name"] == "msToken"), None)
    store_idc = next((c["value"] for c in cookies if c["name"] == "store-idc"), None)
    tt_target_idc_sign = next(
        (c["value"] for c in cookies if c["name"] == "tt-target-idc-sign"), None
    )
    tt_chain_token = next(
        (c["value"] for c in cookies if c["name"] == "tt_chain_token"), None
    )
    tt_csrf_token = next(
        (c["value"] for c in cookies if c["name"] == "tt_csrf_token"), None
    )
    sessionid_ss = next(
        (c["value"] for c in cookies if c["name"] == "sessionid_ss"), None
    )

    if not session_id:
        eprint("No cookie with Tiktok session id found: use login to save session id")
        sys.exit(1)
    if not dc_id:
        print(
            "[WARNING]: Please login, tiktok datacenter id must be allocated, or may fail"
        )
        dc_id = "useast2a"
    print("User successfully logged in.")
    print(f"Tiktok Datacenter Assigned: {dc_id}")

    print("Uploading video...")

    # Parameter validation,
    if schedule_time and (schedule_time > 864000 or schedule_time < 900):
        print("[-] Cannot schedule video in more than 10 days or less than 20 minutes")
        return False
    if len(title) > 2200:
        print("[-] The title has to be less than 2200 characters")
        return False
    if schedule_time != 0 and visibility_type == 1:
        print("[-] Private videos cannot be uploaded with schedule")
        return False

    # Check video length - 1 minute max, takes too long to run this.

    # Creating Session
    session = requests.Session()
    session.cookies.set("sessionid", session_id, domain=".tiktok.com")
    session.cookies.set("tt-target-idc", dc_id, domain=".tiktok.com")
    session.cookies.set("csrfToken", csrfToken, domain=".tiktok.com")
    session.cookies.set("csrf_session_id", csrf_session_id, domain=".tiktok.com")
    # session.cookies.set("msToken", msToken, domain=".tiktok.com")
    session.cookies.set("store-country-code", "vn", domain=".tiktok.com")
    session.cookies.set("store-country-code-src", "vn", domain=".tiktok.com")
    session.cookies.set("store-idc", store_idc, domain=".tiktok.com")
    session.cookies.set("tt-target-idc-sign", tt_target_idc_sign, domain=".tiktok.com")
    session.cookies.set("tt_chain_token", tt_chain_token, domain=".tiktok.com")
    session.cookies.set("tt_csrf_token", tt_csrf_token, domain=".tiktok.com")
    session.cookies.set("sessionid_ss", sessionid_ss, domain=".tiktok.com")

    session.verify = True

    headers = {
        "User-Agent": user_agent,
        "Accept": "application/json, text/plain, */*",
        "Tt-Csrf-Token": session.cookies.get("csrfToken"),
    }
    session.headers.update(headers)

    # Setting proxy if provided.
    # if proxy:
    #     session.proxies = {"http": proxy, "https": proxy}

    creation_id = generate_random_string(21, True)
    project_url = f"https://www.tiktok.com/api/v1/web/project/create/?creation_id={creation_id}&type=1&aid=1988"
    r = session.post(project_url)

    if not assert_success(project_url, r):
        return False

    # get project_id
    project_id = r.json()["project"]["project_id"]
    (
        video_id,
        session_key,
        upload_id,
        crcs,
        upload_host,
        store_uri,
        video_auth,
        aws_auth,
    ) = upload_to_tiktok(video, session)

    url = f"https://{upload_host}/upload/v1/{store_uri}?uploadID={upload_id}&phase=finish&uploadmode=part"
    headers = {
        "Authorization": video_auth,
        "Content-Type": "text/plain;charset=UTF-8",
    }
    data = ",".join([f"{i + 1}:{crcs[i]}" for i in range(len(crcs))])

    if proxy:
        r = requests.post(url, headers=headers, data=data, proxies=session.proxies)
        if not assert_success(url, r):
            return False
    else:
        r = requests.post(url, headers=headers, data=data)
        if not assert_success(url, r):
            return False

    print("CommitUploadInner")
    url = f"https://www.tiktok.com/top/v1?Action=CommitUploadInner&Version=2020-11-19&SpaceName=tiktok"
    data = '{"SessionKey":"' + session_key + '","Functions":[{"name":"GetMeta"}]}'

    r = session.post(url, auth=aws_auth, data=data)
    if not assert_success(url, r):
        return False

    # /video/transcode/enable Enable Video
    enable_video_url = f"https://www.tiktok.com/api/v1/video/transcode/enable/?video_id={video_id}&aid=1988"
    enable_resp = session.post(url=enable_video_url)
    print("Enable Vid resp:", enable_resp.status_code, enable_resp.json())

    #  Call get result until finish upload video
    print("Checking finish upload...")
    while True:
        check_finish_upload_url = f"https://www.tiktok.com/api/v1/video/transcode/result/?video_id={video_id}&aid=1988"
        check_finish_resp = session.get(url=check_finish_upload_url)
        isFinished = False
        if check_finish_resp.status_code == 200:
            isFinished = check_finish_resp.json()["finished"]
            print("Is finish upload video", isFinished)
        if isFinished:
            print("Finish upload video")
            break
        time.sleep(1)
    # publish video
    url = "https://www.tiktok.com"
    headers = {"user-agent": user_agent}

    r = session.head(url, headers=headers)
    if not assert_success(url, r):
        return False

    headers = {
        "content-type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "user-agent": user_agent,
        "Tt-Csrf-Token": session.cookies.get("csrfToken"),
        "Cookie": "; ".join(
            [f"{key}={value}" for key, value in session.cookies.get_dict().items()]
        ),
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Dest": "empty",
    }
    brand = ""

    if brand and brand[-1] == ",":
        brand = brand[:-1]
    markup_text, text_extra = convert_tags(title, session)
    data = {
        "upload_param": {
            "video_param": {
                "text": title,
                "text_extra": text_extra,
                "markup_text": markup_text,
                "poster_delay": 0,
            },
            "visibility_type": visibility_type,
            "allow_comment": allow_comment,
            "allow_duet": allow_duet,
            "allow_stitch": allow_stitch,
            "sound_exemption": 0,
            "geofencing_regions": [],
            "creation_id": creation_id,
            "is_uploaded_in_batch": False,
            "is_enable_playlist": False,
            "is_added_to_playlist": False,
            "tcm_params": r'"{\"commerce_toggle_info\":{}}"',
            "aigc_info": {"aigc_label_type": ai_label},
        },
        "project_id": project_id,
        "draft": "",
        "single_upload_param": [],
        "video_id": video_id,
        "creation_id": creation_id,
    }
    if schedule_time:
        data["upload_param"]["schedule_time"] = schedule_time + int(time.time())
    print("Waiting to finish processing video in Tiktok")
    time.sleep(5)  # Waiting for 20 minutes
    print("Start click on POST")

    url_config_update = (
        "https://www.tiktok.com/api/v1/web/project/update/config/?aid=1988"
    )
    url_payload_config = r"{\"url\":\"" + video_id + r"\"}"
    payload = (
        '{"project_id":"'
        + project_id
        + '","config":[{"type":1,"payload":"'
        + url_payload_config
        + '"},{"type":100,"payload":"%2F9j%2F4AAQSkZJRgABAQAAAQABAAD%2F4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb%2F2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDRENDg8QEBEQCgwSExIQEw8QEBD%2F2wBDAQMDAwQDBAgEBAgQCwkLEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBD%2FwAARCABGACcDASIAAhEBAxEB%2F8QAFQABAQAAAAAAAAAAAAAAAAAAAAn%2FxAAUEAEAAAAAAAAAAAAAAAAAAAAA%2F8QAFAEBAAAAAAAAAAAAAAAAAAAAAP%2FEABQRAQAAAAAAAAAAAAAAAAAAAAD%2F2gAMAwEAAhEDEQA%2FAJVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%2F%2FZ"}]}'
    )
    update_resp = session.post(url=url_config_update, headers=headers, data=payload)
    print("update_config", update_resp.json()["status_msg"])

    uploaded = False
    retryAttemps = 0
    while True:
        try:
            mstoken = session.cookies.get("msToken")
            # xbogus = subprocess_jsvmp(os.path.join(os.getcwd(), "tiktok_uploader", "./x-bogus.js"), user_agent, f"app_name=tiktok_web&channel=tiktok_web&device_platform=web&aid=1988&msToken={mstoken}")
            signatures = subprocess_jsvmp(
                os.path.join(
                    os.getcwd(), "tiktok_uploader", "tiktok-signature", "browser.js"
                ),
                user_agent,
                f"https://www.tiktok.com/api/v1/web/project/post/?app_name=tiktok_web&channel=tiktok_web&device_platform=web&aid=1988&msToken={mstoken}",
            )
            tt_output = json.loads(signatures)["data"]
            project_post_dict = {
                "app_name": "tiktok_web",
                "channel": "tiktok_web",
                "device_platform": "web",
                "aid": 1988,
                "msToken": mstoken,
                "X-Bogus": tt_output["x-bogus"],
                "_signature": tt_output["signature"],
                # "X-TT-Params": tt_output["x-tt-params"],  # not needed rn.
            }
            url = f"https://www.tiktok.com/api/v1/web/project/post/"
            r = session.request(
                "POST",
                url,
                params=project_post_dict,
                data=json.dumps(data),
                headers=headers,
            )
            try:
                print("Post resp", r.content)
                if r.json()["status_msg"] == "You are posting too fast. Take a rest.":
                    print("[-] You are posting too fast, try later again")
                    return False
                uploaded = True
                break
            except Exception as e:
                print("[-] Waiting for TikTok to process video...", str(retryAttemps))
                retryAttemps += 1
                if retryAttemps >= 100:
                    print("[-] Reach max retry attemps")
                    return False
                time.sleep(0.5)  # wait 1.5 seconds before asking again.
        except Exception as e:
            print("Got exception when proceess", e)

    print("Process video DONE")

    if not uploaded:
        print("[-] Could not upload video")
        return False
    print("Check if video uploaded successfully")
    # Check if video uploaded successfully
    url = f"https://www.tiktok.com/api/v1/web/project/list/?aid=1988"

    r = session.get(url)
    if not assert_success(url, r):
        return False
    # print(r.json()["infos"])
    for j in r.json()["infos"]:
        if j["creationID"] == creation_id:
            if (
                j["tasks"][0]["status_msg"] == "Y project task init"
                or j["tasks"][0]["status_msg"] == "Success"
            ):
                print("[+] Video uploaded successfully.")
                return True
            print(
                f"[-] Video could not be uploaded: {j['tasks'][0]['status_msg']}, json:"
            )
            return False


def upload_to_tiktok(video_file, session):
    url = "https://www.tiktok.com/api/v1/video/upload/auth/?aid=1988"
    r = session.get(url)
    if not assert_success(url, r):
        return False

    aws_auth = AWSSigV4(
        "vod",
        region="ap-singapore-1",
        aws_access_key_id=r.json()["video_token_v5"]["access_key_id"],
        aws_secret_access_key=r.json()["video_token_v5"]["secret_acess_key"],
        aws_session_token=r.json()["video_token_v5"]["session_token"],
    )
    # with open(os.path.join(os.getcwd(), Config.get().videos_dir, video_file), "rb") as f:
    # 	video_content = f.read()
    print("Fetching video")
    fetch_vid_resp = requests.get(url=video_file)
    video_content = fetch_vid_resp.content
    file_size = len(video_content)
    url = f"https://www.tiktok.com/top/v1?Action=ApplyUploadInner&Version=2020-11-19&SpaceName=tiktok&FileType=video&IsInner=1&X-Amz-Expires=604800"
    print("Fetching video DONE")

    r = session.get(url, auth=aws_auth)
    if not assert_success(url, r):
        return False

    # upload chunks
    upload_node = r.json()["Result"]["InnerUploadAddress"]["UploadNodes"][0]
    video_id = upload_node["Vid"]
    store_uri = upload_node["StoreInfos"][0]["StoreUri"]
    video_auth = upload_node["StoreInfos"][0]["Auth"]
    upload_host = upload_node["UploadHost"]
    session_key = upload_node["SessionKey"]
    chunk_size = 5242880
    chunks = []
    i = 0
    while i < file_size:
        chunks.append(video_content[i : i + chunk_size])
        i += chunk_size
    crcs = []
    upload_id = str(uuid.uuid4())
    # for i in range(len(chunks)):
    # 	chunk = chunks[i]
    # 	crc = crc32(chunk)
    # 	crcs.append(crc)
    # 	url = f"https://{upload_host}/upload/v1/{store_uri}?partNumber={i + 1}&uploadID={upload_id}&phase=transfer"
    # 	print(url)
    # 	headers = {
    # 		"Authorization": video_auth,
    # 		"Content-Type": "application/octet-stream",
    # 		"Content-Disposition": 'attachment; filename="undefined"',
    # 		"Content-Crc32": crc,
    # 	}

    # 	r = session.post(url, headers=headers, data=chunk)
    # 	print("Resp upload part",r.json())
    crc = crc32(video_content)
    crcs.append(crc)
    headers = {
        "Authorization": video_auth,
        "Content-Type": "application/octet-stream",
        "Content-Disposition": 'attachment; filename="undefined"',
        "Content-Crc32": crc,
    }
    url_post = f"https://{upload_host}/upload/v1/{store_uri}"
    resp = session.post(url=url_post, headers=headers, data=video_content)
    print(resp.json())
    return (
        video_id,
        session_key,
        upload_id,
        crcs,
        upload_host,
        store_uri,
        video_auth,
        aws_auth,
    )


if __name__ == "__main__":
    upload_video(
        "letdat",
        "https://v5-dy-o-abtest.zjcdn.com/86a7d115ce73c1f9025781a4517a2933/66018e01/video/tos/cn/tos-cn-ve-15/oUDQPANhGgDAyKoDZEBjerA1BPI9fnAJzHRgbU/?a=1128&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1157&bt=1157&cs=0&ds=6&ft=iusdFLqoQmo0PDwYfxnaQ950U4i6JE.C~&mime_type=video_mp4&qs=0&rc=Ozk7N2Y1NzU4OzxoPDw5OkBpM2l4bTo6Zjg0ajMzNGkzM0A2YWA2YC41Xi8xYzIyMzYxYSNoanBgcjQwMGJgLS1kLTBzcw%3D%3D&btag=10e00088000&cc=46&cquery=100d&dy_q=1711374313&feature_id=59cb2766d89ae6284516c6a254e9fb61&l=202403252145135CE6809A80C85412C3EC",
        "test",
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
