import os
import crud
import magic
import webbrowser
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, messagebox


class VideoData:
    def __init__(self, name, path, hour, minutes, seconds, ampm):
        self.name = name
        self.path = path
        self.hour = hour
        self.minutes = minutes
        self.seconds = seconds
        self.ampm = ampm

    def __repr__(self):
        return f'{self.name[0:10]}'


class AutoVideoPlayer:
    def __init__(self, master):
        self.master = master

        self.master.title('Auto Video Player')

        # positioning window at the center of the screen
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        self.x_coordinate = (self.screen_width - 600) // 2
        self.y_coordinate = (self.screen_height - 430) // 2
        self.master.geometry(f'600x430+{self.x_coordinate}+{self.y_coordinate}')

        self.master.resizable(False, False)
        self.frm = Frame(self.master, padding=10)
        self.frm.grid(row=0, column=0)

        self.frm2 = LabelFrame(self.frm, text='Video & Play Time')
        self.frm2.grid(row=0, column=0, ipadx=5)

        self.frm3 = LabelFrame(self.frm, text='Video List')
        self.frm3.grid(row=4, column=0, pady=10, padx=10, ipadx=5)

        self.default_ampm = None
        self.default_seconds = None
        self.default_minute = None
        self.default_hour = None

        self.create_widgets()

    def open_filedialog(self):
        f = magic.Magic(mime=True, uncompress=True)
        self.master.filename = filedialog.askopenfilename(initialdir=os.path.join(os.path.expanduser('~'), 'Videos'),
                                                          title='Select a video',
                                                          filetypes=(('mp4 files', '*.mp4'), ('all files', '*.*'))
                                                          )
        if self.master.filename == '':
            return
        video_format = f.from_file(self.master.filename)
        if video_format.startswith('video/'):
            video_path.set(self.master.filename)
        else:
            messagebox.showerror('Incorrect video format', 'File selected is not a video.')

    def get_data_to_save(self):
        video_save_limit = 12
        total = self.number_of_saved_videos() + 1

        if total <= video_save_limit:

            # get video name
            global video_name_to_save
            required_length = 25
            video_name = video_name_textbox.get()
            number_of_video_name_characters = len(video_name)

            if 0 < number_of_video_name_characters <= required_length:
                video_name_to_save = video_name
            else:
                if number_of_video_name_characters == 0:
                    messagebox.showwarning('Empty field', 'Video name cannot be empty.')
                    return
                if number_of_video_name_characters > required_length:
                    messagebox.showwarning('Character limit exceeded', 'Video name must be less than 25 characters.')
                    video_name_textbox.delete(0, END)
                    return

            # get video path
            video_path_to_save = video_path_textbox.get()
            if video_path_to_save == '':
                messagebox.showwarning('Empty field', 'Video path cannot be empty.')
                return

            # get time
            hour_to_save = hour_entry.get()
            minute_to_save = minute_entry.get()
            seconds_to_save = seconds_entry.get()
            ampm_to_save = ampm_entry.get()

            if any(value == '' for value in (hour_to_save, minute_to_save, seconds_to_save, ampm_to_save)):
                messagebox.showerror('Invalid time', 'The time set is invalid.')
                self.clear_textboxes()
                return

            # add video record to database
            crud.add_video_record(video_name_to_save,
                                  video_path_to_save,
                                  hour_to_save,
                                  minute_to_save,
                                  seconds_to_save,
                                  ampm_to_save)

            # clear textboxes
            self.clear_textboxes()

            # display all saved videos
            self.video_list_component()
        else:
            messagebox.showerror('Limit reached', 'Maximum number of videos to save has been reached.')

    @staticmethod
    def clear_textboxes():
        video_name_textbox.delete(0, END)
        video_path_textbox.delete(0, END)
        hour_entry.set('12')
        minute_entry.set('00')
        seconds_entry.set('00')
        ampm_entry.set('AM')

    @staticmethod
    def number_of_saved_videos():
        return len(crud.list_video_records())

    def refresh_video_list_component(self):
        all_video_records = crud.list_video_records()

        for button in self.frm3.winfo_children():
            button.destroy()

        increment = 0
        all_video_records.append(0)

        for i in range(3):
            for j in range(4):
                if all_video_records[0 + increment] != 0:
                    button = Button(self.frm3, text=all_video_records[0 + increment], padding=4)
                    button.grid(row=i, column=j, padx=10, pady=10)
                    button.bind('<Button-1>', self.delete_video)
                    button.bind('<Return>', self.delete_video)
                    increment += 1
                else:
                    break

    def delete_video(self, event):
        response = messagebox.askyesno('Delete video', 'Do you want to delete this video record?')
        button_text = event.widget.cget('text')

        if response == 1:
            all_video_records = crud.list_video_records()
            for record in all_video_records:
                if str(record.video_name).startswith(str(button_text)):
                    crud.delete_video_record(record.video_name)
                    messagebox.showinfo('Success', 'Video record deleted.')
                    self.refresh_video_list_component()
                    break

    def video_play_time_component(self):
        self.default_hour = StringVar(value='12')
        self.default_minute = StringVar(value='00')
        self.default_seconds = StringVar(value='00')
        self.default_ampm = StringVar(value='AM')

        Style().configure('Custom.TLabel', font='Helvetica 10')

        # video name section
        video_name_label = Label(self.frm2, text='Video Name', style='Custom.TLabel')
        video_name_label.grid(row=0, column=0)

        global video_name_textbox

        video_name_textbox = Entry(self.frm2, width=50)
        video_name_textbox.grid(row=0, column=1, columnspan=10, pady=10, padx=10, ipady=4)

        # video path section
        video_path_label = Label(self.frm2, text='Video Path', style='Custom.TLabel')
        video_path_label.grid(row=1, column=0)

        global video_path
        global video_path_textbox
        video_path = StringVar()
        video_path_textbox = Entry(self.frm2, textvariable=video_path, width=50)
        video_path_textbox.grid(row=1, column=1, columnspan=10, pady=10, padx=10, ipady=4)

        browse_button = Button(self.frm2, text='Browse...', padding=4, command=self.open_filedialog)
        browse_button.grid(row=1, column=11)

        # time section
        time_label = Label(self.frm2, text='Select Time', style='Custom.TLabel')
        time_label.grid(row=2, column=0, padx=10, pady=10)

        global hour_entry
        hour_entry = Spinbox(self.frm2, textvariable=self.default_hour, format='%02.0f', from_=1, to=12, width=5)
        hour_entry.grid(row=2, column=1, padx=10, pady=10, ipady=4, sticky='w')

        global minute_entry
        minute_entry = Spinbox(self.frm2, textvariable=self.default_minute, format='%02.0f', from_=0, to=59, width=5)
        minute_entry.grid(row=2, column=2, padx=10, pady=10, ipady=4, sticky='w')

        global seconds_entry
        seconds_entry = Spinbox(self.frm2, textvariable=self.default_seconds, format='%02.0f', from_=0, to=59, width=5)
        seconds_entry.grid(row=2, column=3, padx=10, pady=10, ipady=4, sticky='w')

        global ampm_entry
        ampm_entry = Combobox(self.frm2, textvariable=self.default_ampm, width=5, values=['AM', 'PM'])
        ampm_entry.grid(row=2, column=4, padx=10, pady=10, ipady=4, sticky='w')

        # save and cancel buttons
        save_button = Button(self.frm2, text='Save', padding=4, command=self.get_data_to_save)
        save_button.grid(row=3, column=1, columnspan=2, padx=10, pady=10)
        cancel_button = Button(self.frm2, text='Cancel', padding=4, command=self.clear_textboxes)
        cancel_button.grid(row=3, column=3, columnspan=2, padx=10, pady=10)

    def video_list_component(self):
        Style().configure('Custom.TLabel', font='Helvetica 10')

        increment = 0
        video_list = crud.list_video_records()
        video_list.append(0)

        for i in range(3):
            for j in range(4):
                if video_list[0 + increment] != 0:
                    button = Button(self.frm3, text=video_list[0 + increment], padding=4)
                    button.grid(row=i, column=j, padx=10, pady=10)
                    button.bind('<Button-1>', self.delete_video)
                    button.bind('<Return>', self.delete_video)
                    increment += 1
                else:
                    break

    def create_widgets(self):
        self.video_play_time_component()
        self.video_list_component()


def main():
    root = Tk()
    app = AutoVideoPlayer(root)
    root.mainloop()


if __name__ == '__main__':
    main()
