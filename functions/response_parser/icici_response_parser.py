import json
from glom import glom, Coalesce

with open('mappings/icici_mapping.json') as f:
    mapping = json.load(f)
    

def extract_values(quotes):
    additional_details = {}
    for key, value in quotes.items():
        if key not in mapping:
            additional_details[key] = value
    return additional_details

spec = {'Plans':('PremiumSummary',
                    [ 
                        { 
                            'SupplierName': Coalesce('SupplierName', default = 'ICICI'),
                            'SupplierID': Coalesce('SupplierID', default = 5),
                            'PlanID': 'ProductCode',
                            'PlanName':'ProductName',
                            'TotalCover':Coalesce('TotalCover',default = 'Not defined'),
                            'OneTimePayoutPercentage':Coalesce('OneTimePayoutPercentage', default = 0),
                            'PolicyTerm':'PremiumPaymentTerm',
                            'Term':'Term',
                            'PayoutTerm':'PayoutTerm',
                            'IsSelected':'SelectedOption',
                            'AnnualPremium':'AnnualPremium',
                            'DeathBenefit':'DeathBenefit',
                            'Premiums':{
                                'PaymentFrequency':Coalesce('PaymentFrequency', default = 12),
                                'PremiumWithoutGST':'PremiumInstallment',
                                'TotalPremium':'PremiumInstallmentWithTax',
                                'modeOfPremium':'ModeOfPayment',
                                'AdditionalDetails':extract_values,
                            },
                            'Riders':('RiderDetails.Rider',[
                                {
                                    'RiderName':'Name',
                                    'SumAssured':'SA',
                                    'Term':'Term',
                                    'Premiums':{
                                        'PaymentFrequency':Coalesce('PaymentFrequency', default = 12),
                                        'Premium':'Premium',
                                        'ServiceTax':'ServiceTax',
                                        'AdditionalDetails':extract_values,
                                    }
                                }
                            ]
                            ),
                            'AdditionalDetails':extract_values,
                        }
                    ]
                ),  
                'AdditionalDetails':extract_values,
        }

def final_response(response):
    standard_data = glom(response,spec)
    return standard_data
