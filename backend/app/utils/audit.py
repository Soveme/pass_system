import json
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, Any

from app.models.audit_log import AuditLog
from app.models.user import User

class AuditLogger:
    """Log all operations for compliance (ФЗ-152, GDPR)"""
    
    @staticmethod
    async def log_action(
        db: AsyncSession,
        user_id: Optional[int],
        action: str,
        entity_type: str,
        entity_id: str,
        changes: Optional[dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """Log an action"""
        
        log_entry = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            changes=json.dumps(changes) if changes else None,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.utcnow()
        )
        
        db.add(log_entry)
        await db.commit()
        
        # Log to console as well
        print(f"[AUDIT] {action} - {entity_type}:{entity_id} by User:{user_id} at {datetime.utcnow()}")
        if changes:
            print(f"[AUDIT_DETAILS] Changes: {json.dumps(changes, indent=2)}")
        if ip_address:
            print(f"[AUDIT_IP] {ip_address}")
    
    @staticmethod
    async def get_user_logs(
        db: AsyncSession,
        user_id: int,
        limit: int = 100
    ):
        """Get all audit logs for a user"""
        result = await db.execute(
            select(AuditLog)
            .where(AuditLog.user_id == user_id)
            .order_by(AuditLog.timestamp.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_entity_logs(
        db: AsyncSession,
        entity_type: str,
        entity_id: str,
        limit: int = 100
    ):
        """Get all logs for a specific entity"""
        result = await db.execute(
            select(AuditLog)
            .where(
                AuditLog.entity_type == entity_type,
                AuditLog.entity_id == entity_id
            )
            .order_by(AuditLog.timestamp.desc())
            .limit(limit)
        )
        return result.scalars().all()

async def audit_create(db: AsyncSession, user_id: int, entity_type: str, entity_id: str, data: dict):
    """Log CREATE action"""
    await AuditLogger.log_action(
        db, user_id, "CREATE", entity_type, entity_id, {"created": data}
    )

async def audit_update(db: AsyncSession, user_id: int, entity_type: str, entity_id: str, before: dict, after: dict):
    """Log UPDATE action"""
    await AuditLogger.log_action(
        db, user_id, "UPDATE", entity_type, entity_id, {"before": before, "after": after}
    )

async def audit_delete(db: AsyncSession, user_id: int, entity_type: str, entity_id: str, data: dict):
    """Log DELETE action"""
    await AuditLogger.log_action(
        db, user_id, "DELETE", entity_type, entity_id, {"deleted": data}
    )

async def audit_read(db: AsyncSession, user_id: int, entity_type: str, entity_id: str):
    """Log READ action"""
    await AuditLogger.log_action(
        db, user_id, "READ", entity_type, entity_id
    )
