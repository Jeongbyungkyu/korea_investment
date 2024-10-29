from datetime import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class Token:
    access_token: str
    issued_at: datetime
    expires_in: int = 14400  # 4 hours in seconds
    
    def is_expired(self) -> bool:
        """Check if token is expired (older than 4 hours)"""
        if not self.issued_at:
            return True
        
        elapsed = (datetime.now() - self.issued_at).total_seconds()
        return elapsed >= self.expires_in
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Token':
        """Create Token instance from dictionary"""
        return cls(
            access_token=data['access_token'],
            issued_at=datetime.fromisoformat(data['issued_at']),
            expires_in=data.get('expires_in', 14400)
        )
    
    def to_dict(self) -> dict:
        """Convert Token instance to dictionary"""
        return {
            'access_token': self.access_token,
            'issued_at': self.issued_at.isoformat(),
            'expires_in': self.expires_in
        }