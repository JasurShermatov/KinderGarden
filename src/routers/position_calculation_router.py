from fastapi import APIRouter, HTTPException, status, Depends

from src.models import User
from src.schemas.meal_schemas import MealListQuery
from src.schemas.portion_calculation_schema import (
    PortionCalculationListSchema,
    PortionCalculationReadSchema,
)
from src.services.portion_calculation_controller import PortionCalculationController
from src.utils.security import get_current_user

router = APIRouter(
    prefix="/portion-calculate",
    tags=["portion-calculate"],
)


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=PortionCalculationListSchema
)
async def get_portion_count(
    payload: MealListQuery = Depends(),
    current_user: User = Depends(get_current_user),
    portion_calculation_controller: PortionCalculationController = Depends(),
) -> PortionCalculationListSchema:
    if current_user.role_id not in (1, 2, 3, 4):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await portion_calculation_controller.get_portion_count(payload=payload)


@router.get(
    "/{meal_id}",
    status_code=status.HTTP_200_OK,
    response_model=PortionCalculationReadSchema,
)
async def get_portion_count_by_id(
    meal_id: int,
    current_user: User = Depends(get_current_user),
    portion_calculation_controller: PortionCalculationController = Depends(),
) -> PortionCalculationReadSchema:
    if current_user.role_id not in (1, 2, 3, 4):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await portion_calculation_controller.get_portion_count_by_id(
        meal_id=meal_id,
    )
