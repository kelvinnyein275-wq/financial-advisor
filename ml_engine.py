from google import genai
from dotenv import load_dotenv
import pandas as pd
import os

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler



load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)



df = pd.read_json("personal_finance_dataset.json")
X = df[["age", "income", "expenses", "savings"]].copy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
model = KMeans(n_clusters=5, random_state=42)
model.fit(X_scaled)
X["Clusters"] = model.labels_
cluster_data = X.groupby("Clusters").median()

def create_chat(client):
    return client.chats.create(model="gemini-3.5-flash-lite")

def financial_advice(chat, prompt):
    
    try:
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Temporarily unavailable. Please try again later. Error: {e}"
    

def cluster_predictions(age, income, expenses, savings):
    new_customer = pd.DataFrame(
        [[age, income, expenses, savings]],
        columns=["age", "income", "expenses", "savings"]
    )

    new_customer_scaled = scaler.transform(new_customer)

    prediction = model.predict(new_customer_scaled)

    return prediction[0]

def profiling(cluster):
    profiles = {
    0: {
        "name": "High Income Balanced",
        "description": "You earn a strong income while maintaining a healthy balance between spending and saving. Your finances show a stable approach, giving you room to enjoy your income while continuing to build financial security."


    },

    1: {
        "name": "High Income High Spender",
        "description": "You have a strong income, but a significant portion goes toward expenses. Your earning power gives you plenty of financial potential, and managing spending more carefully could help you turn more of that income into long-term savings."
    },

    2: {
        "name": "Moderate Income Saver",
        "description": "You may not have the highest income, but you make good use of what you earn. Your ability to keep expenses under control and consistently save puts you on a solid path toward building greater financial stability."
    },

    3: {
        "name": "Financially Strained",
        "description": "A large portion of your income is currently being used to cover expenses, leaving less room for savings. Focusing on manageable spending changes and gradually building savings could help create more financial breathing room over time."
    },

    4: {
        "name": "Wealth Builder",
        "description": "You combine a strong income with controlled spending and high savings. This puts you in a strong position to grow your financial resources and work toward longer-term goals while maintaining your current saving habits."
    }
}

    return profiles[cluster]

def get_cluster_medians(cluster):
    return cluster_data.loc[cluster]

def financial_context_function(age, income, expenses, savings, cluster, profile_name):
    financial_context = {
        "age": age,
        "income": income,
        "expenses": expenses,
        "savings": savings,
        "cluster": cluster,
        "profile_name": profile_name
    }
    return financial_context

def create_financial_prompt(context):
    
    prompt = f"""
        You are a personal financial education assistant.

        Here is the user's financial information:

        Age: {context["age"]}
        Income: {context["income"]}
        Expenses: {context["expenses"]}
        Savings: {context["savings"]}

        Financial Profile:
        Cluster: {context["cluster"]}
        Profile Name: {context["profile_name"]}

        Use this information to provide personalized financial guidance.

        Formatting rules:
        - Do not use Markdown.
        - Do not use *, **, #, or Markdown headings.
        - Use plain text only.
        - Keep paragraphs short and easy to read.
        """

    return prompt

def create_history_prompt(chat_history):
    prompt = "Here is the conversation so far:\n\n"

    for message in chat_history:
        prompt += f'{message["role"]}: {message["message"]}\n'

    prompt += f'''\nRespond to the user's latest message.
    Formatting rules:
    - Do not use Markdown.
    - Do not use *, **, #, or Markdown headings.
    - Use plain text only.
    - Keep paragraphs short and easy to read.
    
    '''
   


    return prompt