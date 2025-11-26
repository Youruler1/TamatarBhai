"""
Caching service for storing generated content
"""

import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import Cache, get_db

logger = logging.getLogger(__name__)


class CacheService:
    """Service for managing cached content"""
    
    def __init__(self, default_ttl_hours: int = 24):
        self.default_ttl_hours = default_ttl_hours
    
    async def get_cached_preview(self, dish_name: str, db: Session) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached preview data for a dish
        
        Args:
            dish_name: Name of the dish
            db: Database session
            
        Returns:
            Cached preview data or None if not found/expired
        """
        try:
            # Normalize dish name
            normalized_name = dish_name.lower().strip()
            
            # Query cache
            cache_entry = db.query(Cache).filter(
                Cache.dish_name == normalized_name,
                Cache.cache_type == 'preview'
            ).first()
            
            if not cache_entry:
                logger.info(f"📭 No cache entry found for '{dish_name}'")
                return None
            
            # Check if expired
            if cache_entry.expires_at and cache_entry.expires_at < datetime.utcnow():
                logger.info(f"⏰ Cache expired for '{dish_name}', removing...")
                db.delete(cache_entry)
                db.commit()
                return None
            
            # Parse and return cached data
            cached_data = json.loads(cache_entry.cache_data)
            logger.info(f"✅ Cache hit for '{dish_name}'")
            return cached_data
            
        except Exception as e:
            logger.error(f"❌ Failed to retrieve cache for '{dish_name}': {e}")
            return None
    
    async def cache_preview(self, dish_name: str, preview_data: Dict[str, Any], 
                          db: Session, ttl_hours: Optional[int] = None) -> bool:
        """
        Cache preview data for a dish
        
        Args:
            dish_name: Name of the dish
            preview_data: Preview data to cache
            db: Database session
            ttl_hours: Time to live in hours (uses default if None)
            
        Returns:
            True if cached successfully, False otherwise
        """
        try:
            # Normalize dish name
            normalized_name = dish_name.lower().strip()
            
            # Calculate expiry time
            ttl = ttl_hours or self.default_ttl_hours
            expires_at = datetime.utcnow() + timedelta(hours=ttl)
            
            # Check if entry already exists
            existing_entry = db.query(Cache).filter(
                Cache.dish_name == normalized_name,
                Cache.cache_type == 'preview'
            ).first()
            
            if existing_entry:
                # Update existing entry
                existing_entry.cache_data = json.dumps(preview_data)
                existing_entry.expires_at = expires_at
                existing_entry.created_at = datetime.utcnow()
                logger.info(f"🔄 Updated cache for '{dish_name}'")
            else:
                # Create new entry
                cache_entry = Cache(
                    dish_name=normalized_name,
                    cache_type='preview',
                    cache_data=json.dumps(preview_data),
                    expires_at=expires_at
                )
                db.add(cache_entry)
                logger.info(f"💾 Cached preview for '{dish_name}'")
            
            db.commit()
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to cache preview for '{dish_name}': {e}")
            db.rollback()
            return False
    
    async def get_cached_image(self, dish_name: str, db: Session) -> Optional[str]:
        """
        Get cached image URL for a dish
        
        Args:
            dish_name: Name of the dish
            db: Database session
            
        Returns:
            Image URL or None if not cached
        """
        try:
            normalized_name = dish_name.lower().strip()
            
            cache_entry = db.query(Cache).filter(
                Cache.dish_name == normalized_name,
                Cache.cache_type == 'image'
            ).first()
            
            if cache_entry and (not cache_entry.expires_at or cache_entry.expires_at > datetime.utcnow()):
                image_data = json.loads(cache_entry.cache_data)
                return image_data.get('image_url')
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to get cached image for '{dish_name}': {e}")
            return None
    
    async def cache_image(self, dish_name: str, image_url: str, 
                         db: Session, ttl_hours: Optional[int] = None) -> bool:
        """
        Cache image URL for a dish
        
        Args:
            dish_name: Name of the dish
            image_url: URL of the generated image
            db: Database session
            ttl_hours: Time to live in hours
            
        Returns:
            True if cached successfully
        """
        try:
            normalized_name = dish_name.lower().strip()
            ttl = ttl_hours or (self.default_ttl_hours * 7)  # Images last longer
            expires_at = datetime.utcnow() + timedelta(hours=ttl)
            
            image_data = {
                'image_url': image_url,
                'generated_at': datetime.utcnow().isoformat()
            }
            
            # Check for existing entry
            existing_entry = db.query(Cache).filter(
                Cache.dish_name == normalized_name,
                Cache.cache_type == 'image'
            ).first()
            
            if existing_entry:
                existing_entry.cache_data = json.dumps(image_data)
                existing_entry.expires_at = expires_at
                existing_entry.created_at = datetime.utcnow()
            else:
                cache_entry = Cache(
                    dish_name=normalized_name,
                    cache_type='image',
                    cache_data=json.dumps(image_data),
                    expires_at=expires_at
                )
                db.add(cache_entry)
            
            db.commit()
            logger.info(f"💾 Cached image for '{dish_name}': {image_url}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to cache image for '{dish_name}': {e}")
            db.rollback()
            return False
    
    async def get_cached_captions(self, dish_name: str, db: Session) -> Optional[Dict[str, str]]:
        """
        Get cached captions for a dish
        
        Args:
            dish_name: Name of the dish
            db: Database session
            
        Returns:
            Dictionary with bhai and formal captions or None
        """
        try:
            normalized_name = dish_name.lower().strip()
            
            cache_entry = db.query(Cache).filter(
                Cache.dish_name == normalized_name,
                Cache.cache_type == 'captions'
            ).first()
            
            if cache_entry and (not cache_entry.expires_at or cache_entry.expires_at > datetime.utcnow()):
                return json.loads(cache_entry.cache_data)
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to get cached captions for '{dish_name}': {e}")
            return None
    
    async def cache_captions(self, dish_name: str, captions: Dict[str, str], 
                           db: Session, ttl_hours: Optional[int] = None) -> bool:
        """
        Cache captions for a dish
        
        Args:
            dish_name: Name of the dish
            captions: Dictionary with bhai and formal captions
            db: Database session
            ttl_hours: Time to live in hours
            
        Returns:
            True if cached successfully
        """
        try:
            normalized_name = dish_name.lower().strip()
            ttl = ttl_hours or self.default_ttl_hours
            expires_at = datetime.utcnow() + timedelta(hours=ttl)
            
            # Check for existing entry
            existing_entry = db.query(Cache).filter(
                Cache.dish_name == normalized_name,
                Cache.cache_type == 'captions'
            ).first()
            
            if existing_entry:
                existing_entry.cache_data = json.dumps(captions)
                existing_entry.expires_at = expires_at
                existing_entry.created_at = datetime.utcnow()
            else:
                cache_entry = Cache(
                    dish_name=normalized_name,
                    cache_type='captions',
                    cache_data=json.dumps(captions),
                    expires_at=expires_at
                )
                db.add(cache_entry)
            
            db.commit()
            logger.info(f"💾 Cached captions for '{dish_name}'")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to cache captions for '{dish_name}': {e}")
            db.rollback()
            return False
    
    async def invalidate_cache(self, dish_name: str, db: Session, 
                             cache_type: Optional[str] = None) -> int:
        """
        Clear cache for a specific dish
        
        Args:
            dish_name: Name of the dish
            db: Database session
            cache_type: Specific cache type to clear (None for all)
            
        Returns:
            Number of cache entries deleted
        """
        try:
            normalized_name = dish_name.lower().strip()
            
            query = db.query(Cache).filter(Cache.dish_name == normalized_name)
            
            if cache_type:
                query = query.filter(Cache.cache_type == cache_type)
            
            deleted_count = query.delete()
            db.commit()
            
            logger.info(f"🗑️ Cleared {deleted_count} cache entries for '{dish_name}'")
            return deleted_count
            
        except Exception as e:
            logger.error(f"❌ Failed to clear cache for '{dish_name}': {e}")
            db.rollback()
            return 0
    
    async def cleanup_expired_cache(self, db: Session) -> int:
        """
        Remove all expired cache entries
        
        Args:
            db: Database session
            
        Returns:
            Number of expired entries removed
        """
        try:
            deleted_count = db.query(Cache).filter(
                Cache.expires_at < datetime.utcnow()
            ).delete()
            
            db.commit()
            
            if deleted_count > 0:
                logger.info(f"🧹 Cleaned up {deleted_count} expired cache entries")
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"❌ Failed to cleanup expired cache: {e}")
            db.rollback()
            return 0
    
    def get_cache_stats(self, db: Session) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Args:
            db: Database session
            
        Returns:
            Dictionary with cache statistics
        """
        try:
            total_entries = db.query(Cache).count()
            
            # Count by type
            preview_count = db.query(Cache).filter(Cache.cache_type == 'preview').count()
            image_count = db.query(Cache).filter(Cache.cache_type == 'image').count()
            caption_count = db.query(Cache).filter(Cache.cache_type == 'captions').count()
            
            # Count expired
            expired_count = db.query(Cache).filter(
                Cache.expires_at < datetime.utcnow()
            ).count()
            
            return {
                'total_entries': total_entries,
                'by_type': {
                    'preview': preview_count,
                    'image': image_count,
                    'captions': caption_count
                },
                'expired_entries': expired_count,
                'active_entries': total_entries - expired_count
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get cache stats: {e}")
            return {}


# Global cache service instance
cache_service = CacheService()