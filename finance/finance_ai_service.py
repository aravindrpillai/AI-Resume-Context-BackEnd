from __future__ import annotations

import json
from aiengine.handler import AIAgentHandler
from finance.prompt import FINANCE_SYSTEM_PROMPT
from finance.models import FinancialAdvisor
from ai.constants import CLAUDE_MODEL, OPENAI_MODEL


class FinanceAIService:

    def __init__(self):
        self.handler = AIAgentHandler(
            provider="openai",
            model=OPENAI_MODEL,
            system_prompt=FINANCE_SYSTEM_PROMPT,
        )

    def _build_state(self, record: FinancialAdvisor) -> dict:
        return {
            # Identity & Demographics
            "age":               record.age,
            "city":              record.city,
            "employment_status": record.employment_status,

            # Income
            "primary_income":    float(record.primary_income),
            "secondary_income":  float(record.secondary_income),

            # Fixed Expenses
            "rent_mortgage":     float(record.rent_mortgage),
            "insurance_premiums": float(record.insurance_premiums),
            "subscriptions":     float(record.subscriptions),
            "outstanding_loans": float(record.outstanding_loans),

            # Variable Expenses
            "variable_expenses": float(record.variable_expenses),

            # Assets
            "savings_balance":   float(record.savings_balance),
            "investments":       float(record.investments),
            "property_value":    float(record.property_value),
            "emergency_fund":    float(record.emergency_fund),

            # Goals
            "goals":             record.goals,
        }

    def _build_payload(self, record: FinancialAdvisor) -> dict:
        state = self._build_state(record)
        return {
            "conversation": [
                {
                    "role": "user",
                    "content": "Please analyse my financial profile and generate my financial health report.",
                }
            ],
            "current_state": state,
            "instruction": (
                "Analyse the financial profile provided in current_state. "
                "Return a complete financial health report strictly following "
                "the JSON structure defined in your instructions. "
                "Use the actual numbers from the profile in your analysis."
            ),
        }

    def generate(self, record: FinancialAdvisor) -> FinancialAdvisor:
        payload = self._build_payload(record)

        response = self.handler.push_message(payload=payload)

        raw_text = response.get("text", "")

        try:
            ai_response = json.loads(raw_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"AI returned invalid JSON: {e}\n\nRaw response:\n{raw_text}")

        record.ai_response = ai_response
        record.save()

        return record
