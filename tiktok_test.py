from tiktok_uploader import tiktok
import requests, time, logging, colorlog

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
if __name__ == "__main__":
    tiktok.login("quangver02_1")
    # tiktok.upload_video(
    #     "test01",
    #     "https://v11-o.douyinvod.com/a860538503855813fb8b8ed59ce32a44/6601ae3a/video/tos/cn/tos-cn-ve-15/oUDQPANhGgDAyKoDZEBjerA1BPI9fnAJzHRgbU/?a=1128&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1157&bt=1157&cs=0&ds=6&ft=iusdFLqoQmo0PDUwpxnaQ950U4i6JE.C~&mime_type=video_mp4&qs=0&rc=Ozk7N2Y1NzU4OzxoPDw5OkBpM2l4bTo6Zjg0ajMzNGkzM0A2YWA2YC41Xi8xYzIyMzYxYSNoanBgcjQwMGJgLS1kLTBzcw%3D%3D&btag=10e00088000&cc=3e&cquery=100d&dy_q=1711382562&feature_id=59cb2766d89ae6284516c6a254e9fb61&l=20240326000242A39BF00849070F25BC50",
    #     "test",
    #     0,
    #     1,
    #     1,
    #     1,
    #     0,
    #     0,
    #     0,
    #     0,
    #     None,
    # )
