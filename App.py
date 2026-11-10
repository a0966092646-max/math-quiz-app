import streamlit as st
import random
import time
from datetime import datetime
import os

# 網頁標題與設定
st.set_page_config(page_title="數學大挑戰", page_icon="🔢", layout="centered")

st.title("🔢 數學大挑戰 (行動網頁版)")

# 初始化 Session State
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.question_count = 0
    st.session_state.max_questions = 5
    st.session_state.game_mode = "加法挑戰"  # 預設模式
    st.session_state.difficulty = "中等 (1~100)"
    st.session_state.num1 = random.randint(1, 100)
    st.session_state.num2 = random.randint(1, 100)
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.input_counter = 0

# 側邊欄：遊戲設定
st.sidebar.header("⚙️ 遊戲設定")

# 模式選擇
new_mode = st.sidebar.selectbox("選擇遊戲模式", ["加法挑戰", "九九乘法挑戰"], index=0 if st.session_state.game_mode == "加法挑戰" else 1)

# 如果切換模式，重置遊戲
if new_mode != st.session_state.game_mode:
    st.session_state.game_mode = new_mode
    st.session_state.score = 0
    st.session_state.question_count = 0
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.input_counter += 1
    
    if new_mode == "加法挑戰":
        low, high = (1, 10) if "簡單" in st.session_state.difficulty else (1, 100) if "中等" in st.session_state.difficulty else (1, 1000)
        st.session_state.num1 = random.randint(low, high)
        st.session_state.num2 = random.randint(low, high)
    else:
        # 九九乘法範圍固定為 1 ~ 9
        st.session_state.num1 = random.randint(1, 9)
        st.session_state.num2 = random.randint(1, 9)
    st.rerun()

# 難易度選擇（僅在加法模式時顯示）
if st.session_state.game_mode == "加法挑戰":
    new_diff = st.sidebar.selectbox("選擇加法難易度", ["簡單 (1~10)", "中等 (1~100)", "困難 (1~1000)"], index=1)
    if new_diff != st.session_state.difficulty:
        st.session_state.difficulty = new_diff
        st.session_state.score = 0
        st.session_state.question_count = 0
        st.session_state.start_time = time.time()
        st.session_state.game_over = False
        st.session_state.input_counter += 1
        low, high = (1, 10) if "簡單" in new_diff else (1, 100) if "中等" in new_diff else (1, 1000)
        st.session_state.num1 = random.randint(low, high)
        st.session_state.num2 = random.randint(low, high)
        st.rerun()
else:
    st.sidebar.info("💡 九九乘法模式：訓練 1~9 的基礎乘法運算！")

# 遊戲主流程
if not st.session_state.game_over:
    st.markdown(f"### 📍 目前模式：{st.session_state.game_mode} | 第 {st.session_state.question_count + 1} / {st.session_state.max_questions} 題")
    
    # 根據不同模式顯示對應符號
    if st.session_state.game_mode == "加法挑戰":
        st.info(f"請計算： **{st.session_state.num1} + {st.session_state.num2} = ?**")
        operator = "+"
    else:
        st.info(f"請計算： **{st.session_state.num1} × {st.session_state.num2} = ?**")
        operator = "×"
    
    current_input_key = f"quiz_input_{st.session_state.input_counter}"
    
    with st.form(key="quiz_form"):
        user_input = st.text_input("請輸入您的答案：", key=current_input_key, placeholder="請輸入數字...", autocomplete="off")
        submit_button = st.form_submit_button(label="提交答案", type="primary")
        
        if submit_button:
            if user_input.strip().isdigit():
                ans = int(user_input.strip())
                
                # 計算正確答案
                if operator == "+":
                    correct = st.session_state.num1 + st.session_state.num2
                else:
                    correct = st.session_state.num1 * st.session_state.num2
                
                if ans == correct:
                    st.success("🎉 答對了！")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ 答錯囉！正確答案是 {correct}")
                
                st.session_state.question_count += 1
                st.session_state.input_counter += 1  # 換題時更新 key 清空欄位
                
                if st.session_state.question_count < st.session_state.max_questions:
                    if st.session_state.game_mode == "加法挑戰":
                        low, high = (1, 10) if "簡單" in st.session_state.difficulty else (1, 100) if "中等" in st.session_state.difficulty else (1, 1000)
                        st.session_state.num1 = random.randint(low, high)
                        st.session_state.num2 = random.randint(low, high)
                    else:
                        st.session_state.num1 = random.randint(1, 9)
                        st.session_state.num2 = random.randint(1, 9)
                    time.sleep(0.8)
                    st.rerun()
                else:
                    st.session_state.game_over = True
                    # 遊戲結束，寫入排行榜
                    elapsed = time.time() - st.session_state.start_time
                    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    record_line = f"[{now_str}] 模式: {st.session_state.game_mode} | 得分: {st.session_state.score}/{st.session_state.max_questions} | 用時: {elapsed:.2f}秒\n"
                    with open("math_leaderboard.txt", "a", encoding="utf-8") as f:
                        f.write(record_line)
                    time.sleep(0.8)
                    st.rerun()
            else:
                st.warning("⚠️ 請輸入有效的整數數字！")

else:
    # 結算畫面
    elapsed = time.time() - st.session_state.start_time
    st.balloons()
    st.success("🏆 恭喜完成所有挑戰！")
    st.metric(label="您的總得分", value=f"{st.session_state.score} / {st.session_state.max_questions}")
    st.metric(label="總花費時間", value=f"{elapsed:.2f} 秒")
    
    if st.button("🔄 再玩一次"):
        st.session_state.score = 0
        st.session_state.question_count = 0
        st.session_state.start_time = time.time()
        st.session_state.game_over = False
        st.session_state.input_counter += 1
        st.rerun()

# 顯示排行榜
st.sidebar.markdown("---")
st.sidebar.subheader("📜 歷史排行榜")
if os.path.exists("math_leaderboard.txt"):
    with open("math_leaderboard.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in reversed(lines[-5:]):
            st.sidebar.text(line.strip())
else:
    st.sidebar.text("尚無紀錄")
