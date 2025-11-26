"""
Nutrition lookup service with fuzzy matching
"""

import pandas as pd
import logging
from typing import Optional, Dict, Any, List
from fuzzywuzzy import fuzz, process
from pathlib import Path

logger = logging.getLogger(__name__)


class NutritionService:
    """Service for nutrition data lookup with fuzzy matching"""
    
    def __init__(self, csv_path: str = "data/nutrition_lookup.csv"):
        self.csv_path = Path(csv_path)
        self.df = None
        self.dish_names = []
        self._load_nutrition_data()
    
    def _load_nutrition_data(self):
        """Load nutrition data from CSV file"""
        try:
            if not self.csv_path.exists():
                logger.error(f"❌ Nutrition CSV file not found: {self.csv_path}")
                return
            
            self.df = pd.read_csv(self.csv_path)
            self.dish_names = self.df['dish_name'].str.lower().tolist()
            
            logger.info(f"✅ Loaded {len(self.df)} dishes from nutrition database")
            
        except Exception as e:
            logger.error(f"❌ Failed to load nutrition data: {e}")
            self.df = None
            self.dish_names = []
    
    def fuzzy_match_dish(self, dish_name: str, threshold: int = 70) -> Optional[Dict[str, Any]]:
        """
        Find closest dish match using fuzzy string matching
        
        Args:
            dish_name: Name of dish to search for
            threshold: Minimum similarity score (0-100)
            
        Returns:
            Dictionary with dish data or None if no match found
        """
        if self.df is None or not self.dish_names:
            logger.warning("⚠️ Nutrition data not available")
            return None
        
        try:
            # Normalize input
            normalized_dish = dish_name.lower().strip()
            
            # Find best match using fuzzy matching
            best_match = process.extractOne(
                normalized_dish, 
                self.dish_names,
                scorer=fuzz.ratio
            )
            
            if best_match and best_match[1] >= threshold:
                matched_name = best_match[0]
                confidence = best_match[1]
                
                # Get the row data
                row = self.df[self.df['dish_name'].str.lower() == matched_name].iloc[0]
                
                result = {
                    'original_query': dish_name,
                    'matched_name': row['dish_name'],
                    'confidence': confidence,
                    'calories': int(row['calories']),
                    'meal_type': row['meal_type'],
                    'protein_g': float(row['protein_g']) if pd.notna(row['protein_g']) else None,
                    'carbs_g': float(row['carbs_g']) if pd.notna(row['carbs_g']) else None,
                    'fat_g': float(row['fat_g']) if pd.notna(row['fat_g']) else None,
                    'description': row['description'] if pd.notna(row['description']) else None
                }
                
                logger.info(f"✅ Matched '{dish_name}' to '{row['dish_name']}' (confidence: {confidence}%)")
                return result
            
            else:
                logger.warning(f"⚠️ No good match found for '{dish_name}' (best score: {best_match[1] if best_match else 0})")
                return None
                
        except Exception as e:
            logger.error(f"❌ Fuzzy matching failed for '{dish_name}': {e}")
            return None
    
    def get_calories(self, dish_name: str) -> int:
        """
        Get calories for dish with fuzzy matching fallback
        
        Args:
            dish_name: Name of dish
            
        Returns:
            Calories per serving, or estimated value if not found
        """
        match = self.fuzzy_match_dish(dish_name)
        
        if match:
            return match['calories']
        else:
            # Fallback estimation based on dish type
            estimated_calories = self._estimate_calories(dish_name)
            logger.info(f"⚠️ Using estimated calories for '{dish_name}': {estimated_calories}")
            return estimated_calories
    
    def get_dish_info(self, dish_name: str) -> Dict[str, Any]:
        """
        Get complete dish information
        
        Args:
            dish_name: Name of dish
            
        Returns:
            Complete dish information dictionary
        """
        match = self.fuzzy_match_dish(dish_name)
        
        if match:
            return match
        else:
            # Return estimated data
            return {
                'original_query': dish_name,
                'matched_name': dish_name,
                'confidence': 0,
                'calories': self._estimate_calories(dish_name),
                'meal_type': 'any',
                'protein_g': None,
                'carbs_g': None,
                'fat_g': None,
                'description': f"Estimated nutritional information for {dish_name}"
            }
    
    def search_dishes(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for dishes matching query
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching dishes
        """
        if self.df is None:
            return []
        
        try:
            # Get fuzzy matches
            matches = process.extract(
                query.lower(),
                self.dish_names,
                scorer=fuzz.partial_ratio,
                limit=limit
            )
            
            results = []
            for match_name, score in matches:
                if score >= 50:  # Lower threshold for search
                    row = self.df[self.df['dish_name'].str.lower() == match_name].iloc[0]
                    results.append({
                        'name': row['dish_name'],
                        'calories': int(row['calories']),
                        'meal_type': row['meal_type'],
                        'description': row['description'] if pd.notna(row['description']) else None,
                        'match_score': score
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Dish search failed: {e}")
            return []
    
    def get_all_dishes(self) -> List[Dict[str, Any]]:
        """Get all dishes in the database"""
        if self.df is None:
            return []
        
        try:
            return [
                {
                    'name': row['dish_name'],
                    'calories': int(row['calories']),
                    'meal_type': row['meal_type'],
                    'description': row['description'] if pd.notna(row['description']) else None
                }
                for _, row in self.df.iterrows()
            ]
        except Exception as e:
            logger.error(f"❌ Failed to get all dishes: {e}")
            return []
    
    def _estimate_calories(self, dish_name: str) -> int:
        """
        Estimate calories based on dish name patterns
        
        Args:
            dish_name: Name of dish
            
        Returns:
            Estimated calories
        """
        dish_lower = dish_name.lower()
        
        # Simple heuristics for calorie estimation
        if any(word in dish_lower for word in ['paratha', 'naan', 'kulcha', 'bhatura']):
            return 300  # Bread items
        elif any(word in dish_lower for word in ['rice', 'biryani', 'pulao']):
            return 250  # Rice dishes
        elif any(word in dish_lower for word in ['dal', 'lentil']):
            return 180  # Lentil dishes
        elif any(word in dish_lower for word in ['chicken', 'mutton', 'meat']):
            return 350  # Meat dishes
        elif any(word in dish_lower for word in ['paneer', 'cheese']):
            return 280  # Paneer dishes
        elif any(word in dish_lower for word in ['sabzi', 'vegetable', 'curry']):
            return 150  # Vegetable dishes
        elif any(word in dish_lower for word in ['samosa', 'pakora', 'snack']):
            return 200  # Snacks
        elif any(word in dish_lower for word in ['sweet', 'dessert', 'halwa']):
            return 400  # Sweets
        else:
            return 250  # Default estimate
    
    def reload_data(self):
        """Reload nutrition data from CSV"""
        logger.info("🔄 Reloading nutrition data...")
        self._load_nutrition_data()


# Global nutrition service instance
nutrition_service = NutritionService()