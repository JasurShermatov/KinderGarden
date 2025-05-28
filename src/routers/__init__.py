from fastapi import APIRouter

from .authentication_router import router as auth_router
from .user_router import router as user_router
from .meal_router import router as meal_router
from .ingredients_router import router as ingredients_router
from .units_router import router as units_router
from .alerts_router import router as alerts_router
from .position_calculation_router import (
    router as position_calculation_router,
)
from .report_router import router as report_router
api_v1_router = APIRouter()

api_v1_router.include_router(auth_router, tags=["Authentication"])
api_v1_router.include_router(user_router, tags=["Users"])
api_v1_router.include_router(meal_router, tags=["Meals"])
api_v1_router.include_router(ingredients_router, tags=["Ingredients"])
api_v1_router.include_router(units_router, tags=["Units"])
api_v1_router.include_router(alerts_router, tags=["Alerts"])
api_v1_router.include_router(
    position_calculation_router, tags=["Position Calculation"]
)
api_v1_router.include_router(report_router, tags=["Reports"])


__all__ = ["api_v1_router"]
