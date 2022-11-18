from telegram import Update, Bot
import os
from dotenv import load_dotenv
import xmltodict
from xml.parsers.expat import ExpatError
load_dotenv()
TelegramBotToken = os.environ['TGTOKEN']
bot = Bot(token=TelegramBotToken)

tg_target = os.environ["target_tg_channel"]
yt_accept = os.environ.get("accept_yt_channel", "").split(",")

def channel_noti(request):
    """Accept and parse requests from YT's pubsubhubbub.
    https://developers.google.com/youtube/v3/guides/push_notifications
    """

    challenge = request.args.get("hub.challenge")
    if challenge:
        # YT will send a challenge from time to time to confirm the server is alive.
        return challenge
    if request.method == "POST":
        try:
            # Parse the XML from the POST request into a dict.
            xml_dict = xmltodict.parse(request.data)
            print(xml_dict)
            # Lazy verification - check if the POST request is from a channel ID that's been
            # set in config["channel_ids"].  Skip the check if that config option is empty.
            channel_id = xml_dict["feed"]["entry"]["yt:channelId"]
            if yt_accept != [] and channel_id not in yt_accept:
                return "", 403

            # Parse out the video URL.
            video_url = xml_dict["feed"]["entry"]["link"]["@href"]
            
            message = f"宣傳部表示又有新片出啦！\n{video_url}"
            bot.send_message(text=message, chat_id=tg_target)

        except (ExpatError, LookupError):
            # request.data contains malformed XML or no XML at all, return FORBIDDEN.
            return "", 403

        # Everything is good, return NO CONTENT.
        return "", 204

