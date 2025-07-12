import os
import pandas as pd
from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv()  # Load variables from .env
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

# TRANSACTIONS_FOLDER = "bank_statements_prompt_gen"  
# N_ROWS = 200  

def create_csv_for_prompt_generation(TRANSACTIONS_FOLDER, N_ROWS, PROMPTS_FOLDER):
    if not os.path.exists(PROMPTS_FOLDER):
        os.makedirs(PROMPTS_FOLDER)
    csv_files = [f for f in os.listdir(TRANSACTIONS_FOLDER) if f.endswith(('.csv'))]
    df_list = []
    # print("df_list", df_list)
    for file in csv_files:
        try:
            df = pd.read_csv(os.path.join(TRANSACTIONS_FOLDER, file))
            df_list.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    df = pd.concat(df_list, ignore_index=True)
    # print("df", df)
    df = df.sample(frac=1, random_state=33).head(N_ROWS).reset_index(drop=True)
    df.to_csv(f"{PROMPTS_FOLDER}/transactions_for_prompt_gen.csv", index=False)
    print("csv saved")
    return df


def build_context_summary(df):
    context = ""
    for _, row in df.iterrows():
        context += (
            f"- Date: {row['date']}, Merchant: {row['merchant']}, Category: {row['category']}, "
            f"Amount: {row['amount']} {row['currency']}, Payment Mode: {row['payment_mode']}, "
            f"Type: {row['type']}\n"
        )
    return context

# context_summary = build_context_summary(df)

def generate_prompt(task_instruction, num_prompts, filename, context_summary):
    system_msg = (
        "Assume you are a top of your field data scientist expert and prompt engineer tasked with generating high-quality prompts for testing LLMs "
        "using a batch of transaction data. The prompts should follow the instruction below."
    )

    user_msg = (
        f"Transaction data summary (200 samples):\n{context_summary}\n\n"
        f"Instruction: {task_instruction}\n\n"
        f"Generate {num_prompts} unique, relevant prompts. Return only the prompts as a numbered list."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.7,
            max_tokens=1500,
        )
        prompts = response.choices[0].message.content.strip()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(prompts)
        print(f" Saved {num_prompts} prompts to {filename}")
    except Exception as e:
        print(f"Error generating {filename}: {e}")

# generate_prompt(
#     task_instruction="Assume you are a top of your field data scientist expert and prompt engineer. Create prompts that test the model’s ability to do statistical analysis or summarization, like totals, averages, or trends across transaction data.",
#     num_prompts=25,
#     filename="prompts/statistical_prompts.txt"
# )

# generate_prompt(
#     task_instruction="Assume you are a top of your field data scientist expert and prompt engineer. Create prompts that require subjective reasoning or human-like interpretation, such as suspicious activity, intent, or user behavior.",
#     num_prompts=25,
#     filename="prompts/subjective_prompts.txt"
# )

# generate_prompt(
#     task_instruction="Assume you are a top of your field data scientist expert and prompt engineer. Create prompts that test whether an LLM hallucinates or fabricates facts. Ask questions that only make sense if the model uses only the given data and avoids adding made-up information.",
#     num_prompts=10,
#     filename="prompts/hallucination_prompts.txt"
# )
