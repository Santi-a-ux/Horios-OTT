from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.deps import get_current_user, require_roles
from app.db.database import get_db
from app.db.models import User, UserRole, Video, VideoStatus
from app.mux.service import MuxService
from app.videos.schemas import VideoCreateRequest, VideoResponse, PlayResponse

router = APIRouter(prefix="/videos", tags=["videos"])


@router.post("", response_model=VideoResponse, status_code=201)
def create_video(
    payload: VideoCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
):
    mux_service = MuxService()
    try:
        mux_asset_id, playback_id = mux_service.create_asset(payload.input_url)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Mux asset creation failed",
        )

    video = Video(
        title=payload.title,
        description=payload.description,
        is_premium=payload.is_premium,
        mux_asset_id=mux_asset_id,
        playback_id=playback_id,
        status=VideoStatus.PROCESSING.value,
        created_by=current_user.id,
    )
    db.add(video)
    db.commit()
    db.refresh(video)

    return VideoResponse(
        id=video.id,
        title=video.title,
        description=video.description,
        is_premium=video.is_premium,
        mux_asset_id=video.mux_asset_id,
        playback_id=video.playback_id,
        status=video.status,
        created_by=video.created_by,
        created_at=video.created_at,
    )


@router.get("", response_model=list[VideoResponse])
def list_videos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Video)
    if current_user.role == UserRole.USER:
        query = query.filter(Video.is_premium.is_(False))
    videos = query.order_by(Video.created_at.desc()).all()

    return [
        VideoResponse(
            id=v.id,
            title=v.title,
            description=v.description,
            is_premium=v.is_premium,
            mux_asset_id=v.mux_asset_id,
            playback_id=v.playback_id,
            status=v.status,
            created_by=v.created_by,
            created_at=v.created_at,
        )
        for v in videos
    ]


@router.get("/{video_id}", response_model=VideoResponse)
def get_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    if video.is_premium and current_user.role == UserRole.USER:
        raise HTTPException(status_code=403, detail="Premium content")

    return VideoResponse(
        id=video.id,
        title=video.title,
        description=video.description,
        is_premium=video.is_premium,
        mux_asset_id=video.mux_asset_id,
        playback_id=video.playback_id,
        status=video.status,
        created_by=video.created_by,
        created_at=video.created_at,
    )


@router.get("/{video_id}/play", response_model=PlayResponse)
def play_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    if video.mux_asset_id:
        try:
            mux_service = MuxService()
            latest_status = mux_service.get_asset_status(video.mux_asset_id)
            if latest_status != video.status:
                video.status = latest_status
                db.commit()
                db.refresh(video)
        except Exception:
            pass

    if video.status != VideoStatus.READY.value:
        return PlayResponse(status=video.status, playback_url=None)

    if video.is_premium and current_user.role == UserRole.USER:
        raise HTTPException(status_code=403, detail="Premium content")

    playback_url = MuxService.get_public_playback_url(video.playback_id)
    return PlayResponse(status=video.status, playback_url=playback_url)
