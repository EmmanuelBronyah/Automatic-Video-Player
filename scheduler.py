import time
import datetime
import schedule
import threading
import webbrowser


def main():
    """
    This module is not meant to be run on its own. So this main function is set up
    so if this module is run, nothing happens.

    :return: Returns None.
    """
    pass


def video_player_main(obj):
    """
    Runs the get_time_and_path function and schedule_video_play function in that order.

    :param obj: This is the current video record saved into the database.
    :return: Returns None.
    """
    time_start, time_end = get_time_and_path(obj)
    schedule_video_play(obj, time_start, time_end)


def convert_time(hour, minutes, seconds, ampm):
    raw_time = f'{hour} {minutes} {seconds} {ampm}'
    converted_time = datetime.datetime.strptime(raw_time, '%I %M %S %p')
    converted_time = converted_time.replace(microsecond=0)

    return converted_time


def get_time_and_path(obj):
    """
    Collects the time and path of the current video record saved into the database.

    :param obj: This is the current video record saved into the database.
    :return: Returns the time scheduled to play the video and the time to end the
    scheduled task.
    """
    if obj:
        hour, minutes, seconds, ampm = obj.hour, obj.minutes, obj.seconds, obj.ampm
        converted_time = convert_time(hour, minutes, seconds, ampm)
        end_time = converted_time + datetime.timedelta(seconds=1)
        time_start = str(converted_time.time())[0:5]
        time_end = str(end_time.time())[:]

        return time_start, time_end
    return


def play_video(path):
    """
    Plays the video scheduled.

    :param path: The path to the video scheduled to play.
    :return: Returns None
    """
    webbrowser.open(path)


def job(path):
    """
    Runs the play_video function.

    :param path: The path to the video scheduled to play.
    :return: Returns None.
    """
    play_video(path)


def schedule_video_play(obj, time_start, time_end):
    """
    Runs the statement which schedules the video to play.
    :param obj: This is the current video record saved into the database.
    :param time_start: The time scheduled to play the video.
    :param time_end: The time scheduled to end the scheduled task.
    :return: Returns None.
    """
    schedule.every().day.at(time_start).until(time_end).do(job, obj.path).tag(obj.video_name)


def run_schedule():
    """
    Runs a loop which continually checks for scheduled tasks.
    :return: Returns None.
    """
    while True:
        schedule.run_pending()
        time.sleep(1)


# The schedule function is placed in a separate thread to
# avoid a situation where multiple instances of the same task
# are scheduled and executed concurrently
thread = threading.Thread(target=run_schedule)
thread.start()


def delete_video_called(video_name):
    """
    Removes the scheduled task for the deleted video record.

    :param video_name: The video name of the deleted video record.
    :return: Returns None.
    """
    schedule.clear(video_name)


if __name__ == '__main__':
    main()
