import json
import openai
from logger import get_logger

logger = get_logger(__name__)
openai_client = openai.OpenAI()


def generate_summary(data: dict) -> str:
    logger.info("Generating investment signal via OpenAI")
    chat_completions = openai_client.chat.completions.create(
        top_p=1,
        temperature=0.3,
        frequency_penalty=0.3,
        presence_penalty=0.1,
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a world-class crypto expert specialising in investment signals. Based on the data provided, return a BUY, SELL, or WAIT signal. Consider that historically, the most appropriate moment to enter the crypto market is when the fear and greed index indicates fear or extreme fear, and when the CBBI (Crypto Bull Bear Index) is BULLISH (value at or below 10), which historically signals market bottoms and prime buying opportunities. Coins available on top exchanges like Binance, Bybit, and Coinbase are generally more attractive due to increased liquidity and trust. Only use the data provided.",
            },
            {"role": "user", "content": json.dumps(data)},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "investment_signal",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "signal": {"type": "string", "enum": ["BUY", "SELL", "WAIT"]},
                        "summary": {"type": "string"},
                    },
                    "required": ["signal", "summary"],
                    "additionalProperties": False,
                },
            },
        },
    )
    result = json.loads(chat_completions.choices[0].message.content)
    logger.info("Signal: %s", result["signal"])
    return result
