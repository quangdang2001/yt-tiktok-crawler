import requests


def pinedream_payload(event):
    return {
        "operationName": "executeTestRequest",
        "query": "mutation executeTestRequest($ancestorIds: [String!], $childIds: [String!], $deploymentId: String!, $endNamespace: String, $endPhase: StepPhaseEnum, $lambdaMakerSuffix: String, $orgId: String, $sourceEmit: EmitInput, $startNamespace: String, $startPhase: StepPhaseEnum, $traceId: String, $triggerOnly: Boolean, $useLabyrinth: Boolean) {  my(orgId: $orgId) {    executeTestRequest(      ancestorIds: $ancestorIds      childIds: $childIds      deploymentId: $deploymentId      endStepNamespace: $endNamespace      endStepPhase: $endPhase      executionTraceId: $traceId      lambdaMakerSuffix: $lambdaMakerSuffix      sourceEmit: $sourceEmit      startStepNamespace: $startNamespace      startStepPhase: $startPhase      triggerOnly: $triggerOnly      useLabyrinth: $useLabyrinth    ) {      errors      executionTraceId      stepErrors {        namespace        error        __typename      }      __typename    }    __typename  }}",
        "variables": {
            "deploymentId": "d_MOsy4RMW",
            "endNamespace": "upload_video_1",
            "orgId": "o_v1IRzOb",
            "sourceEmit": {
                "event": event,
                "indexId": "1711241425886-0",
                "indexedAtMs": 1711241425886,
                "metadata": {
                    "emitId": "2e72ir7NFXcON0wFScwxUBOF5aj",
                    "emitterId": "hi_eqHm2Oj",
                    "name": "",
                    "summary": "GET /",
                },
            },
            "startNamespace": "upload_video",
        },
    }


def youtubeUploader(event):
    url = "https://api.pipedream.com/graphql"
    header = {
        "Content-Type": "application/json",
        "cookie": "pdsid=ba7b93f08891f801761d9c7de3b82233",
    }
    payload = pinedream_payload(event)
    resp = requests.post(url=url, json=payload, headers=header)
    if resp.status_code == 200:
        print("Upload success", event[0]["title"])
    else:
        print("Upload failed", resp.status_code, resp.content)
    return resp


if __name__ == "__main__":
    youtubeUploader(
        [
            {
                "des": "Kênh chuyên về tiktok, douyin gái xink Trung Quốc. #douyin #chinesegirl #hotgirls #beautifulgirls #cutegirls #beautifulchinesegirls #bodygoals #fashionstyle #model #dance #beauty #cosplay #sexylegs #asianbeauty #streetfashion #chinesebeauty #tiktok",
                "link_download": "https://v5-dy-o-abtest.zjcdn.com/840823b79512b2458724e4b3fb6fe2cf/65ff86c5/video/tos/cn/tos-cn-v-0015c005-alinc2/oEiACvAFseOYABNADlNF9LgALDIUbAHnIeIsaZ/?a=1128&ch=0&cr=0&dr=0&cd=0%7C0%7C0%7C0&cv=1&br=21854&bt=21854&cs=0&ds=4&ft=iusdFLqoQmo0PDmxXcUaQ950U4i6JE.C~&mime_type=video_mp4&qs=13&rc=MzY5Mzk6Zms1cDMzNGkzM0BpMzY5Mzk6Zms1cDMzNGkzM0BqYjVvcjRfMnNgLS1kLWFzYSNqYjVvcjRfMnNgLS1kLWFzcw%3D%3D&btag=10e00048000&cc=46&cquery=100y&dy_q=1711241390&l=202403240849507CE5B8A24050C9026D7D",
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
                "title": "Những clip triệu view gái xinh hot tiktok Trung Hoa #douyin #beautiful #603",
                "url": "https://www.douyin.com/video/7331336529870163235",
            }
        ]
    )
