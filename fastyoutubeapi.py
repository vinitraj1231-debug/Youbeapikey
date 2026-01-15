from fastapi import FastAPI, Query, HTTPException
import yt_dlp

app = FastAPI()

YDL_OPTS_SEARCH = {
    "quiet": True,
    "skip_download": True,
    "extract_flat": True,
    "nocheckcertificate": True,
    "geo_bypass": True,
    "user_agent": (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0 Mobile Safari/537.36"
    ),
    "extractor_args": {
        "youtube": {
            "player_client": ["android"],
            "player_skip": ["webpage"]
        }
    }
}

YDL_OPTS_FULL = {
    "quiet": True,
    "skip_download": True,
    "nocheckcertificate": True,
    "geo_bypass": True,
    "user_agent": YDL_OPTS_SEARCH["user_agent"],
    "extractor_args": YDL_OPTS_SEARCH["extractor_args"]
}


@app.get("/search")
async def search_youtube(title: str = Query(...)):
    try:
        # Step 1: Search
        with yt_dlp.YoutubeDL(YDL_OPTS_SEARCH) as ydl:
            search = ydl.extract_info(f"ytsearch1:{title}", download=False)
            entry = search["entries"][0]

        # Step 2: Full metadata
        with yt_dlp.YoutubeDL(YDL_OPTS_FULL) as ydl:
            info = ydl.extract_info(entry["url"], download=False)

        return {
            "playlist": False,
            "title": info.get("title"),
            "link": info.get("webpage_url"),
            "duration": info.get("duration"),
            "thumbnail": info.get("thumbnail")
        }

    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"YouTube extraction failed: {str(e)}"
)
