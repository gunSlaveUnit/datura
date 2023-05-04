from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.api.v1.schemas.review import ReviewCreateSchema
from server.src.core.models.review import Review
from server.src.core.models.user import User
from server.src.core.settings import Tags, REVIEWS_ROUTER_PREFIX
from server.src.core.utils.auth import GetCurrentUser
from server.src.core.utils.db import get_db

router = APIRouter(prefix=REVIEWS_ROUTER_PREFIX, tags=[Tags.REVIEWS])


@router.get('/')
async def items(game_id: int,
                db=Depends(get_db)):
    return db.query(Review).filter(Review.game_id == game_id).all()


@router.post('/')
async def create(game_id: int,
                 new_review_data: ReviewCreateSchema,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(GetCurrentUser())):
    review = Review(**vars(new_review_data))
    review.game_id = game_id
    review.user_id = current_user.id

    return await Review.create(db, review)
