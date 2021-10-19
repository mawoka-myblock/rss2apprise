# Rss2Apprise

A short script designed to run on [Deta Micros](https://deta.sh) to monitor an RSS-Feed
and notify you if it changes over one of [Apprise](https://github.com/caronc/apprise)'s
many possibilities.

# Setup

Push the following button:

[![Deploy](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy?repo=your-repo-url)

And add a cron by running `deta cron set "0/30 * * * ? *"`
