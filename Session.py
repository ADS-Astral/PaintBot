from datetime import datetime
import PySimpleGUI as sg


class Session:
    """
    A session is a job or task appointed to the robot.
    The robot can remember what it was previously doing after turning it on or off.
    """

    startTime = 0
    file = None

    # Contains all the feeds in short-term memory.
    feeds = []

    def __init__(self, fileName=None):
        if fileName is not None:
            self.file = open(file=fileName, mode='a')
        else:
            self.time = datetime.now()
            self.file = open(file="session_{}.csv".format(self.time).replace(":", "."), mode='w')
        pass

    def __del__(self):
        if self.file is not None:
            self.file.close()
        pass

    def Append(self, feed):
        """
        Adds a new feed into the feeder list.
        """
        self.feeds.append(feed)
        pass

    def Flush(self):
        """
        Causes the CSV file to save everything from feeder list.
        """
        with self.file as appender:
            for feed in self.feeds:
                appender.write(str(feed.ToRow()))
        self.feeds.clear()

    pass  # class Session


class Feed:
    """
    A feed is an event or action performed by or to the robot as an element of history for the session.
    """

    timestamp = 0
    distance = 0
    battery = 0
    paint = ""
    position = None
    rotation = 0
    colorBitmap = None
    depthBitmap = None

    def ToRow(self):
        return [
            self.timestamp,
            self.distance,
            self.battery,
            self.paint,
            self.position,
            self.rotation,
            self.colorBitmap,
            self.depthBitmap,
        ]
        pass

    pass  # class Feed


if __name__ == '__main__':

    FEEDS_LISTED = 100

    timeLapse = 0

    session = Session()

    for i in range(0, 10000):
        session.Append(Feed())

    layout = [
        [sg.Text(key="file-label"), sg.FileBrowse()],
        [sg.Slider(key="time-slider", range=(0, 120), orientation="h", tick_interval=30)],
        [sg.InputText(key="time-input", default_text="0")],
        [sg.Listbox(key="feed-list", values=[], size=(30, 6))],
        [sg.Submit(), sg.Cancel()],
    ]

    window = sg.Window(
        "Session Viewer - Paint Bot",
        layout,
        no_titlebar=False,
        location=(0, 0))

    timeInput = window["time-input"]
    timeSlider = window["time-slider"]
    timeSliderValue = 0

    fileLabel = window["file-label"]
    fileLabel.Update(value="File: ")

    feedValues = []
    feedList = window["feed-list"]
    i = 0
    for feed in session.feeds:
        if 0 <= feed.timestamp < 20000:
            feedValues.append("#{} ({})".format(i, feed.timestamp))
        i += 1

    while True:
        event, values = window.Read(timeout=1)
        if event in ("Quit", None):
            break

        if timeLapse is not values["time-slider"]:
            timeLapse = values["time-slider"]
            timeSlider.Update(value=timeLapse)
            timeInput.Update(value=timeLapse)
        elif timeLapse is not timeInput.Get():
            timeLapse = timeInput.Get()
            timeSlider.Update(value=timeLapse)
            timeInput.Update(value=timeLapse)
        if feedValues is not None:
            feedList.Update(values=feedValues)
            feedValues = None

        # window.Refresh()

    window.close()
