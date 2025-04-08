from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

# --- 入力データ ---
name = "Akashi Tohma"
attendance_option = "勤務終了(End of work)"
task_description = "本日の業務：○○データの整理・分析、および報告資料の作成"
note = ""

# --- Edgeドライバ起動 ---
options = webdriver.EdgeOptions()
# options.add_argument("--headless")  # 非表示で実行したいときに有効化

driver = webdriver.Edge(
    service=Service(EdgeChromiumDriverManager().install()),
    options=options
)

driver.get("https://forms.office.com/Pages/ResponsePage.aspx?id=s-vy4xAIWUmOBWzs2MAP8pBcJeApFIhNgiKUedRi32NUNTZMMlJCUllCODRTTjlOOEs1V1NWM0FCVS4u")
wait = WebDriverWait(driver, 15)

# --- 入力欄の取得と入力 ---
text_inputs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[data-automation-id="textInput"]')))
text_inputs[0].send_keys(name)
text_inputs[1].send_keys(task_description)
text_inputs[2].send_keys(note)

# --- 勤怠管理（JSで確実にクリック）---
choice_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-automation-id="choiceItem"]')))
selected = False
for item in choice_items:
    try:
        label = item.find_element(By.TAG_NAME, "label")
        if attendance_option in label.text.strip():
            driver.execute_script("arguments[0].click();", label)
            time.sleep(0.5)
            selected = True
            break
    except Exception as e:
        continue

# --- 選択できているか確認 ---
if not selected:
    print("⚠️ 勤怠管理の選択に失敗しました。スクリプトを終了します。")
    driver.quit()
    exit()

# --- 送信ボタン押下 ---
try:
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-automation-id="submitButton"]')))
    submit_button.click()
except Exception as e:
    print("⚠️ 送信ボタンが押せませんでした:", e)
    driver.quit()
    exit()

# --- 成功画面を検出して送信確認 ---
try:
    confirmation_text = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="heading"]')))
    print("✅ フォーム送信に成功しました！")
    print("📤 送信内容:")
    print(f"・氏名: {name}")
    print(f"・勤怠管理: {attendance_option}")
    print(f"・業務内容: {task_description}")
    print(f"・備考: {note if note else '（空欄）'}")
except Exception:
    print("⚠️ 送信後の確認画面が検出できませんでした。手動で確認をお願いします。")

time.sleep(2)
driver.quit()
