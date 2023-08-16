import json
import logging

def generate_request() -> dict:
    f = open('data/standard.json')
    input_data = json.load(f)
    f.close()

    f = open('mappings/hdfc_to_standard_mapping.json')
    mapping = json.load(f)
    f.close()    

    output_data = {
        "Plans": [],
        "PaymentTermType": input_data.get(mapping.get("PaymentTermType", "PaymentTermType"), None),
        "PolicyTerm": input_data.get(mapping.get("PolicyTerm", "PolicyTerm"), None),
        "PremiumPayingTerm": input_data.get(mapping.get("PremiumPayingTerm", "PremiumPayingTerm"), None),
        "IsPremiumDiscounted": input_data.get(mapping.get("IsPremiumDiscounted", "IsPremiumDiscounted"), None),
    }
    output_data["Plans"] = create_plan_details(input_data.get(mapping.get("Plans", "Plans"),[]), mapping)
    return output_data

def create_plan_details(plan_data, mapping):
    plans = []
    for plan in plan_data:
        plan_dict = {
            "PlanName": plan.get(mapping.get("PlanName", "PlanName"), None),
            "BasePlanId": plan.get(mapping.get("BasePlanId", "BasePlanId"), None),
            "PlanId": plan.get(mapping.get("PlanId", "PlanId"), None),
            "IsSelected": plan.get(mapping.get("IsSelected", "IsSelected"), None),
            "SumAssured": plan.get(mapping.get("SumAssured", "SumAssured"), None),
            "TotalCover": plan.get(mapping.get("TotalCover", "TotalCover"), None),
            "MonthlyIncome": plan.get(mapping.get("MonthlyIncome", "MonthlyIncome"), None),
            "OneTimePayout": plan.get(mapping.get("OneTimePayout", "OneTimePayout"), None),
            "OneTimePayoutPercentage": plan.get(mapping.get("OneTimePayoutPercentage", "OneTimePayoutPercentage"), None),
            "PolicyTerm": plan.get(mapping.get("PolicyTerm", "PolicyTerm"), None),
            "ClaimsSettled": plan.get(mapping.get("ClaimsSettled", "ClaimsSettled"), None),
            "Premiums": [],
            "Riders": [],
            "TropPlanPremiums": plan.get(mapping.get("TropPlanPremiums", "TropPlanPremiums"), None)
        }
        plan_dict["Premiums"] = create_premium_details(plan.get(mapping.get("Premiums", "Premiums"), []), mapping)
        plan_dict["Riders"] = create_rider_details(plan.get(mapping.get("Riders", "Riders"), []), mapping)
        plans.append(plan_dict)
    return plans

def create_rider_details(riders_data, mapping) -> list:
    riders = []
    for rider in riders_data:
        rider_dict = {
            "RiderName": rider.get(mapping.get("RiderName","RiderName"), None),
            "RiderId": rider.get(mapping.get("RiderId","RiderId"), None),
            "CategoryId": rider.get(mapping.get("CategoryId","CategoryId"), None),
            "IsSelected": rider.get(mapping.get("IsSelected","IsSelected"), None),
            "SumAssured": rider.get(mapping.get("SumAssured","SumAssured"), None),
            "MinSumAssured": rider.get(mapping.get("MinSumAssured","MinSumAssured"), None),
            "MaxSumAssured": rider.get(mapping.get("MaxSumAssured","MaxSumAssured"), None),
            "PolicyTerm": rider.get(mapping.get("PolicyTerm","PolicyTerm"), None),
            "PremiumPayingTerm": rider.get(mapping.get("PremiumPayingTerm","PremiumPayingTerm"), None),
            "TypeSelected": rider.get(mapping.get("TypeSelected","TypeSelected"), None),
            "Premiums": []
        }
        rider_dict["Premiums"] = create_premium_details(rider.get(mapping.get("Premiums","Premiums"), []), mapping)
        riders.append(rider_dict)
    return riders

def create_premium_details(premiums_data, mapping) -> list:
    premiums = []
    for premium in premiums_data:
        premium_dict = {
            "PaymentFrequency": premium.get(mapping.get("PaymentFrequency", "PaymentFrequency"), None),
            "PremiumWithoutGST": premium.get(mapping.get("PremiumWithoutGST", "PremiumWithoutGST"), None),
            "GSTOnPremium": premium.get(mapping.get("GSTOnPremium", "GSTOnPremium"), None),
            "TotalPremium": premium.get(mapping.get("TotalPremium", "TotalPremium"), None),
            "TotalPremiumWithRiders": premium.get(mapping.get("TotalPremiumWithRiders", "TotalPremiumWithRiders"), None),
            "survivalBenefit": premium.get(mapping.get("survivalBenefit", "survivalBenefit"), None),
            "SecondYearPremium": premium.get(mapping.get("SecondYearPremium", "SecondYearPremium"), None),
            "SecondYearPremiumWGST": premium.get(mapping.get("SecondYearPremiumWGST", "SecondYearPremiumWGST"), None)
        }
        premiums.append(premium_dict)
    return premiums