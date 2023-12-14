from database import initialize_database
from models import VideoRecord

session = initialize_database()


def add_video_record(name, path, hour, minutes, seconds, ampm):
    video_record = VideoRecord(video_name=name, video_path=path, hour=hour, minutes=minutes, seconds=seconds, ampm=ampm)
    session.add(video_record)
    session.commit()


def get_video_record(name):
    result = session.query(VideoRecord).filter_by(video_name=name).first()
    return result


def list_video_records():
    results = session.query(VideoRecord).all()
    return results


def number_of_video_records():
    return session.query(VideoRecord).count()


def delete_video_record(name):
    result = session.query(VideoRecord).filter_by(video_name=name).first()
    session.delete(result)
    session.commit()
    return True
