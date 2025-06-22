import json
import openai

openai_client = openai.OpenAI()


def generate_summary(data: dict) -> str:
    chat_completions = openai_client.chat.completions.create(
        top_p=1,
        temperature=0.3,
        frequency_penalty=0.3,
        presence_penalty=0.1,
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a world-class crypto expert specialising in providing concise investment advice. Based on the data provided, deliver a single paragraph summary that analyzes current market conditions, sentiment, and trends. Use simple language for the average investor. Consider that historically, the most appropriate moment to enter the crypto market is when the fear and greed index indicates fear or extreme fear. Also note that coins available on top exchanges like Binance, Bybit, and Coinbase are generally more attractive for potential investors due to increased liquidity, trust, and accessibility. Your response should end with an objective assessment. If you don't have enough information to make a clear recommendation, state this explicitly. Only use the data provided and avoid making claims if you're not confident.",
            },
            {"role": "user", "content": json.dumps(data)},
        ],
    )
    summary = chat_completions.choices[0].message.content
    return summary
