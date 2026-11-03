# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse
# from openai import OpenAI

# app = FastAPI()

# @app.get("/", response_class=HTMLResponse)
# def instant():
#     client = OpenAI()
#     message = """
# You are on a website that has just been deployed to production for the first time!
# Please reply with an enthusiastic announcement to welcome visitors to the site, explaining that it is live on production for the first time!
# """
#     messages = [{"role": "user", "content": message}]
#     response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
#     reply = response.choices[0].message.content.replace("\n", "<br/>")
#     html = f"<html><head><title>Live in an Instant!</title></head><body><p>{reply}</p></body></html>"
#     return html

import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def instant():
    try:
        from google import genai

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return HTMLResponse(
                "<h3>Configuration Error: GEMINI_API_KEY is missing in Vercel Environment Variables.</h3>",
                status_code=500
            )

        client = genai.Client(api_key=api_key)

        message = """
        You are on a website that has just been deployed to production for the first time!
        Please reply with an enthusiastic announcement to welcome visitors to the site!
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=message,
        )

        reply = response.text.replace("\n", "<br/>")
        return f"<html><head><title>Live in an Instant!</title></head><body><p>{reply}</p></body></html>"

    except Exception as e:
        return HTMLResponse(content=f"<h3>Runtime Error: {str(e)}</h3>", status_code=500)