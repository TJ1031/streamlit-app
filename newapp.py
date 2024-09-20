import streamlit as st
import random

def win_probability(num_trials, switch, num_boxes, num_open, reveal_or_random_choice):
    win_count = 0
    for _ in range(num_trials):
        # 設定1と設定6の台をランダムに配置
        boxes = ["設定1"] * (num_boxes - 1) + ["設定6"]
        random.shuffle(boxes)

        # 自分が最初に選ぶ台
        my_choice = random.randint(0, num_boxes - 1)

        # 残りの設定1の台を探す（店長が知っている）
        orner_choices = [i for i in range(num_boxes) if i != my_choice and boxes[i] == "設定1"]

        # 分岐：設定1の台を開示するか、次に座った人がランダムに選ぶか
        if reveal_or_random_choice == "店長が設定1を開示":
            # 店長は設定1の台を知っているので、確実に設定1を開示
            if len(orner_choices) < num_open:
                return "開示する設定1の台数が多すぎるため、条件を修正してください"
            opened_boxes = random.sample(orner_choices, num_open)

        elif reveal_or_random_choice == "次に座る人がランダムに選ぶ":
            # 次に座る人は設定1を知らないので、ランダムに台を選ぶ
            remaining_boxes = [i for i in range(num_boxes) if i != my_choice]
            random_choice = random.choice(remaining_boxes)  # 次に座る人がランダムに台を選ぶ

            # 次に座った台が設定1なら、その台を開示する
            if boxes[random_choice] == "設定1":
                opened_boxes = [random_choice]
            else:
                opened_boxes = []

        # 台移動するかどうか
        if switch:
            # 自分が最初に選んだ台と開示された台以外の台に移動
            remaining_boxes = [i for i in range(num_boxes) if i != my_choice and i not in opened_boxes]
            if remaining_boxes:
                my_choice = random.choice(remaining_boxes)
            else:
                return "移動先の台が存在しません"

        # 最終的に選んだ台が設定6かどうかを確認
        if boxes[my_choice] == "設定6":
            win_count += 1

    return f"設定6ツモ確率: {win_count / num_trials:.2%}"

st.title("設定6ツモシミュレーター")

# 算出条件の表示
st.markdown("""
### 算出条件
- 設定6が1台入る機種1イベントを想定
- 6が入る場所は完全ランダムなので適当に座る
- 店長は答えを知っており、設定1の台を開示してくれる
- 次に座る人は設定1の台を知らないため、ランダムに台を選ぶ
- 次に座った人が設定1だった場合、その台が開示される
""")

num_trials = st.number_input("試行回数", value=10000)
num_boxes = st.number_input("設置台数", value=3)
num_open = st.number_input("開示される設定1の台数", value=1)

# 分岐の選択肢を追加（店長が設定1を開示するパターン、次に座る人がランダムに選ぶパターン）
reveal_or_random_choice = st.radio(
    "店長が設定1を開示するか、次に座った人の台が設定1と判別できた場合かを選んでください",
    ("店長が設定1を開示", "次に座った人の台が設定1と判別できた")
)

switch = st.checkbox("台移動する")

if st.button("確率を計算する"):
    result = win_probability(num_trials, switch, num_boxes, num_open, reveal_or_random_choice)
    st.write(result)
