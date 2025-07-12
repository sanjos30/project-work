import pandas as pd
import os
from openai import OpenAI
from tiktoken import encoding_for_model

def ask_questions_from_csv(csv_path: str, questions_path: str, model: str, save_path: str) -> str:
    # Initialize OpenAI
    from dotenv import load_dotenv
    load_dotenv() 
    API_KEY = os.getenv("OPENAI_API_KEY") 
    
    client = OpenAI(api_key=API_KEY)


    df = pd.read_csv(csv_path)
    df = df.sort_values(by="date")
    # csv_string = df.to_json(orient='records', indent=2)
    csv_string = df.to_markdown(index=False)

    with open(questions_path, 'r', encoding='utf-8') as f:
        questions = f.read().strip().split('\n')

    answers = []

    for question in questions:
        prompt = f"""You are a financial data analyst. Given this table, answer the following question.
            DATA: {csv_string}
            QUESTION: {question}"""
        response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1500
        )
        answers.append(f"Q: {question}\n A: {response.choices[0].message.content}\n")
    
    with open(f"{save_path}", "w", encoding="utf-8") as f:
        for answer in answers:
            f.write(f"{answer}\n\n")

    return f"answers saved to {save_path}"




if __name__ == "__main__":
    CSV_FILE = "prompts_test/transactions_for_prompt_gen.csv"
    QUESTIONS_FILE = "prompts_test/hallucination_prompts.txt"
    SAVE_PATH = "prompts_test/hallucination_answers.txt"
    result = ask_questions_from_csv(csv_path=CSV_FILE, questions_path=QUESTIONS_FILE, model="gpt-4o", save_path=SAVE_PATH)

    print(result)
