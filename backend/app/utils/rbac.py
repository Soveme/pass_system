from enum import Enum
from typing import List, Optional
from app.models.user import UserRole

class Permission(str, Enum):
    # Pass management
    CREATE_PASS = "create_pass"
    VIEW_PASS = "view_pass"
    UPDATE_PASS = "update_pass"
    REVOKE_PASS = "revoke_pass"
    
    # Scanning
    SCAN_PASS = "scan_pass"
    
    # Admin operations
    VIEW_AUDIT_LOG = "view_audit_log"
    EXPORT_REPORT = "export_report"
    MANAGE_USERS = "manage_users"
    CONFIGURE_SYSTEM = "configure_system"
    
    # Data access
    VIEW_SENSITIVE_DATA = "view_sensitive_data"
    DELETE_DATA = "delete_data"

# Role-based permissions mapping
ROLE_PERMISSIONS = {
    UserRole.GUEST: [
        Permission.VIEW_PASS,
    ],
    UserRole.EMPLOYEE: [
        Permission.VIEW_PASS,
        Permission.SCAN_PASS,
    ],
    UserRole.GUARD: [
        Permission.SCAN_PASS,
        Permission.VIEW_PASS,
    ],
    UserRole.HR: [
        Permission.CREATE_PASS,
        Permission.VIEW_PASS,
        Permission.UPDATE_PASS,
        Permission.VIEW_AUDIT_LOG,
    ],
    UserRole.ADMIN: [
        Permission.CREATE_PASS,
        Permission.VIEW_PASS,
        Permission.UPDATE_PASS,
        Permission.REVOKE_PASS,
        Permission.SCAN_PASS,
        Permission.VIEW_AUDIT_LOG,
        Permission.EXPORT_REPORT,
        Permission.MANAGE_USERS,
        Permission.VIEW_SENSITIVE_DATA,
    ],
    UserRole.IT_SPECIALIST: [
        Permission.VIEW_AUDIT_LOG,
        Permission.VIEW_SENSITIVE_DATA,
        Permission.CONFIGURE_SYSTEM,
        Permission.DELETE_DATA,
    ],
    UserRole.MANAGEMENT: [
        Permission.VIEW_PASS,
        Permission.EXPORT_REPORT,
        Permission.VIEW_AUDIT_LOG,
    ]
}

def check_permission(role: UserRole, permission: Permission) -> bool:
    """Check if role has permission"""
    permissions = ROLE_PERMISSIONS.get(role, [])
    return permission in permissions

def get_role_permissions(role: UserRole) -> List[Permission]:
    """Get all permissions for a role"""
    return ROLE_PERMISSIONS.get(role, [])

class PermissionChecker:
    """Helper class for permission checks"""
    
    @staticmethod
    def can_view_pass(role: UserRole) -> bool:
        return check_permission(role, Permission.VIEW_PASS)
    
    @staticmethod
    def can_create_pass(role: UserRole) -> bool:
        return check_permission(role, Permission.CREATE_PASS)
    
    @staticmethod
    def can_update_pass(role: UserRole) -> bool:
        return check_permission(role, Permission.UPDATE_PASS)
    
    @staticmethod
    def can_scan_pass(role: UserRole) -> bool:
        return check_permission(role, Permission.SCAN_PASS)
    
    @staticmethod
    def can_view_audit_logs(role: UserRole) -> bool:
        return check_permission(role, Permission.VIEW_AUDIT_LOG)
    
    @staticmethod
    def can_manage_users(role: UserRole) -> bool:
        return check_permission(role, Permission.MANAGE_USERS)
