from datetime import datetime


class Session:

    startTime = 0
    file = None
    feeds = []

    def __init__(self):
        self.time = datetime.now()
        self.file = open("session_{}.csv".format(self.time), 'a')
        pass

    def __del__(self):
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
                appender.write(feed.ToRow())
        self.feeds = []

    pass  # class Session


class Feed:

    distance = 0
    battery = 0
    colorFrame = None
    depthFrame = None

    def ToRow(self):
        return [
            self.distance,
            self.battery,
            self.colorFrame,
            self.depthFrame,
        ]
        pass

    pass  # class Feed
