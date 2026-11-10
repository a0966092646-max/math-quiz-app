import streamlit as st
import random
import time
from datetime import datetime
import os

# 網頁標題與設定
st.set_page_config(page_title="數學加法大挑戰", page_icon="➕", layout="centered")

st.title("➕ 數學加法大挑戰 (行動網頁版)")

# 初始化 Session State
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.question_count = 0
    st.session_state.max_questions = 5
    st.session_state.difficulty = "中等"
    st.session_state.num1 = random.randint(1, 100)
    st.session_state.num2 = random.randint(1, 100)
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.input_counter = 0

# 側邊欄：難易度選擇
st.sidebar.header("⚙️ 遊戲設定")
new_diff = st.sidebar.selectbox("選擇難易度", ["簡單 (1~10)", "中等 (1~100)", "困難 (1~1000)"], index=1)

# 如果切換難易度，重置遊戲
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

# 遊戲主流程
if not st.session_state.game_over:
    st.markdown(f"### 📍 目前進度：第 {st.session_state.question_count + 1} / {st.session_state.max_questions} 題")
    
    # 顯示題目
    st.info(f"請計算： **{st.session_state.num1} + {st.session_state.num2} = ?**")
    
    current_input_key = f"quiz_input_{st.session_state.input_counter}"
    
    with st.form(key="quiz_form"):
        user_input = st.text_input("請輸入您的答案：", key=current_input_key, placeholder="輸入數字後按 Enter 送出...")
        submit_button = st.form_submit_button(label="提交答案", type="primary")
        
        if submit_button:
            if user_input.strip().isdigit():
                ans = int(user_input.strip())
                correct = st.session_state.num1 + st.session_state.num2
                
                if ans == correct:
                    st.success("🎉 答對了！")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ 答錯囉！正確答案是 {correct}")
                
                st.session_state.question_count += 1
                st.session_state.input_counter += 1  # 換題時更新 key 確保內容清空
                
                if st.session_state.question_count < st.session_state.max_questions:
                    low, high = (1, 10) if "簡單" in st.session_state.difficulty else (1, 100) if "中等" in st.session_state.difficulty else (1, 1000)
                    st.session_state.num1 = random.randint(low, high)
                    st.session_state.num2 = random.randint(low, high)
                    time.sleep(0.8)
                    st.rerun()
                else:
                    st.session_state.game_over = True
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
