import gradio as gr

# E值计算逻辑
def calculate_e_value(rank_home, rank_away, odds_win, odds_draw, odds_lose):
    try:
        rank_diff = rank_home - rank_away
        prob_win = 0.45 + 0.0053 * rank_diff
        min_odds = min(odds_win, odds_draw, odds_lose)
        e_value = round(prob_win * min_odds, 3)

        if e_value >= 1:
            suggestion = "✅ 投注该方向"
            color = "#d4edda"
        elif e_value >= 0.93:
            suggestion = "⚠️ 放弃该场"
            color = "#fff3cd"
        else:
            suggestion = "🔄 反向投注（选对面）"
            color = "#f8d7da"

        return rank_diff, e_value, suggestion, color
    except:
        return 0, 0.0, "输入有误", "#f8d7da"

# 历史记录
history = []

def batch_process(data):
    results = []
    for row in data:
        if any(x is None for x in row) or len(row) != 5:
            continue
        r1, r2, o1, o2, o3 = row
        diff, ev, sug, color = calculate_e_value(r1, r2, o1, o2, o3)
        results.append([r1, r2, o1, o2, o3, diff, ev, sug])
        history.append([r1, r2, o1, o2, o3, diff, ev, sug])
    return results

def get_history():
    return history[::-1][:20]  # 最近20条

with gr.Blocks(css=".gr-table td {text-align: center}") as demo:
    gr.Markdown("""
    # ⚽ 竞彩 E 值投注推荐工具（多场批量版）
    输入多场比赛数据，获取每场投注建议（带颜色提示）
    - 支持手机适配
    - 输入：主队排名、客队排名、胜、平、负三项赔率
    """)

    with gr.Row():
        input_table = gr.Dataframe(
            headers=["主队排名", "客队排名", "胜赔率", "平赔率", "负赔率"],
            datatype=["number", "number", "number", "number", "number"],
            row_count=5,
            col_count=(5, "fixed"),
            interactive=True,
            label="输入比赛数据（可增加行）"
        )

    btn = gr.Button("计算投注建议")

    output_table = gr.Dataframe(
        headers=["主队排名", "客队排名", "胜赔率", "平赔率", "负赔率", "排名差", "E值", "建议"],
        label="计算结果（带建议）",
        interactive=False
    )

    history_btn = gr.Button("查看最近历史记录（最多20条）")
    history_output = gr.Dataframe(
        headers=["主队排名", "客队排名", "胜赔率", "平赔率", "负赔率", "排名差", "E值", "建议"],
        label="历史记录",
        interactive=False
    )

    btn.click(fn=batch_process, inputs=input_table, outputs=output_table)
    history_btn.click(fn=get_history, outputs=history_output)

# 启动
if __name__ == "__main__":
    demo.launch()