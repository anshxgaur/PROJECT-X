"""
Obsidian Vault Reader - Extracts billing data from markdown files
"""

import os
import yaml
import re
from pathlib import Path
from typing import Dict, List, Optional, Any

class ObsidianReader:
    """Reads and parses Obsidian markdown files with YAML frontmatter"""
    
    def __init__(self, vault_path: str):
        """
        Initialize Obsidian reader with vault path
        
        Args:
            vault_path: Path to Obsidian vault root directory
        """
        self.vault_path = Path(vault_path)
        if not self.vault_path.exists():
            raise FileNotFoundError(f"Vault path does not exist: {vault_path}")
    
    def read_frontmatter(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract YAML frontmatter from markdown file
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            Dictionary with frontmatter data
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file starts with ---
            if not content.startswith('---'):
                return {}
            
            # Extract frontmatter
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if not match:
                return {}
            
            frontmatter_str = match.group(1)
            frontmatter = yaml.safe_load(frontmatter_str)
            return frontmatter or {}
        except Exception as e:
            print(f"Error reading frontmatter from {file_path}: {e}")
            return {}
    
    def read_markdown_content(self, file_path: Path) -> str:
        """
        Extract markdown content (without frontmatter)
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            Markdown content string
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove frontmatter
            if content.startswith('---'):
                match = re.match(r'^---\n.*?\n---\n', content, re.DOTALL)
                if match:
                    return content[match.end():]
            
            return content
        except Exception as e:
            print(f"Error reading markdown from {file_path}: {e}")
            return ""
    
    def get_bilty_files(self) -> List[Path]:
        """
        Get all bilty markdown files from vault
        
        Returns:
            List of Path objects for bilty files
        """
        bilties_dir = self.vault_path / "Bilties"
        if not bilties_dir.exists():
            return []
        
        return sorted(bilties_dir.glob("*.md"))
    
    def parse_bilty(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Parse complete bilty from markdown file
        
        Args:
            file_path: Path to bilty markdown file
            
        Returns:
            Dictionary with parsed bilty data or None on error
        """
        frontmatter = self.read_frontmatter(file_path)
        if not frontmatter:
            return None
        
        # Clean up numeric fields
        bilty = {
            'bilty_id': frontmatter.get('bilty_id'),
            'bilty_number': frontmatter.get('bilty_number'),
            'status': frontmatter.get('status', 'pending'),
            'sender_name': frontmatter.get('sender_name'),
            'receiver_name': frontmatter.get('receiver_name'),
            'origin_city': frontmatter.get('origin_city'),
            'destination_city': frontmatter.get('destination_city'),
            'distance_km': float(frontmatter.get('distance_km') or 0),
            'weight_kg': float(frontmatter.get('weight_kg') or 0),
            'goods_type': frontmatter.get('goods_type'),
            'goods_value': frontmatter.get('goods_value', 0),
            'rate_per_km': float(frontmatter.get('rate_per_km') or 0),
            'total_amount': float(re.sub(r'[^\d.]', '', str(frontmatter.get('total_amount', 0)))),
            'payment_status': frontmatter.get('payment_status', 'pending'),
            'priority': frontmatter.get('priority', 'medium'),
            'weather_conditions': frontmatter.get('weather_conditions', 'clear'),
            'highway_percentage': float(frontmatter.get('highway_percentage') or 0),
            'actual_delay_hours': float(frontmatter.get('actual_delay_hours') or 0),
            'scheduled_duration_hours': float(frontmatter.get('scheduled_duration_hours') or 0),
        }
        
        return bilty
    
    def get_all_bilties(self) -> List[Dict[str, Any]]:
        """
        Get all parsed bilties from vault
        
        Returns:
            List of dictionaries with bilty data
        """
        bilties = []
        for file_path in self.get_bilty_files():
            bilty = self.parse_bilty(file_path)
            if bilty:
                bilties.append(bilty)
        
        return bilties
    
    def get_bilty_features(self, bilty: Dict[str, Any]) -> Dict[str, float]:
        """
        Convert bilty data to ML features
        
        Args:
            bilty: Parsed bilty dictionary
            
        Returns:
            Dictionary with feature names and values
        """
        # Convert categorical to numeric
        priority_map = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
        payment_map = {'pending': 0, 'partial': 1, 'paid': 2}
        weather_map = {'clear': 0, 'rain': 1, 'monsoon': 2, 'fog': 1, 'snow': 2}
        
        features = {
            'distance_km': bilty['distance_km'],
            'weight_kg': bilty['weight_kg'],
            'rate_per_km': bilty['rate_per_km'],
            'total_amount': bilty['total_amount'],
            'priority_score': priority_map.get(bilty['priority'].lower(), 2),
            'payment_status_score': payment_map.get(bilty['payment_status'].lower(), 0),
            'weather_score': weather_map.get(bilty['weather_conditions'].lower(), 0),
            'highway_percentage': bilty['highway_percentage'],
            'goods_value': float(re.sub(r'[^\d.]', '', str(bilty['goods_value'])) or 0),
        }
        
        return features
    
    def get_training_data(self) -> tuple:
        """
        Get training features and delays from all bilties
        
        Returns:
            Tuple of (features_list, delays_list)
        """
        import pandas as pd
        
        all_bilties = self.get_all_bilties()
        features_list = []
        delays_list = []
        
        for bilty in all_bilties:
            if bilty['actual_delay_hours'] >= 0:  # Valid data
                features = self.get_bilty_features(bilty)
                features_list.append(features)
                delays_list.append(bilty['actual_delay_hours'])
        
        if not features_list:
            return pd.DataFrame(), pd.Series()
        
        df_features = pd.DataFrame(features_list)
        series_delays = pd.Series(delays_list)
        
        return df_features, series_delays


def load_obsidian_bilties(vault_path: str) -> List[Dict[str, Any]]:
    """
    Convenience function to load all bilties from Obsidian vault
    
    Args:
        vault_path: Path to Obsidian vault
        
    Returns:
        List of bilty dictionaries
    """
    try:
        reader = ObsidianReader(vault_path)
        return reader.get_all_bilties()
    except Exception as e:
        print(f"Error loading Obsidian bilties: {e}")
        return []
