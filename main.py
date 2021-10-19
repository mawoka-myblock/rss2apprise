import apprise as AppRise
from apprise import NotifyFormat
import feedparser
import markdownify
from deta import Deta
from os import getenv
import hashlib
import requests
from deta import app


class config:
    rss_url = getenv("RSS_URL")
    deta_project_key = getenv("DETA_PROJECT_KEY")
    apprise_uris = getenv("APPRISE_URI").split(",")


@app.lib.cron()
def cron_job(event):
    deta = Deta(config.deta_project_key)
    base = deta.Base("rss2apprise")
    r = requests.get(config.rss_url)
    old_hash = base.get("hash")["value"]
    hash_feed = hashlib.sha512(str(r.text).encode("utf-8")).hexdigest()
    if old_hash != hash_feed:
        base.put(hash_feed, "hash")
        d = feedparser.parse(r.text)
        apprise = AppRise.Apprise()
        apprise.add(config.apprise_uris)
        apprise.notify(title=f"New Entry: {d.entries[0].title}", body_format=NotifyFormat.MARKDOWN, body=f"""
# Details
- Title: {d.entries[0].title}
- Published at: {d.entries[0].published}
- Link: [{d.entries[0].link}]({d.entries[0].link})
# Description:
{markdownify.markdownify(d.entries[0].description)}
                """)
        return "Feed Changed!"

    else:
        return "Feed didn't change!"
