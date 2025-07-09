import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 사용자로부터 입력 받기
num_articles = int(input("몇 개의 article에 대해 테스트를 할까요? "))
author_info_choice = input("저자 정보를 누를까요? (yes, no, random): ").strip().lower()
memo_choice = input("메모를 남길까요? (yes, no, random): ").strip().lower()
feedback_choice = input("피드백을 남길까요? (yes, no, random): ").strip().lower()
rating_choice = input("별점을 남길까요? (yes, no, random): ").strip().lower()

# 웹 드라이버 설정 (Chrome 브라우저 사용)
driver = webdriver.Chrome()

# 데이터 수집을 위한 리스트 초기화
data = []

def process_article(article_element):
    # 아티클 클릭
    article_title = article_element.text
    article_id = article_element.get_attribute("href").split('/')[-1]  # URL에서 아티클 ID 가져오기
    article_element.click()

    # 아티클 페이지로 이동 후 2~5초 대기 (랜덤)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
    duration = random.randint(2, 5)
    time.sleep(duration)

    # 저자 정보 클릭
    if author_info_choice == "yes" or (author_info_choice == "random" and random.choice([True, False])):
        author_info_button = driver.find_element(By.CSS_SELECTOR, ".modal-button")
        author_info_button.click()
        time.sleep(1)
        close_modal_button = driver.find_element(By.XPATH, "//div[@id='authorModal']//button[@onclick='closeModal()']")
        close_modal_button.click()
        author_info_clicked = True
    else:
        author_info_clicked = False

    # 메모 작성
    if memo_choice == "yes" or (memo_choice == "random" and random.choice([True, False])):
        memo_button = driver.find_element(By.CSS_SELECTOR, ".memo-button")
        memo_button.click()
        time.sleep(0.5)  # 더 긴 대기 시간
        memo_textarea = driver.find_element(By.ID, "memoText")
        memo_text = "이것은 자동화된 메모입니다."
        memo_textarea.send_keys(memo_text)
        time.sleep(0.5)  # 더 긴 대기 시간
        save_button = driver.find_element(By.XPATH, "//button[contains(text(), '저장')]")
        driver.execute_script("arguments[0].click();", save_button)  # JavaScript로 클릭
        memo_written = memo_text
    else:
        memo_written = None

    # 피드백 작성
    if feedback_choice == "yes" or (feedback_choice == "random" and random.choice([True, False])):
        feedback_textarea = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "userAnswer"))
        )
        feedback_text = "이것은 자동화된 피드백입니다."
        feedback_textarea.send_keys(feedback_text)
        time.sleep(0.5)  # 더 긴 대기 시간
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit')]"))
        )
        driver.execute_script("arguments[0].click();", submit_button)  # JavaScript로 클릭
        feedback_given = feedback_text
    else:
        feedback_given = None

    # 별점 입력
    if rating_choice == "yes" or (rating_choice == "random" and random.choice([True, False])):
        rating_buttons = driver.find_elements(By.CSS_SELECTOR, ".rating-button")
        rating = random.randint(1, len(rating_buttons))  # 1부터 최대 별점까지 랜덤
        rating_buttons[rating - 1].click()
        time.sleep(0.5)  # 더 긴 대기 시간
        rating_given = rating
    else:
        rating_given = None

    # 데이터 저장
    data.append({
        "article_id": article_id,
        "article_title": article_title,
        "author_info_clicked": author_info_clicked,
        "memo_written": memo_written,
        "feedback_given": feedback_given,
        "rating_given": rating_given,
        "duration": duration
    })

    return article_id

def visit_article(article_element):
    # 아티클 페이지를 처리하고, 내부 링크를 통해 다른 아티클로 넘어가는 경우도 추적
    initial_article_id = process_article(article_element)
    
    # 아티클 페이지에서 내부 링크를 찾고, 클릭하여 다른 아티클로 이동
    internal_links = driver.find_elements(By.CSS_SELECTOR, ".internal-link")  # 내부 링크를 찾는 CSS 선택자
    for link in internal_links:
        link_text = link.text
        link_id = link.get_attribute("href").split('/')[-1]  # URL에서 아티클 ID 가져오기
        link.click()
        
        # 새 아티클 페이지로 이동 후 2~5초 대기 (랜덤)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
        time.sleep(random.randint(2, 5))
        
        # 새 아티클 페이지 처리
        process_article(driver.find_element(By.CSS_SELECTOR, ".article a[href*='{}']".format(link_id)))
        
        # 목록으로 돌아가기
        driver.back()
        time.sleep(0.5)  # 더 긴 대기 시간
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".container")))
        driver.find_elements(By.CSS_SELECTOR, ".article a")  # 아티클 목록 갱신

# 로그인 및 테스트 진행
try:
    # 로그인 페이지로 이동
    driver.get("http://127.0.0.1:5000")

    # 로그인 정보 입력
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.TAG_NAME, "button")

    username_input.send_keys("tester")
    password_input.send_keys("tester")
    login_button.click()

    # 로그인 후 index 페이지로 이동
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".container")))

    # 아티클 목록 가져오기
    articles = driver.find_elements(By.CSS_SELECTOR, ".article a")
    article_count = len(articles)
    visited_articles = []

    for _ in range(num_articles):  # 입력받은 수만큼 아티클 방문
        # 랜덤으로 아티클 선택
        random_index = random.randint(0, article_count - 1)
        while random_index in visited_articles:
            random_index = random.randint(0, article_count - 1)
        visited_articles.append(random_index)
        article = articles[random_index]

        visit_article(article)

    # "읽기 모두 끝내기" 버튼 클릭
    end_reading_button = driver.find_element(By.LINK_TEXT, "읽기 끝내기")
    driver.execute_script("arguments[0].click();", end_reading_button)  # JavaScript로 클릭
    time.sleep(0.5)  # 더 긴 대기 시간

    # "Export to Excel" 버튼 클릭
    export_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Export to Excel"))
    )
    driver.execute_script("arguments[0].click();", export_button)  # JavaScript로 클릭
    time.sleep(0.5)  # 더 긴 대기 시간

finally:
    # 완료 후 브라우저 종료
    time.sleep(2)
    driver.quit()

# 엑셀 파일로 데이터 저장
df = pd.DataFrame(data)
with pd.ExcelWriter('expected_results.xlsx') as writer:
    df.to_excel(writer, index=False)

print("예상 결과가 expected_results.xlsx 파일에 저장되었습니다.")