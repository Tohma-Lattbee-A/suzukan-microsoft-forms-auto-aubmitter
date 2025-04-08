from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import argparse
import time

# --- 引数で勤務開始 or 終了を指定 ---
parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["start", "end"], required=True)
args = parser.parse_args()

# --- 勤怠種別をモードに応じて設定 ---
attendance_option = "勤務開始(Start of work)" if args.mode == "start" else "勤務終了(End of work)"

# --- 3名分の情報（業務は end のときのみ使用）---
users = [
    {"name": "明石到真", "task": "資料整理／作成、データ分析"},
    {"name": "下山佳南", "task": "資料整理／作成、データ分析"},
    {"name": "野宮勇介", "task": "資料整理／作成、データ分析"}
]

# --- フォームURL（共通） ---
form_url = "https://forms.office.com/Pages/ResponsePage.aspx?id=s-vy4xAIWUmOBWzs2MAP8pBcJeApFIhNgiKUedRi32NUNTZMMlJCUllCODRTTjlOOEs1V1NWM0FCVS4u"

def submit_form(name, task_description, attendance_option, note=""):
    print(f"\n--- {name} さんの送信を開始します ---")

    # --- Edgeドライバ起動（headless可能） ---
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Edge(
        service=Service(EdgeChromiumDriverManager().install()),
        options=options
    )

    driver.get(form_url)
    wait = WebDriverWait(driver, 15)

    try:
        # --- 入力欄（氏名、業務、備考） ---
        text_inputs = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'input[data-automation-id="textInput"]')))
        text_inputs[0].send_keys(name)
        text_inputs[1].send_keys(task_description)
        text_inputs[2].send_keys(note)

        # --- 勤怠選択肢（JSクリック） ---
        choice_items = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'div[data-automation-id="choiceItem"]')))
        selected = False
        for item in choice_items:
            try:
                label = item.find_element(By.TAG_NAME, "label")
                if attendance_option in label.text.strip():
                    driver.execute_script("arguments[0].click();", label)
                    time.sleep(0.5)
                    selected = True
                    break
            except Exception:
                continue

        if not selected:
            print(f"⚠️ {name}: 勤怠管理の選択に失敗しました。")
            driver.quit()
            return

        # --- 送信 ---
        submit_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[data-automation-id="submitButton"]')))
        submit_button.click()

        # --- 成功確認 ---
        confirmation_text = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="heading"]')))
        print("✅ フォーム送信に成功しました！")
        print("📤 送信内容:")
        print(f"・氏名: {name}")
        print(f"・勤怠管理: {attendance_option}")
        print(f"・業務内容: {task_description if task_description else '（空欄）'}")
        print(f"・備考: {note if note else '（空欄）'}")

    except Exception as e:
        print(f"⚠️ {name}: 処理中にエラーが発生しました:", e)

    finally:
        driver.quit()
        time.sleep(1)

# --- 実行（3名分ループ） ---
for user in users:
    task = "" if args.mode == "start" else user["task"]
    submit_form(
        name=user["name"],
        task_description=task,
        attendance_option=attendance_option,
        note=""
    )
