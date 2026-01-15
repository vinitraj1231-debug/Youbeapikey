from fastapi import FastAPI, Query, HTTPException
import aiohttp
import re
import json

app = FastAPI(title="Cloud Safe YouTube Search API")

YOUTUBE_SEARCH_URL = "https://www.youtube.com/results?search_query="

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9"
}


def extract_json(html: str):
    match = re.search(r"var ytInitialData = (.*?);</script>", html)
    if not match:
        return None
    return json.loads(match.group(1))


@app.get("/search")
async def search(title: str = Query(...)):
    try:
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.get(YOUTUBE_SEARCH_URL + title) as resp:
                html = await resp.text()

        data = extract_json(html)
        if not data:
            raise Exception("ytInitialData not found")

        contents = (
            data["contents"]["twoColumnSearchResultsRenderer"]
            ["primaryContents"]["sectionListRenderer"]["contents"][0]
            ["itemSectionRenderer"]["contents"]
        )

        for item in contents:
            if "videoRenderer" in item:
                v = item["videoRenderer"]
                video_id = v["videoId"]

                return {
                    "playlist": False,
                    "title": "".join(r["text"] for r in v["title"]["runs"]),
                    "link": f"https://www.youtube.com/watch?v={video_id}",
                    "duration": v["lengthText"]["simpleText"],
                    "thumbnail": v["thumbnail"]["thumbnails"][-1]["url"]
                }

        raise Exception("No video found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
