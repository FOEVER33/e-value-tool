from flask import Flask, render_template_string, request

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>竞彩E值推荐工具</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        input, button { padding: 8px; margin: 5px; }
        .result { margin-top: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <h2>竞彩E值推荐工具（输入排名与赔率）</h2>
    <form method="post">
        主队排名: <input type="number" name="home_rank" required>
        客队排名: <input type="number" name="away_rank" required><br>
        最低赔率: <input type="number" step="0.01" name="min_odds" required><br>
        <button type="submit">计算E值并给出建议</button>
    </form>
    {% if result %}
    <div class="result">
        计算结果：<br>
        排名差 = {{ rank_diff }}<br>
        E值 = {{ e_value }}<br>
        策略建议：{{ strategy }}
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    rank_diff = e_value = strategy = None
    if request.method == "POST":
        home_rank = int(request.form["home_rank"])
        away_rank = int(request.form["away_rank"])
        min_odds = float(request.form["min_odds"])
        rank_diff = home_rank - away_rank
        e_value = round((0.45 + 0.0053 * rank_diff) * min_odds, 3)
        if e_value >= 1.0:
            strategy = "✅ 正期望，可下注"
        elif e_value >= 0.93:
            strategy = "❌ 放弃此场"
        else:
            strategy = "🔄 反向投注（选对面）"
        result = True
    return render_template_string(html, result=result, rank_diff=rank_diff,
                                  e_value=e_value, strategy=strategy)

if __name__ == "__main__":
    app.run()