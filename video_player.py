import threading
import time
import datetime
import schedule
import webbrowser


def main():
    pass


def video_player_main(obj):
    time_start, time_end = get_time_and_path(obj)
    schedule_video_play(obj, time_start, time_end)


def get_time_and_path(obj):
    if obj:
        hour, minutes, seconds, ampm, path = obj.hour, obj.minutes, obj.seconds, obj.ampm, obj.path
        raw_time = f'{hour} {minutes} {seconds} {ampm}'
        converted_time = datetime.datetime.strptime(raw_time, '%I %M %S %p')
        converted_time = converted_time.replace(microsecond=0)
        end_time = converted_time + datetime.timedelta(seconds=1)

        time_start = str(converted_time.time())[0:5]
        time_end = str(end_time.time())[:]

        return time_start, time_end
    return


def play_video(path):
    webbrowser.open(path)


def job(path):
    play_video(path)


def schedule_video_play(obj, time_start, time_end):
    schedule.every().day.at(time_start).until(time_end).do(job, obj.path).tag(obj.video_name)


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


thread = threading.Thread(target=run_schedule)
thread.start()


def delete_video_called(video_name):
    schedule.clear(video_name)


if __name__ == '__main__':
    main()
