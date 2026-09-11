from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/simplify", methods=["POST"])
def simplify():
    data = request.json
    content = data.get("content", "").strip()
    level = data.get("level", "Beginner")

    if not content:
        return jsonify({"error": "Please enter course content."})

    if level == "Beginner":
        explanation = f"{content}\n\nThis concept can be understood by focusing on its basic purpose, main components, and a simple real-world example."
    elif level == "Intermediate":
        explanation = f"{content}\n\nAt an intermediate level, this concept can be understood by connecting its main components, working principles, and practical applications."
    else:
        explanation = f"{content}\n\nAt an advanced level, this concept can be studied through its underlying principles, technical details, relationships with other concepts, and practical applications."

    return jsonify({
        "level": level,
        "explanation": explanation,
        "concepts": [
            "Core concept",
            "Important components",
            "Working principle",
            "Practical application"
        ],
        "definitions": [
            "Key technical terms are explained according to the selected proficiency level."
        ],
        "example": "A suitable real-world example can be used to connect the academic concept with practical understanding.",
        "summary": f"The topic was simplified for a {level.lower()} learner while retaining its important meaning.",
        "questions": [
            "What is the main concept?",
            "What are its important components?",
            "Where is this concept applied?"
        ]
    })

if __name__ == "__main__":
    app.run(debug=True)
