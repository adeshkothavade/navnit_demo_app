import json
import os
from glom import glom, Coalesce

def get_data(mapping_file, spec_file,data):

    with open(mapping_file) as f:
        mapping = json.load(f)
    
    with open(spec_file) as f:
        spec = json.load(f)

        
        #This function puts in all the additional values into a dictionary
        def extract_values(quotes):
            additional_details = {}
            for key, value in quotes.items():
                if key not in mapping:
                    additional_details[key] = value
            return additional_details


        def spec_builder(data):
            if isinstance(data,tuple):
                if any(isinstance(el, list) for el in data):
                    return (data[0],[spec_builder(data[1])])
                    
            if isinstance(data,list):
                if any(isinstance(el, list) for el in data):
                    data=tuple(data)
                    return spec_builder(data)
                    
                elif any(isinstance(el, dict) for el in data):
                    return spec_builder(data[0])
            
            elif isinstance(data,dict):
                if 'AdditionalDetails' in data:
                    data['AdditionalDetails']= extract_values
                return {key: spec_builder(value) for key, value in data.items()}
            else:
                return data
    
    
        specification = spec_builder(spec)

        def final_response():
            target = data
            standard_data = glom(target,specification)
            return standard_data


        response = final_response()

    return response


