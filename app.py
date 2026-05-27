import anthropic
from flask import Flask, render_template, request, stream_with_context, Response

app = Flask(__name__)
client = anthropic.Anthropic()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    mood = request.form.get("mood", "")
    location = request.form.get("location", "")
    energy = request.form.get("energy", "")

    prompt = f"""You are a fun, direct activity recommender. No fluff.

The user is in {location} and feeling {mood}. Their energy level is {energy}.

Give them exactly 3 activity options for tonight. For each one:
- Name it
- One sentence why it fits their mood
- What they need to do right now to make it happen

End with a clear RECOMMENDED PICK and one sentence why.

Be specific. No generic advice like "go for a walk." Give them something they'll actually do."""

    def generate():
        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                yield text

    return Response(stream_with_context(generate()), mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True)
