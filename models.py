from database import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column


class VideoRecord(Base):
    __tablename__ = 'video_records'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    video_name: Mapped[str] = mapped_column(String(25), unique=True)
    video_path: Mapped[str]
    hour: Mapped[int] = mapped_column(Integer)
    minutes: Mapped[int] = mapped_column(Integer)
    seconds: Mapped[int] = mapped_column(Integer)
    ampm: Mapped[str] = mapped_column(String(2))

    def __repr__(self):
        return f'{self.video_name[0:10]}'

