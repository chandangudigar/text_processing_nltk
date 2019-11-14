from flask import Flask, request, render_template
import jinja2
import nltk
from nltk.corpus import stopwords
import language_check
from bs4 import BeautifulSoup
import os
import textdistance


jinja2.exceptions.TemplateNotFound


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def hello():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.form:
            uname = request.form.get("username")
            password = request.form.get("password")
            if uname == "student" and password == "student":
                return render_template("home.html", user=uname)

            else:
                return render_template(
                    "index.html", user="invalid username or Password"
                )


@app.route("/execute", methods=["POST", "GET"])
def execute():
    if request.method == "POST":
        if request.form:
            answer = "Cloud computing allows consumers and businesses to use applications without installation and access their personal files at any computer with internet access. Cloud-based services are ideal for businesses with growing or fluctuating bandwidth demands."
            text = request.form.get("text")
            tool = language_check.LanguageTool("en-US")
            matches = tool.check(text)
            language_check.correct(text, matches)
            mark = 0
            if len(matches) == 0:
                mark = mark + 5
            elif len(matches) > 5:
                mark = mark + 4
            elif len(matches) > 10:
                mark = mark + 3

            # Context based comparison

            

            allWords = nltk.tokenize.word_tokenize(text)
            stopwords = nltk.corpus.stopwords.words("english")
            words = []
            point = [",", ".", ";", "'", ""]
            for w in allWords:
                if w not in stopwords:
                    if w not in point:
                        words.append(w)
            allWordDist = nltk.FreqDist(w.lower() for w in words)

            allWordExceptStopDist = nltk.FreqDist(
                w.lower() for w in allWordDist if w not in stopwords
            )

            mostCommon = allWordDist.most_common()

            allWord = nltk.tokenize.word_tokenize(answer)
            stopwords = nltk.corpus.stopwords.words("english")
            word = []
            point = [",", ".", ";", "'", "-"]
            for w in allWord:
                if w not in allWordDist:
                    if w not in point:
                        word.append(w)
            mark1 = 0
            length = len(allWord)
            if length > 15:
                for a in allWord:
                    for r in allWordDist:
                        dist1 = float(textdistance.jaro_winkler(a, r))
                        dist = round(dist1, 2)
                        if dist > 0.500:
                            mark1 = mark1 + 1
                            break
                marks2 = int(mark1 / length * 5)
                total = mark + marks2
            else:
                total = 0
    return render_template("result.html", total=total)


if __name__ == "__main__":
    app.run(debug=True)

