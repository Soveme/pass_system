from .auth import router as auth_router
from .passes import router as passes_router
from .scan import router as scan_router
from .admin import router as admin_router
from .visits import router as visits_router

__all__ = ["auth_router", "passes_router", "scan_router", "admin_router", "visits_router"]
