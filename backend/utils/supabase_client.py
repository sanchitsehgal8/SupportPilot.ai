"""Supabase Client - database connection and utilities"""
from supabase import create_client, Client


class SupabaseClient:
    """Manages Supabase database connection"""
    
    _instance = None
    
    def __new__(cls, url: str = None, key: str = None):
        """Singleton pattern for database connection"""
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
            if url and key:
                cls._instance.client = create_client(url, key)
        return cls._instance
    
    def get_client(self) -> Client:
        """Get Supabase client"""
        if not hasattr(self, 'client') or self.client is None:
            raise Exception("Supabase client not initialized. Call init_client() first.")
        return self.client
    
    def init_client(self, url: str, key: str):
        """Initialize Supabase client"""
        self.client = create_client(url, key)
    
    def health_check(self) -> bool:
        """Check if database connection is healthy"""
        try:
            result = self.client.table('users').select('count').execute()
            return True
        except Exception as e:
            print(f"Health check failed: {e}")
            return False
    
    @staticmethod
    def get_instance(url: str = None, key: str = None) -> 'SupabaseClient':
        """Get singleton instance"""
        return SupabaseClient(url, key)
