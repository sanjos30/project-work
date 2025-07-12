# Neon Financial Records - Full Workflow

This project demonstrates how to use OpenAI models to analyze financial transaction data and answer custom questions using a Jupyter Notebook workflow.

## Prerequisites

- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/installation/)
- OpenAI API key

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/Neon-FinancialRecords.git
   cd Neon-FinancialRecords
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key:**
   - Create a `.env` file in the project root:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

## Step-by-Step Instructions on running the Workflow

1. **Install Jupyter Notebook (if not already installed):**
   ```sh
   pip install notebook
   ```

2. **Start the Jupyter Notebook server:**
   ```sh
   jupyter notebook
   ```
   ** Before running the notebook remember to delete the csv files from bank_statements and bank_statements_prompt_gen **

3. **Open the Notebook:**
   - After running the command above, a browser window will open.
   - Navigate to the project folder and click on `full_workflow.ipynb` to open it.

4. **Run the Notebook Cells:**
   - Click on the first cell.
   - Press `Shift + Enter` to execute the cell.
   - Continue running each cell in order, following any instructions or prompts in the notebook.

5. **Review Results:**
   - The notebook will display outputs, answers, and any saved files as specified in each cell.
