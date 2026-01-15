from fastapi import FastAPI, Query
import yt_dlp

app = FastAPI()

@app.get("/search")
async def search_youtube(title: str = Query(...)):

    search_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True
    }

    with yt_dlp.YoutubeDL(search_opts) as ydl:
        search = ydl.extract_info(f"ytsearch1:{title}", download=False)
        entry = search["entries"][0]

    # अब full info extract करो
    video_opts = {
        "quiet": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(video_opts) as ydl:
        info = ydl.extract_info(entry["url"], download=False)

    return {
        "playlist": False,
        "title": info.get("title"),
        "link": info.get("webpage_url"),
        "duration": info.get("duration"),
        "thumbnail": info.get("thumbnail")
    }
