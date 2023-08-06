from os.path import isfile


class FileDescription:

    def __init__(self, path: str, extension: str, index: int):
        self.path = path
        self.extension = extension
        self.index = index

    def getPath(self) -> str:
        return self.path

    def getIndex(self) -> int:
        return self.index

    def getExtension(self) -> str:
        return self.extension

    def getFileName(self, thisPath = None, extension = None) -> str:
        if thisPath is None:
            thisPath = self.path
        return self.getFileNameWithIndex(thisPath, self.index, extension)

    def getFileNameWithExtension(self, extension: str) -> str:
        return self.getFileName(self.path, extension)

    def getFileNameWithIndex(self, thisPath: str, index: int, extension = None) -> str:
        if extension is None:
            extension = self.extension
        return "%s/%04d.%s" % (thisPath, index, extension)

    def getRawFileName(self) -> str:
        return "%04d.%s" % (self.index, self.extension)

    def addToIndex(self, count: int):
        self.index += count

    def nextFileExists(self, count: int, thisPath = None):
        if thisPath is None:
            thisPath = self.path
        return isfile(self.getFileNameWithIndex(thisPath, self.index + count))

    def previousFileExists(self, count: int, thisPath = None):
        if thisPath is None:
            thisPath = self.path
        return isfile(self.getFileNameWithIndex(thisPath, self.index - count))
