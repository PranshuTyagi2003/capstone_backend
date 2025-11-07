import google.generativeai as genai
from app.config.settings import get_settings
import logging
import time

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        settings = get_settings()
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.TextGenerationModel(name='gemini-1.5-flash')

    def generate_customer_response(self, query: str, customer_context: dict) -> str:
        prompt = self._build_prompt(query, customer_context)
        max_retries = 3

        for attempt in range(max_retries):
            try:
                response = self.model.generate_text(prompt)
                return response.text
            except Exception as e:
                logger.error(f"Gemini API call failed on attempt {attempt + 1}: {str(e)}")
                time.sleep(1)

        return "Sorry, I am unable to answer your question right now. Please try again later."

    def _build_prompt(self, query: str, context: dict) -> str:
        status = context.get('dunning_status', 'UNKNOWN')
        overdue_days = context.get('overdue_days', 0)
        outstanding = context.get('outstanding_amount', 0)
        customer_type = context.get('customer_type', 'UNKNOWN')
        plan = context.get('plan_type', 'UNKNOWN')

        prompt = f"""
You are a helpful customer support assistant for a telecom company.

Customer Info:
- Status: {status}
- Overdue Days: {overdue_days}
- Outstanding Balance: ₹{outstanding}
- Customer Type: {customer_type}
- Plan: {plan}

Customer Query: "{query}"

Answer clearly, empathetically, and professionally. Explain status, restrictions, and next steps in simple words.
"""
        return prompt
