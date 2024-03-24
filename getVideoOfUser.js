var getid = async function(sec_user_id, max_cursor) {
    var res = await fetch("https://www.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id="+ sec_user_id +"&max_cursor=" + max_cursor + "&locate_item_id=7321618900121128219&locate_query=false&show_live_replay_strategy=1&need_time_list=1&time_list_query=0&whale_cut_token=&cut_version=1&count=18&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=en-US&browser_platform=Win32&browser_name=Edge&browser_version=122.0.0.0&browser_online=true&engine_name=Blink&engine_version=122.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=8.65&effective_type=4g&round_trip_time=150&webid=7348488984941970982&msToken=8iDxZbV2rIuaOTmbOPaN97i0ixpNnQrtAcaZHQEfldCQPF5YglgecSiLPDTFLPEAYgcQeRv3omcGVmPxYc2HAs1C9_sPcHFZGhgLLUVQV8KVqOHjP-kiHxmet4Bl&X-Bogus=DFSzswVOybsANro1tLev52aNGa60", {
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\", \"Microsoft Edge\";v=\"108\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        },
        "Referer": "https://www.douyin.com/user/"+ sec_user_id,
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "body": null,
        "method": "GET",
    });
    try {
        res = await res.json();
        // if (!res?.aweme_list) {
        //     res = await res.json();
        // }
    } catch (e) {
        // res = await getid(sec_user_id, max_cursor);
        console.log(e);
    }
    return res;
}

var saveToFile = function(text) {
    var blob = new Blob([text], { type: 'text/plain' });
    var a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob);
    a.download = 'douyin-video-links.txt';
    a.click();
}

var run = async function() {
    var result = [];
    var video_id = [];
    var hasMore = 1;
    var sec_user_id = location.pathname.replace("/user/", "");
    var max_cursor = 0;
    while (hasMore == 1) {
        var moredata = await getid(sec_user_id, max_cursor);
        hasMore = moredata['has_more'];
        max_cursor = moredata['max_cursor'];
        for (var i in moredata['aweme_list']) {
            video_id.push(moredata['aweme_list'][i]['aweme_id'])
            if (moredata['aweme_list'][i]['video']['play_addr']['url_list'][0].startsWith("https"))
                result.push(moredata['aweme_list'][i]['video']['play_addr']['url_list'][0]);
            else
                result.push(moredata['aweme_list'][i]['video']['play_addr']['url_list'][0].replace("http", "https"));
            // console.clear();
            console.log("Number of videos: " + result.length);
        }
    }
    saveToFile(video_id.join('\n'));
}
run();