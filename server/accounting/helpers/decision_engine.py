class DecisionEngine:
    def __init__(self, business_name, year_established, profit_or_loss_summary, pre_assessment_value):
        self.business_name = business_name
        self.year_established = year_established
        self.profit_or_loss_summary = profit_or_loss_summary
        self.pre_assessment_value = pre_assessment_value
    
    def decide(self):
        approved = self.pre_assessment_value >= 60
        return "Approved" if approved else "Rejected"

  
