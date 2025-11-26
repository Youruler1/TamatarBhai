"""
Chart generation service using matplotlib
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import logging
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np

logger = logging.getLogger(__name__)


class ChartService:
    """Service for generating charts and visualizations"""
    
    def __init__(self, charts_dir: str = "data/images"):
        self.charts_dir = Path(charts_dir)
        self.charts_dir.mkdir(parents=True, exist_ok=True)
        
        # Set style
        plt.style.use('default')
        sns.set_palette("husl")
    
    async def generate_weekly_chart(self, meal_data: List[Dict[str, Any]], 
                                  start_date: str, end_date: str) -> str:
        """
        Generate weekly calorie consumption chart
        
        Args:
            meal_data: List of meal consumption data
            start_date: Start date string (YYYY-MM-DD)
            end_date: End date string (YYYY-MM-DD)
            
        Returns:
            Path to generated chart image
        """
        try:
            # Create filename
            timestamp = int(datetime.now().timestamp())
            filename = f"weekly_chart_{start_date}_{end_date}_{timestamp}.png"
            filepath = self.charts_dir / filename
            
            # Process data
            if not meal_data:
                # Create empty chart
                return await self._create_empty_chart(filepath, start_date, end_date)
            
            # Convert to DataFrame
            df = pd.DataFrame(meal_data)
            df['consumed_at'] = pd.to_datetime(df['consumed_at'])
            df['date'] = df['consumed_at'].dt.date
            
            # Group by date and sum calories
            daily_calories = df.groupby('date')['calories'].sum().reset_index()
            
            # Create date range for the week
            start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            date_range = pd.date_range(start=start_dt, end=end_dt, freq='D')
            date_df = pd.DataFrame({'date': date_range.date})
            
            # Merge with actual data
            chart_data = date_df.merge(daily_calories, on='date', how='left')
            chart_data['calories'] = chart_data['calories'].fillna(0)
            chart_data['day_name'] = pd.to_datetime(chart_data['date']).dt.strftime('%a')
            
            # Create the chart
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Bar chart
            bars = ax.bar(chart_data['day_name'], chart_data['calories'], 
                         color='#ff6b6b', alpha=0.8, edgecolor='#d63031', linewidth=1)
            
            # Customize chart
            ax.set_title(f'Weekly Calorie Consumption\n{start_date} to {end_date}', 
                        fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Day of Week', fontsize=12, fontweight='bold')
            ax.set_ylabel('Calories', fontsize=12, fontweight='bold')
            
            # Add value labels on bars
            for bar, calories in zip(bars, chart_data['calories']):
                if calories > 0:
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                           f'{int(calories)}', ha='center', va='bottom', fontweight='bold')
            
            # Add average line
            avg_calories = chart_data['calories'].mean()
            if avg_calories > 0:
                ax.axhline(y=avg_calories, color='#00b894', linestyle='--', 
                          linewidth=2, alpha=0.8, label=f'Average: {int(avg_calories)} cal')
                ax.legend()
            
            # Styling
            ax.grid(True, alpha=0.3, axis='y')
            ax.set_ylim(0, max(chart_data['calories'].max() * 1.1, 100))
            
            # Remove top and right spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            plt.tight_layout()
            
            # Save chart
            plt.savefig(filepath, dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            plt.close()
            
            chart_url = f"/data/images/{filename}"
            logger.info(f"✅ Generated weekly chart: {chart_url}")
            return chart_url
            
        except Exception as e:
            logger.error(f"❌ Failed to generate weekly chart: {e}")
            return await self._create_error_chart()
    
    async def generate_meal_distribution_chart(self, meal_data: List[Dict[str, Any]]) -> str:
        """
        Generate meal type distribution pie chart
        
        Args:
            meal_data: List of meal consumption data
            
        Returns:
            Path to generated chart image
        """
        try:
            if not meal_data:
                return await self._create_error_chart()
            
            # Create filename
            timestamp = int(datetime.now().timestamp())
            filename = f"meal_distribution_{timestamp}.png"
            filepath = self.charts_dir / filename
            
            # Process data
            df = pd.DataFrame(meal_data)
            meal_calories = df.groupby('meal_type')['calories'].sum()
            
            # Create pie chart
            fig, ax = plt.subplots(figsize=(8, 8))
            
            colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57']
            wedges, texts, autotexts = ax.pie(meal_calories.values, 
                                             labels=meal_calories.index,
                                             autopct='%1.1f%%',
                                             colors=colors,
                                             startangle=90,
                                             explode=[0.05] * len(meal_calories))
            
            ax.set_title('Calorie Distribution by Meal Type', 
                        fontsize=16, fontweight='bold', pad=20)
            
            # Enhance text
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            plt.tight_layout()
            
            # Save chart
            plt.savefig(filepath, dpi=150, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            plt.close()
            
            chart_url = f"/data/images/{filename}"
            logger.info(f"✅ Generated meal distribution chart: {chart_url}")
            return chart_url
            
        except Exception as e:
            logger.error(f"❌ Failed to generate meal distribution chart: {e}")
            return await self._create_error_chart()
    
    async def _create_empty_chart(self, filepath: Path, start_date: str, end_date: str) -> str:
        """Create chart for empty data"""
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Create empty bars for each day
            start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            date_range = pd.date_range(start=start_dt, end=end_dt, freq='D')
            day_names = [d.strftime('%a') for d in date_range]
            
            ax.bar(day_names, [0] * len(day_names), color='#ddd', alpha=0.5)
            
            ax.set_title(f'Weekly Calorie Consumption\n{start_date} to {end_date}\n(No data recorded)', 
                        fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Day of Week', fontsize=12, fontweight='bold')
            ax.set_ylabel('Calories', fontsize=12, fontweight='bold')
            ax.set_ylim(0, 100)
            
            # Add message
            ax.text(0.5, 0.5, 'No meal data recorded for this period', 
                   transform=ax.transAxes, ha='center', va='center',
                   fontsize=14, style='italic', color='#666')
            
            ax.grid(True, alpha=0.3, axis='y')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            plt.tight_layout()
            plt.savefig(filepath, dpi=150, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            plt.close()
            
            return f"/data/images/{filepath.name}"
            
        except Exception as e:
            logger.error(f"❌ Failed to create empty chart: {e}")
            return await self._create_error_chart()
    
    async def _create_error_chart(self) -> str:
        """Create error placeholder chart"""
        try:
            filename = "chart_error_placeholder.png"
            filepath = self.charts_dir / filename
            
            fig, ax = plt.subplots(figsize=(8, 6))
            
            ax.text(0.5, 0.5, '📊 Chart Generation Error\nPlease try again later', 
                   transform=ax.transAxes, ha='center', va='center',
                   fontsize=16, fontweight='bold', color='#e74c3c')
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            plt.tight_layout()
            plt.savefig(filepath, dpi=150, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            plt.close()
            
            return f"/data/images/{filename}"
            
        except Exception as e:
            logger.error(f"❌ Failed to create error chart: {e}")
            return "/data/images/default_placeholder.png"


# Global chart service instance
chart_service = ChartService()