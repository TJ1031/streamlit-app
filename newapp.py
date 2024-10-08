import streamlit as st
import random

def win_probability(num_trials, switch, num_boxes, num_open, reveal_or_random_choice):
    win_count = 0
    valid_trials = 0  # 有効試行回数（次に座った人が設定1の場合も含む）
    for _ in range(num_trials):
        # 設定1と設定6の台をランダムに配置
        boxes = ["設定1"] * (num_boxes - 1) + ["設定6"]
        random.shuffle(boxes)

        # 自分が最初に選ぶ台
        my_choice = random.randint(0, num_boxes - 1)

        # 残りの設定1の台を探す（店長が知っている）
        orner_choices = [i for i in range(num_boxes) if i != my_choice and boxes[i] == "設定1"]

        # 分岐：設定1の台を開示するか、次に座った人がランダムに選ぶか
        if reveal_or_random_choice == "店長が設定1を開示した場合":
            # 店長は設定1の台を知っているので、確実に設定1を開示
            if len(orner_choices) < num_open:
                return "開示する設定1の台数が多すぎるため、条件を修正してください"
            opened_boxes = random.sample(orner_choices, num_open)
            valid_trials += 1  # 有効試行回数を増やす

        elif reveal_or_random_choice == "次に座った人の台が設定1と判別できた場合":
            # 次に座る人は設定1を知らないので、ランダムに台を選ぶ
            remaining_boxes = [i for i in range(num_boxes) if i != my_choice]

            # 残りの台数が num_open より少ない場合はエラーメッセージを表示
            if len(remaining_boxes) < num_open:
                return "次に座る全員が設定1になるパターンがありません"
            
            #次に座る人たちが選ぶ台を指定された台数分ランダムに選ぶ
            random_choices = random.sample(remaining_boxes, num_open)

            #開示された台の中に設定1があるか確認
            opened_boxes = [i for i in random_choices if boxes[i] == "設定1"]

            # 開示された台が指定された台数分の設定1であるかを確認
            if len(opened_boxes) == num_open:
                valid_trials += 1
            else:
                #設定1に全員座っていない場合は無視
                continue

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

    # 有効な試行があった場合のみ確率を計算
    if valid_trials > 0:
        return f"設定6ツモ確率: {win_count / valid_trials:.2%}"  #（有効試行回数: {valid_trials}回）
    else:
        return "次に座った人が設定1だったパターンがありませんでした。"



st.title("設定6ツモシミュレーター")

# 算出条件の表示
st.markdown("""
### 算出条件
- 設定6が1台入る機種1イベントを想定
- まずは自分が台を選ぶ、6が入る場所は完全ランダムなので適当に座る
- 店長に開示してもらうor次の人の台が1と判明することで自分の台以外から設定1が分かる
- 次に座る人は答えを知らないためランダムに台を選び、その設定が1だった場合開示される
- 店長は答えを知っており、設定1の台を開示してくれる
- 自分以外の台で設定1の場所を知った後に、自分は残りの台に台移動することができる
""")

num_trials = st.number_input("試行回数", value=10000)
num_boxes = st.number_input("設置台数", value=3)
num_open = st.number_input("開示される設定1の台数", value=1)

# 分岐の選択肢を追加（店長が設定1を開示するパターン、次に座る人がランダムに選ぶパターン）
reveal_or_random_choice = st.radio(
    "店長が設定1を開示するか、次に座った人の台が設定1と判別できた場合かを選んでください",
    ("店長が設定1を開示した場合", "次に座った人の台が設定1と判別できた場合")
)

switch = st.checkbox("台移動する")

if st.button("確率を計算する"):
    result = win_probability(num_trials, switch, num_boxes, num_open, reveal_or_random_choice)
    st.write(result)
