import streamlit as st
import random

def win_probability(num_trials, switch, num_boxes, num_open):
    win_count = 0
    for _ in range(num_trials):
        boxes = ["設定1"] * (num_boxes - 1) + ["設定6"]
        random.shuffle(boxes)
        my_choice = random.randint(0, num_boxes - 1)
        orner_choices = [i for i in range(num_boxes) if i != my_choice and boxes[i] == "設定1"]
        if len(orner_choices) < num_open:
            return "開示する設定1の台数が多すぎるため、条件を修正してください"
        opened_boxes = random.sample(orner_choices, num_open)
        if switch:
            remaining_boxes = [i for i in range(num_boxes) if i != my_choice and i not in opened_boxes]
            if remaining_boxes:
                my_choice = random.choice(remaining_boxes)
            else:
                return "移動先の台が存在しません"
        if boxes[my_choice] == "設定6":
            win_count += 1
    return f"確率: {win_count / num_trials:.2%}"

st.title("設定6ツモシミュレーター")
num_trials = st.number_input("試行回数", value=10000)
num_boxes = st.number_input("設置台数", value=3)
num_open = st.number_input("開示される設定1の台数", value=1)
switch = st.checkbox("台移動する")

if st.button("確率を計算する"):
    result = win_probability(num_trials, switch, num_boxes, num_open)
    st.write(result)