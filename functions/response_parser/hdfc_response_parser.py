import json
from glom import glom, Coalesce

with open('mappings/hdfc_mapping.json') as f:
    mapping = json.load(f)
    
def extract_values(quotes):
    additional_details = {}
    for key, value in quotes.items():
        if key not in mapping:
            additional_details[key] = value
    return additional_details


spec = {
    'Plans':('quotes',[
            {'SupplierName': Coalesce('Supplier_Name',default = 'HDFC'),
            'SupplierID':  'Supplier_Id',
            'PlanID': 'Plan_Id',
            'PlanName':'Plan_Name',
            'IsSelected': Coalesce('IsSelected',default='false'),
            'SumAssured':'SumAssured',
            'TotalCover':'TotalCover',
            'OneTimePayout':'OneTimePayout',
            'OneTimePayoutPercentage':Coalesce('OneTimePayoutPercentage', default = 0),
            'PolicyTerm':'PolicyTerm',
            'ClaimsSettled':'Claims_Settled',
            'Premiums' :('premiumFrequency',[
                        {
                            'PaymentFrequency': 'PaymentFrequency',
                            'PremiumWithoutGST': 'PremiumWithoutGST',
                            'GSTOnPremium': 'GST_On_Premium',
                            'TotalPremium': 'Total_Premium',
                            'TotalPremiumWithRiders':'TotalPremiumWithRiders',
                            'AdditionalDetails':extract_values,
                        }
                    ]),
            "Riders":('riderDetails',[
                {
                    'RiderName':'Rider_Name',
                    'RiderId': 'riderId',
                    'PlanID': 'Plan_Id' ,
                    'CategoryId': 'categoryId',
                    'MinSumAssured':'MinSum',
                    'MaxSumAssured':'MaxSum',
                    'PolicyTerm':'PolicyTerm',
                    'PremiumPayingTerm':'PremiumPayingTerm',
                    'TypeSelected':'TypeSelected',
                    'SumInsured': 'SumInsured',
                    'Premiums' :('premiumFrequency',[
                        {
                            'PaymentFrequency': 'PaymentFrequency',
                            'PremiumWithoutGST': 'PremiumWithoutGST',
                            'GSTOnPremium': 'GST_On_Premium',
                            'TotalPremium': 'Total_Premium',
                            'TotalPremiumWithRiders':'TotalPremiumWithRiders',
                            'AdditionalDetails':extract_values
                            # 'AdditionalDetails':Invoke(extract_values),
                            # 'AdditionalDetails':Assign('Extra',extract_values())
                        }
                    ]),
                    'AdditionalDetails':extract_values,
                }
            ]),
            'AdditionalDetails':extract_values,
            }
    ]),
    'PolicyTerm':'premiumPayingTerm',
    'IsPremiumDiscounted':'IsPremiumDiscounted',
    'AdditionalDetails':extract_values,
}

def final_response(response):
    standard_data = glom(response,spec)
    return standard_data






