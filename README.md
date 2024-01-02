# Automatic Video Player
This is a simple python GUI application which
takes the path to a video file located on your system
and automatically opens the video file also by a timestamp
you give. 

> [!NOTE]  
> The video files of the video records saved are only
opened once within a 24hour range and the application 
only saves up to 12 videos records.
> The windows setup file has been included in the repo.

## Features
* **Takes video name:** A unique name to describe the 
video record is collected for indication.
* **Takes video path:** A path to the video is collected
and validated.
* **Takes time:** Collects the time of play of the video
and performs extra validation of the time given.
* **List out saved records:** Lists out video records saved
in the database.

## Getting started
1. **Clone the repository to your machine.**
```shell
git clone https://github.com/EmmanuelBronyah/Automatic-Video-Player.git
```
2. **Navigate to the project directory.**
```shell
cd auto-video-player
```
3. **Run the program.**
```shell
python main.py
```
## Usage
* Upon running the program you must enter a video name
which must be no more than 25 characters and must not 
be an integer. You must then provide a valid path to a 
video file and select or enter a time for the video to
be played. After you have successfully done all that, click
the save button to save the video record to the database.
A scheduling task will be run in the background which then plays
the video when the time you provided is met. You can hit
the cancel button which deletes all the information filled
previously including reseting the time, this allows you 
to re-fill the input boxes and make changes.

## License
This project is licensed under the MIT License.

## Acknowledgements
- Built by Bronyah Emmanuel.
