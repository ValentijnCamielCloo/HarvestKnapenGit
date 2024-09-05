from datetime import datetime


class Logger():
    """
    A tool to help track intermediary steps of a Python script, an alternative and more advanced
    version to using print() statements to the terminal.

    Rather than using print() statements, a user can add entries to the log. The entries are printed
    to the terminal in a clear fashion, which not only shows the value to be printed, but also
    shows the index of the entry and the exact moment in time the entry was created.

    In addition to tracking intermediary results, this can be used to track the time spent to get
    these results, giving insight in computational efficiency.

    The Logger stores all entries as a list.
    The list can be written to a .txt file in the project folder.


    Created as part of the TU Delft MSc Course CORE workshops.
    """


    def __init__(self, name="logger", filename="log", writelive=True):
        self.name = name
        self.filename = filename
        self.log_entries = [] # self.LogEntry(self, "Initializing", "Initalizing log...")
        self.writelive = writelive

        self.add("", "Initializing log...")


    class LogEntry():
        def __init__(self, logger, time, description="", val=None, units=""):
            self.__logger = logger
            self.index = len(self.__logger.log_entries)
            self.val = val
            self.description = description
            self.units = units
            self.time = time
            self.entry = self.__format_entry()


        def __format_entry(self):
            separator = f"--------------"
            line1 = f"ENTRY {self.index} | {self.time}"
            line2 = f"    {self.description}"
            line3 = f"    {self.val} {self.units}" if self.val is not None else None
            mystring = "\n" + "\n".join(filter(None, [separator,line1,line2,line3,separator]))
            return mystring


    def add(self, description="", val=None, units="", print_log=False):
        time = self.__getuniquetime()
        entry = self.LogEntry(self, time=time, description=description, val=val, units=units)
        self.log_entries.append(entry)

        if self.writelive:
            self.write_log()

        if print_log:
            print(entry.entry)

        return time

    @property
    def log(self, print_log=True):
        if print_log:
            for e in self.log_entries:
                print(e.entry)
        return [e.entry for e in self.log_entries]

    @property
    def get_log_entry_timestamps(self):
        return [e.time for e in self.log_entries]


    def write_log(self, filename=None):
        if filename is None:
            filename= self.filename
        with open(filename + ".txt", "w") as fn:
            for e in self.log_entries:
                fn.write(e.entry)


    def __getuniquetime(self):
        time = str(datetime.now())
        i = 0
        utime = time + "." + str(i).zfill(3)

        while utime in self.get_log_entry_timestamps:
            i += 1
            utime = time + "." + str(i).zfill(3)

            if i > 999:
                break

        return utime


if __name__ == "__main__":

    """
    Example on how to use the logger
    """

    # Create class 'logger' to log print statements
    logger = Logger()

    # Add entries to log. With optional statement "print_log" we ensure that the statement is stored to the log.
    logger.add(description="Maximum load of element", val="3125", units="kN/m")
    logger.add("Text description of the second entry to log", print_log=True)
    logger.add(73234, "A random value to print")


    # Write log to a txt file in your process. Takes optional filename as an input.
    logger.write_log()

    # Print all log entries to screen. Also returns them as a list.
    logger.log
