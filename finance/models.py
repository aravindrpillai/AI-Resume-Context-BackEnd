import uuid
from django.db import models

ALLOWED_FIELDS = [
    "age",
    "city",
    "employment_status",
    "primary_income",
    "secondary_income",
    "rent_mortgage",
    "insurance_premiums",
    "subscriptions",
    "outstanding_loans",
    "variable_expenses",
    "savings_balance",
    "investments",
    "property_value",
    "emergency_fund",
    "goals",
    "ai_response",
]

class FinancialAdvisor(models.Model):
    EMPLOYMENT_STATUS_CHOICES = [
        ('employed', 'Employed'),
        ('self_employed', 'Self-Employed'),
        ('unemployed', 'Unemployed'),
        ('student', 'Student'),
        ('retired', 'Retired'),
    ]

    # Identity & Demographics
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    age = models.IntegerField()
    city = models.CharField(max_length=255)
    employment_status = models.CharField(max_length=50, choices=EMPLOYMENT_STATUS_CHOICES)

    # Income
    primary_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    secondary_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Fixed Expenses
    rent_mortgage = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    insurance_premiums = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subscriptions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    outstanding_loans = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Variable Expenses
    variable_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Assets
    savings_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    investments = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    property_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    emergency_fund = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Goals
    goals = models.TextField(blank=True)

    # AI Response
    ai_response = models.JSONField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'financial_advisor'
        ordering = ['-created_at']

    def __str__(self):
        return f"FinancialAdvisor {self.id} — Age {self.age}, {self.city}"

        
    def show(self):
        return {
            "id": str(self.id),
            "age": self.age,
            "city": self.city,
            "employment_status": self.employment_status,
            "primary_income": float(self.primary_income),
            "secondary_income": float(self.secondary_income),
            "rent_mortgage": float(self.rent_mortgage),
            "insurance_premiums": float(self.insurance_premiums),
            "subscriptions": float(self.subscriptions),
            "outstanding_loans": float(self.outstanding_loans),
            "variable_expenses": float(self.variable_expenses),
            "savings_balance": float(self.savings_balance),
            "investments": float(self.investments),
            "property_value": float(self.property_value),
            "emergency_fund": float(self.emergency_fund),
            "goals": self.goals,
            "ai_response": self.ai_response,
            "created_at": self.created_at.isoformat(),
        }

