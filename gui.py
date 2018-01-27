import time
from tkinter import Tk, Label, Button, Frame
from calc import calc
from tool import requests_responce


URL1 = 'https://www.eliftech.com/school-task'
URL2 = 'https://u0byf5fk31.execute-api.eu-west-1.amazonaws.com/etschool/task'


class GuiApp:
    urls = [URL1, URL2]

    def __init__(self, master):
        master.title('TASK')
        center(master)
        master.resizable(False, False)

        statusFrame = Frame(master, height=60)
        buttomFrame = Frame(master, bg='gray')

        statusFrame.pack(side='top', fill='x')
        buttomFrame.pack(side='bottom', fill='both', expand=1)

        self.label = Label(statusFrame, text='Empty')
        self.run_button = Button(buttomFrame, text='Run', command=self.work_task)

        self.run_button.place(anchor='center', relx=0.5, rely=0.5, width=80, height=50)
        self.label.place(anchor='center', relx=0.5, rely=0.5)

    def get_response_json(self, method='get', secc_url=None, json=None):
        status = False
        response = None
        if secc_url:
            status, response = requests_responce(secc_url, method=method, data_json=json)
        start = time.time()
        while not status:
            for url in self.urls:
                status, response = requests_responce(url, method=method, data_json=json)
                if status:
                    self.secc_url = url
                    return response.json()
            if time.time() - start >= 10:
                return None
        return response.json() if status else None

    def work_task(self):
        json = self.get_response_json()
        if json:
            result = [calc(expressions) for expressions in json['expressions']]
            json = {'id': json['id'], 'results': result}
            json = self.get_response_json(method='post', secc_url=self.secc_url, json=json)
            if not json or ('passed' not in json or not json['passed']):
                label_config = {'text': "False\n you can try again", 'fg': 'red'}
            else:
                label_config = {'text': "True\n you can try again", 'fg': 'green'}
        else:
            label_config = {'text': "False\n you can try again", 'fg': 'red'}
        self.label.configure(label_config)


def center(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


if __name__ == '__main__':
    root = Tk()
    my_gui = GuiApp(root)
    root.mainloop()
    root.mainloop()
