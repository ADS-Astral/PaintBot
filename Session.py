from datetime import datetime


class Session:
    """
    A session is a job or task appointed to the robot.
    The robot can remember what it was previously doing after turning it on or off.
    """

    startTime = 0
    file = None

    # Contains all the feeds in short-term memory.
    feeds = []

    def __init__(self):
        self.time = datetime.now()
        self.file = open(file="session_{}.csv".format(self.time).replace(":", "."), mode='a')
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

    distance = 0
    battery = 0
    paint = ""
    position = None
    rotation = 0

    def ToRow(self):
        return [
            self.distance,
            self.battery,
        ]
        pass

    pass  # class Feed
