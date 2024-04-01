import requests, time, logging, colorlog, json
from Logger import logger

pinedream_config = {
    "ledat3002": {
        "pdsid": "5505f07ffd3f766450a5dc2f5069a949",
        "deploymentId": "d_Wpse57o4",
        "orgId": "o_v1IRzOb",
        "namespace": "upload_video",
        "emitId": "2eBjgVSCmTbY8JGKfoSTGEuv7Fm",
        "emitterId": "hi_eqHm2Oj",
    },
    "quangdang20013": {
        "pdsid": "d17f3151769b76e8a5f95bfd9e3621ad",
        "deploymentId": "d_YGsWRKE8",
        "orgId": "o_KgI8zdv",
        "namespace": "upload_video",
        "emitId": "2eEF6UKpn2oZ9xwg4WIxXWZNgxj",
        "emitterId": "hi_4EHGYmy",
    },
    "quangdang2001ver2": {
        "pdsid": "5326c7e036cc30598fb824ba078dfcb1",
        "deploymentId": "d_BBsKboal",
        "orgId": "o_3EIp9Mw",
        "namespace": "upload_video",
        "emitId": "2eEFguqRqX9Jxf8ce4UxLLbj51U",
        "emitterId": "hi_2VHPMDY",
    },
    "nmy786646": {
        "pdsid": "2cd6d14e3bf99a9af4c008bf4544dfd1",
        "deploymentId": "d_xRsmq291",
        "orgId": "o_NeImARw",
        "namespace": "upload_video",
        "emitId": "2eEGBbj8xdsBexukAsr6jv2Bp4a",
        "emitterId": "hi_JYHye2K",
    },
    "threeguytravel": {
        "pdsid": "e83ee34de46ccaad62f1ecb093ba5890",
        "deploymentId": "d_APspk3Ak",
        "orgId": "o_XGI8bOo",
        "namespace": "upload_video",
        "emitId": "2eH4oPNIhhmKmEa6mHSxdyrBNEp",
        "emitterId": "hi_6LHDkVV",
    },
}


def pinedream_payload(event, config):
    return {
        "operationName": "executeTestRequest",
        "query": "mutation executeTestRequest($ancestorIds: [String!], $childIds: [String!], $deploymentId: String!, $endNamespace: String, $endPhase: StepPhaseEnum, $lambdaMakerSuffix: String, $orgId: String, $sourceEmit: EmitInput, $startNamespace: String, $startPhase: StepPhaseEnum, $traceId: String, $triggerOnly: Boolean, $useLabyrinth: Boolean) {  my(orgId: $orgId) {    executeTestRequest(      ancestorIds: $ancestorIds      childIds: $childIds      deploymentId: $deploymentId      endStepNamespace: $endNamespace      endStepPhase: $endPhase      executionTraceId: $traceId      lambdaMakerSuffix: $lambdaMakerSuffix      sourceEmit: $sourceEmit      startStepNamespace: $startNamespace      startStepPhase: $startPhase      triggerOnly: $triggerOnly      useLabyrinth: $useLabyrinth    ) {      errors      executionTraceId      stepErrors {        namespace        error        __typename      }      __typename    }    __typename  }}",
        "variables": {
            "deploymentId": config["deploymentId"],
            "endNamespace": config["namespace"],
            "orgId": config["orgId"],
            "sourceEmit": {
                "event": event,
                "indexId": "1711241425886-0",
                "indexedAtMs": 1711241425886,
                "metadata": {
                    "emitId": config["emitId"],
                    "emitterId": config["emitterId"],
                    "name": "",
                    "summary": "POST /",
                },
            },
            "startNamespace": config["namespace"],
        },
    }


def youtubeUploader(event, config):

    url = "https://api.pipedream.com/graphql"
    header = {
        "Content-Type": "application/json",
        "cookie": f'pdsid={config["pdsid"]}',
    }
    payload = pinedream_payload(event, config)
    resp = requests.post(url=url, json=payload, headers=header)
    if resp.status_code != 200:
        print("Upload failed ", resp.status_code)
        return
    execution_trace_id = resp.json()["data"]["my"]["executeTestRequest"][
        "executionTraceId"
    ]
    param_check_status = {
        "operationName": "executionTrace",
        "variables": {
            "id": execution_trace_id,
            "includeTrigger": True,
            "namespaces": "null",
        },
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "95a4f663471f2e4664ca77cb3f5c48d9ef4a670d65d1544422e8d2fa63c2904d",
                "version": 1,
            }
        },
    }
    # check_resp = requests.post(url=url, params=param_check_status, headers=header)
    check_url = f"https://api.pipedream.com/graphql?operationName=executionTrace&variables=%7B%22id%22%3A%22{execution_trace_id}%22%2C%22includeTrigger%22%3Atrue%2C%22namespaces%22%3Anull%7D&extensions=%7B%22persistedQuery%22%3A%7B%22sha256Hash%22%3A%2295a4f663471f2e4664ca77cb3f5c48d9ef4a670d65d1544422e8d2fa63c2904d%22%2C%22version%22%3A1%7D%7D"
    check_resp = requests.request("GET", url=check_url, headers=header)

    if check_resp.status_code != 200:
        logger.error("Upload failed " + str(resp.content))
        return

    if check_resp.json()["data"]["executionTrace"]["trace"]["state"] == "ERROR":
        logger.error(
            "Upload failed "
            + json.dumps(check_resp.json()["data"]["executionTrace"]["trace"])
        )
        return

    logger.info(
        "[++++++++++++++++++++++++++++++++] Process video SUCCESS [++++++++++++++++++++++++++++++++]"
    )


if __name__ == "__main__":
    youtubeUploader(
        [
            {
                "des": "Kênh chuyên về tiktok, douyin gái xink Trung Quốc. #douyin #chinesegirl #hotgirls #beautifulgirls #cutegirls #beautifulchinesegirls #bodygoals #fashionstyle #model #dance #beauty #cosplay #sexylegs #asianbeauty #streetfashion #chinesebeauty #tiktok",
                "link_download": "https://v11-o.douyinvod.com/1d2c8b71ccf38c6c1b37d56de875ead1/6602f31d/video/tos/cn/tos-cn-ve-15/oEf3yTg9bAIY8J73Kn9llqB7kDAD8Avfx5xEOI/?a=1128&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1061&bt=1061&cs=0&ds=6&ft=iusdFLqoQmo0PDXq0xnaQ950U4i6JE.C~&mime_type=video_mp4&qs=0&rc=Zzs7aWRmNTs2aDRmPDc6ZkBpam15OTU6ZnZzcTMzNGkzM0BiMGJhYTZjNWMxYC5eLjY1YSNxcl8zcjRnMW9gLS1kLTBzcw%3D%3D&btag=10e00088000&cc=3e&cquery=100d&dy_q=1711465736&feature_id=f0150a16a324336cda5d6dd0b69ed299&l=202403262308562B9826427C7FD32D3466",
                "origin_title": "#大长腿 #御姐",
                "source": "douyin",
                "tags": [
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
                "thumb": "https://p9-sign.douyinpic.com/tos-cn-p-0015/o8AC8eOFLvs9nRTF9bCBipANgND1A1ZQHleDIY~c5_300x400.webp?x-expires=1712448000&x-signature=H0YbFv%2BODw651QDYRtYlPgmCFlA%3D&from=3213915784_large&s=PackSourceEnum_AWEME_DETAIL&se=false&sc=cover&biz_tag=aweme_video&l=202403240849499FB63B88D58CFCEE60D0",
                "title": "TEst2",
                "url": "https://www.douyin.com/video/7331336529870163235",
            }
        ],
        config={
            "pdsid": "5505f07ffd3f766450a5dc2f5069a949",
            "deploymentId": "d_Wpse57o4",
            "orgId": "o_v1IRzOb",
            "namespace": "upload_video",
            "emitId": "2eBjgVSCmTbY8JGKfoSTGEuv7Fm",
            "emitterId": "hi_eqHm2Oj",
        },
    )
