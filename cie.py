import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import base64
#openai
encoded_api_key = 'c2stcHJvai1VZUw2cFNZUldmb2FCenppQ3pBYXRLLU4xNTg1Qno0YXpmZkdRTjlfMDc3RFh6a3RGZUZtVE9vaEU1Nlduby1jU0M4RXVpSDZZVVQzQmxia0ZKcDZjeXkySjJ5aGg1WW5XeVh5YVREZWlHQU52akloMEhvdWtvYnpvc2ZVLVlfUjZiSVhkQWRPZC1ZaWNRdDZGUGFuSnhwSm5iVUE='  
api_key = base64.b64decode(encoded_api_key).decode('utf-8')

openai.api_key = api_key
def get_best_answer(question, answers):
    prompt = f"Question: {question}\nOptions:\n"
    for i, answer in enumerate(answers, 1):
        prompt += f"{i}. {answer}\n"
    
    prompt += "Which option seems to be the best answer? Provide the number of the option."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        temperature=0.5
    )

    answer_text = response.choices[0].text.strip()
    try:
        answer_number = int(answer_text.split()[0])  
        return answer_number
    except ValueError:
        return 1  

#Selenium
username = input("Enter SRN: \n")
password = input("Enter password: \n")
username.strip()
password.strip()
driver = webdriver.Chrome()

driver.get("https://www.pesuacademy.com/Assessment/")
username_field = driver.find_element(By.NAME, "j_username")
username_field.send_keys(username)
password_field = driver.find_element(By.NAME, "j_password")
password_field.send_keys(password)
sign_in_button = driver.find_element(By.ID,"postloginform#/Assessment/j_spring_security_check")
sign_in_button.click()

time.sleep(2)

iagreebutton  = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div/div[5]/div/div[2]/div/table/tbody/tr/td[2]/button")
iagreebutton.click()

for question_num in range(10):
    time.sleep(2)  # wait for question to load

    # Extract question text
    question = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[1]/div/div[1]/div[1]/strong").text
    print(f"Question {question_num + 1}: {question}")

    # Extract answer choices
    answer1prompt = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[1]/div/div[1]/div[2]/ul/li[1]/label").text
    answer2prompt = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[1]/div/div[1]/div[2]/ul/li[2]/label").text
    answer3prompt = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[1]/div/div[1]/div[2]/ul/li[3]/label").text
    answer4prompt = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[1]/div/div[1]/div[2]/ul/li[4]/label").text

    answers = [answer1prompt, answer2prompt, answer3prompt, answer4prompt]
    print(f"Answer 1: {answer1prompt}")
    print(f"Answer 2: {answer2prompt}")
    print(f"Answer 3: {answer3prompt}")
    print(f"Answer 4: {answer4prompt}")



    selected_answer_index = get_best_answer(question, answers)

    if selected_answer_index == 1:
        driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[1]/div/div[1]/div[2]/ul/li[1]/input").click()
    elif selected_answer_index == 2:
        driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[1]/div/div[1]/div[2]/ul/li[2]/input").click()
    elif selected_answer_index == 3:
        driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[1]/div/div[1]/div[2]/ul/li[3]/input").click()
    elif selected_answer_index == 4:
        driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[1]/div/div[1]/div[2]/ul/li[4]/input").click()

    # Click on the "Next" button
    time.sleep(1)
    next_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[1]/div/div[3]/div[1]/ul/li/a")
    next_button.click()

    # Click confirm on pop-up
    time.sleep(1)
    confirmbutton = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/button[1]") 
    confirmbutton.click()

# End test process
time.sleep(1)
endtest = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[2]/div/div[2]/div[2]/div/button")
endtest.click()

time.sleep(1)
endtestconfirm = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/button[2]")
endtestconfirm.click()

driver.quit()
