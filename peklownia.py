import random
import json
import yaml
import os
from datetime import datetime
from typing import Dict, Any, Optional

class RecipeBook:
    """
    Loads config from 'config/peklownia_config.yaml' or falls back to hardcoded dictionaries.
    """
    CLASSIC_08 = {
        "injection_pct": 8.0,
        "salt_concentration": 0.03,
        "tumbling_params": {"duration_min": 120, "rpm": 15}
    }
    LOW_SALT_05 = {
        "injection_pct": 5.0,
        "salt_concentration": 0.02,
        "tumbling_params": {"duration_min": 180, "rpm": 12}
    }

    def __init__(self, config_path: str = 'config/peklownia_config.yaml'):
        self.recipes = {
            "CLASSIC_08": self.CLASSIC_08,
            "LOW_SALT_05": self.LOW_SALT_05
        }
        self._load_config(config_path)

    def _load_config(self, config_path: str):
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config_data = yaml.safe_load(f)
                    if config_data and 'recipes' in config_data:
                        self.recipes.update(config_data['recipes'])
                    elif config_data and 'curing_process' in config_data:
                        # Map generic config to a default recipe if structure differs
                        self.recipes['DEFAULT_FROM_CONFIG'] = {
                            "injection_pct": config_data.get('targets', {}).get('injection_pct', 10.0),
                            "salt_concentration": config_data.get('targets', {}).get('salt_concentration', 0.03),
                            "tumbling_params": config_data.get('targets', {}).get('tumbling_params', {"duration_min": 60, "rpm": 10})
                        }
            except Exception as e:
                print(f"Error loading config: {e}. Using fallback recipes.")

    def get_recipe(self, name: str) -> Optional[Dict[str, Any]]:
        return self.recipes.get(name)

class PeklowniaBatch:
    """
    Represents a curing batch and validates against a RecipeBook.
    """
    def __init__(self, batch_id: str, injection_pct: float, salt_concentration: float, tumbling_params: Dict[str, Any]):
        self.batch_id = batch_id
        self.injection_pct = injection_pct
        self.salt_concentration = salt_concentration
        self.tumbling_params = tumbling_params
        self.timestamp = datetime.now().isoformat()
        self.metadata = {"random_seed": random.randint(1000, 9999)}

    def validate_vs_recipe(self, recipe_name: str, recipe_book: RecipeBook) -> Dict[str, Any]:
        recipe = recipe_book.get_recipe(recipe_name)
        if not recipe:
            return {"valid": False, "error": f"Recipe '{recipe_name}' not found."}

        errors = []
        if abs(self.injection_pct - recipe['injection_pct']) > 0.5:
            errors.append(f"Injection % deviation too high: {self.injection_pct} vs {recipe['injection_pct']}")
        
        if abs(self.salt_concentration - recipe['salt_concentration']) > 0.005:
            errors.append(f"Salt concentration deviation: {self.salt_concentration} vs {recipe['salt_concentration']}")

        # Simplified tumbling validation
        if self.tumbling_params.get('rpm', 0) < recipe['tumbling_params'].get('rpm', 0):
             errors.append("Tumbler RPM below recipe requirement.")

        is_valid = len(errors) == 0
        return {
            "valid": is_valid,
            "errors": errors,
            "batch_data": self.to_json(),
            "recipe_applied": recipe_name
        }

    def to_json(self) -> str:
        return json.dumps({
            "batch_id": self.batch_id,
            "injection_pct": self.injection_pct,
            "salt_concentration": self.salt_concentration,
            "tumbling_params": self.tumbling_params,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        })

if __name__ == "__main__":
    # Example usage
    book = RecipeBook()
    batch = PeklowniaBatch(
        batch_id="BATCH-2026-001",
        injection_pct=8.2,
        salt_concentration=0.031,
        tumbling_params={"duration_min": 120, "rpm": 16}
    )
    
    validation = batch.validate_vs_recipe("CLASSIC_08", book)
    print(f"Validation Result: {json.dumps(validation, indent=2)}")
