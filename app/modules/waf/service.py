import pickle
from loguru import logger

class WAF():
    def __init__(self, model_path: str = "waf_model.sav"):
       self.model = self.load_model(model_path)
       
    def load_model(self, model_path):
        return pickle.load(open(model_path, 'rb'))
    
    def waf_check(self, payload: list):
        results = []
        for field in payload:
            prediction = self.model.predict([field])
            if "valid" in prediction or "shell" in prediction:  
                logger.success(
                    f"\n\tПараметр: {field}\n"
                    f"\tАтаки нет!"
                    )
                results.append(True)
            else:
                logger.error(
                    f"\n\tОбнаружена атака!\n"
                    f"\tПараметр: {field}\n"
                    f"\tТип аттаки: {prediction[0]}"
                    )
                results.append(False)
        return results
            
