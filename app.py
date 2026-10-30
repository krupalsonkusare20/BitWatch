"""BitWatch backend (Flask).

Run:  python app.py        (serves http://localhost:5000)

GET  /api/content  -> lessons, videos, notes links
POST /api/check    -> {method, data, flipped:[indexes]} -> simulation result
"""
import re

from flask import Flask, jsonify, request

from codec import encode, evaluate
from content import COLORS, HAND_LINKS, HL, KEYS, M, NOTE_LINKS

app = Flask(__name__)


@app.get("/api/content")
def get_content():
    return jsonify(
        order=KEYS,
        methods=M,
        colors=COLORS,
        noteLinks=NOTE_LINKS,
        handLinks=HAND_LINKS,
    )


@app.post("/api/check")
def check():
    body = request.get_json(silent=True) or {}
    method = body.get("method")
    data = str(body.get("data", ""))
    flipped = body.get("flipped", [])

    if method not in M:
        return jsonify(error="Unknown method."), 400
    length = M[method]["length"]
    if len(data) != length or not re.fullmatch(r"[01]+", data):
        return jsonify(error=f"Enter exactly {length} bits using only 0 and 1."), 400

    frame_len = len(encode(method, [int(c) for c in data]))
    if not isinstance(flipped, list) or not all(
        isinstance(i, int) and 0 <= i < frame_len for i in flipped
    ):
        return jsonify(error="Bad flipped bit index."), 400

    received, frame, verdict, good = evaluate(method, data, set(flipped))
    is_check = [
        (not ((i + 1) & i)) if method == "hamming" else i >= length
        for i in range(frame_len)
    ]
    return jsonify(
        frame=frame,
        received=received,
        isCheck=is_check,
        labels=HL if method == "hamming" else [str(i + 1) for i in range(frame_len)],
        verdict=verdict,
        good=good,
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
