from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["start", "end"], required=True)
args = parser.parse_args()

attendance_option = "勤務開始(Start of work)" if args.mode == "start" else "勤務終了(End of work)"

users = [
    {"name": "明石到真", "task": "資料の整理とチーム内共有"},
    {"name": "下山佳南", "task": "マーケティングデータの集計"},
    {"name": "野宮勇介", "task": "SNSキャンペーンのレポート作成"}
]

form_url = "https://forms.office.com/Pages/ResponsePage.aspx?id=s-vy4xAIWUmOBWzs2MAP8pBcJeApFIhNgiKUedRi32NUNTZMMlJCUllCODRTTjlOOEs1V1NWM0FCVS4u"

def submit_form(name, task_description, attendance_option, note=""):
    print(f"\n--- {name} さんの送信を開始します ---")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/google-chrome"

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    try:
        driver.get(form_url)

        text_inputs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[data-automation-id="textInput"]')))
        text_inputs[0].send_keys(name)
        text_inputs[1].send_keys(task_description)
        text_inputs[2].send_keys(note)

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
            except Exception:
                continue

        if not selected:
            print(f"⚠️ {name}: 勤怠管理の選択に失敗しました。")
            return

        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-automation-id="submitButton"]')))
        submit_button.click()

        confirmation_text = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="heading"]')))
        print("✅ フォーム送信に成功しました！")
        print(f"・氏名: {name}")
        print(f"・勤怠管理: {attendance_option}")
        print(f"・業務内容: {task_description}")
        print(f"・備考: {note if note else '（空欄）'}")

    except Exception as e:
        print(f"⚠️ {name}: エラーが発生しました:", e)

    finally:
        driver.quit()
        time.sleep(1)

for user in users:
    submit_form(user["name"], user["task"], attendance_option)
