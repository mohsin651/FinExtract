import streamlit as st
import pandas as pd
import openai
import json


file = open("mohsin.txt", "r")
key=file.read().strip()

openai.api_key = key

def extract_financial_data(text):
    prompt = get_prompt_financial() + text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    content = response['choices'][0]['message']['content']

    try:
        data = json.loads(content)
        return pd.DataFrame(data.items(), columns=["Measure", "Value"])

    except (json.JSONDecodeError, IndexError):
        return None

def get_prompt_financial():
    return '''
    Please retrieve company name, revenue, net income and earnings per share (a.k.a. EPS)
    from the following news article. If you can't find the information from this article 
    then return "". Do not make things up.    
    Then retrieve a stock symbol corresponding to that company. For this you can use
    your general knowledge (it doesn't have to be from this article). Always return your
    response as a valid JSON string. The format of that string should be this, 
    {
        "Company Name": "Walmart",
        "Stock Symbol": "WMT",
        "Revenue": "12.34 million",
        "Net Income": "34.78 million",
        "EPS": "2.1 $"
    }
    News Article:
    ============
    '''

if __name__ == '__main__':
    text = '''
    Tesla's Earning news in text format: Tesla's earning this quarter blew all the estimates. They reported 4.5 billion $ profit against a revenue of 30 billion $. Their earnings per share was 2.3 $
    '''

    df = extract_financial_data(text)
    if df is not None:
        print(df.to_string())
    else:
        print("No financial data extracted.")

col1, col2 = st.columns([3,2])

financial_data_df = pd.DataFrame({
        "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
        "Value": ["", "", "", "", ""]
    })

with col1:
    st.title("Financial Data Extraction Tool")
    news_article = st.text_area("Paste your financial news article here", height=300)
    if st.button("Extract"):
        financial_data_df = extract_financial_data(news_article)

with col2:
    st.markdown("<br/>" * 5, unsafe_allow_html=True)  # Creates 5 lines of vertical space
    st.dataframe(
        financial_data_df,
        column_config={
            "Measure": st.column_config.Column(width=150),
            "Value": st.column_config.Column(width=150)
        },
        hide_index=True
    )