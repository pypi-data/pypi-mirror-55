import watchgod


class FileWatcher(watchgod.watcher.AllWatcher):
    """
    A watchgod watcher that only watches a single file
    """

    def __init__(self, root_path, filename):
        """
        Initialize the watcher
        :param root_path: The directory of the file
        :param filename: The filename to watch
        """

        self.filename = filename
        super().__init__(root_path)

    def should_watch_dir(self, entry):
        return False

    def should_watch_file(self, entry):
        return self.filename == entry.name
