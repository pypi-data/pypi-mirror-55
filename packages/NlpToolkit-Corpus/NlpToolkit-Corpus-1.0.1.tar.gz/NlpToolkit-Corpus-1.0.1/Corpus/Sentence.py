from __future__ import annotations
from Dictionary.Word import Word

from Corpus.LanguageChecker import LanguageChecker


class Sentence:

    __words: list

    """
    Another constructor of Sentence class which takes a fileName as an input. It reads each word in the file
    and adds to words list.

    PARAMETERS
    ----------
    fileName: str
        input file to read words from.
    """
    def __init__(self, fileName = None):
        self.__words = []
        if fileName is not None:
            inputFile = open(fileName, "r")
            lines = inputFile.readlines()
            for line in lines:
                wordList = line.split(" ")
                for word in wordList:
                    self.__words.append(Word(word))
            inputFile.close()

    """
    Another constructor of Sentence class which takes a sentence String as an input. It parses the sentence by
    " " and adds each word to the newly created words list.

    PARAMETERS
    ----------
    sentence : str
        String input to parse.
    """
    def initWithSentence(self, sentence: str):
        wordArray = sentence.split(" ")
        for word in wordArray:
            if len(word) > 0:
                self.__words.append(Word(word))

    """
    Another constructor of Sentence class with two inputs; a String sentence and a {@link LanguageChecker}
     * languageChecker. It parses a sentence by " " and then check the language considerations. If it is a valid word,
     * it adds this word to the newly created {@link ArrayList} words.
     *
     * @param sentence        String input.
     * @param languageChecker {@link LanguageChecker} type input.
    """
    def initWithLanguageChecker(self, sentence: str, languageChecker: LanguageChecker):
        wordArray = sentence.split(" ")
        for word in wordArray:
            if len(word) > 0 and languageChecker.isValidWord(word):
                self.__words.append(Word(word))

    """
    The equals method takes a Sentence as an input. First compares the sizes of both words lists and words
    of the Sentence input. If they are not equal then it returns false. Than it compares each word in the list.
    If they are equal, it returns true.

    PARAMETERS
    ----------
    s : Sentence
        Sentence to compare.
        
    RETURNS
    -------
    bool
        True if words of two sentences are equal.
    """
    def __eq__(self, s: Sentence) -> bool:
        if len(self.__words) != len(s.__words):
            return False
        for i in range(len(self.__words)):
            if self.__words[i].getName() != s.__words[i].getName():
                return False
        return True

    """
    The getWord method takes an index input and gets the word at that index.

    PARAMETERS
    ----------
    index : int
        is used to get the word.

    RETURNS
    -------
    Word
        the word in given index.
    """
    def getWord(self, index: int) -> Word:
        return self.__words[index]

    """
    The getWords method returns the words list.

    RETURNS
    -------
    list
        Words ArrayList.
    """
    def getWords(self) -> list:
        return self.__words

    """
    The getStrings method loops through the words list and adds each words' names to the newly created result list.

    RETURNS
    -------
    list
        Result list which holds names of the words.
    """
    def getStrings(self) -> list:
        result = []
        for word in self.__words:
            result.append(word.getName())
        return result

    """
    The getIndex method takes a word as an input and finds the index of that word in the words list if it exists.

    PARAMETERS
    ----------
    word : Word
        Word type input to search for.
        
    RETURNS
    -------
    int
        Index of the found input, -1 if not found.
    """
    def getIndex(self, word: Word) -> int:
        return self.__words.index(word)

    """
    The wordCount method finds the size of the words list.

    RETURNS
    -------
    int
        The size of the words list.
    """
    def wordCount(self) -> int:
        return len(self.__words)

    """
    The addWord method takes a word as an input and adds this word to the words list.
    
    PARAMETERS
    ----------
    word : Word
        Word to add words list.
    """
    def addWord(self, word: Word):
        self.__words.append(word)

    """
    The charCount method finds the total number of chars in each word of words list.

    RETURNS
    -------
    int
        number of the chars in the whole sentence.
    """
    def charCount(self) -> int:
        total = 0
        for word in self.__words:
            total += word.charCount()
        return total

    """
    The replaceWord method takes an index and a word as inputs. It removes the word at given index from words
    list and then adds the given word to given index of words.

    PARAMETERS
    ----------
    i : int      
        index.
    newWord : Word
        to add the words list.
    """
    def replaceWord(self, i: int, newWord: Word):
        self.__words.pop(i)
        self.__words.insert(i, newWord)

    """
    The safeIndex method takes an index as an input and checks whether this index is between 0 and the size of the 
    words.

    PARAMETERS
    ----------
    index : int
        is used to check the safety.
        
    RETURNS
    -------
    bool
        true if an index is safe, false otherwise.
    """
    def safeIndex(self, index: int) -> bool:
        return 0 <= index < len(self.__words)

    """
    The overridden toString method returns an accumulated string of each word in words list.

    RETURNS
    -------
    str
        String result which has all the word in words list.
    """
    def __str__(self) -> str:
        if len(self.__words) > 0:
            result = self.__words[0].__str__()
            for i in range(1, len(self.__words)):
                result = result + " " + self.__words[i].__str__()
            return result
        else:
            return ""

    """
    The toWords method returns an accumulated string of each word's names in words list.

    RETURNS
    -------
    str
        String result which has all the names of each item in words list.
    """
    def toString(self) -> str:
        if len(self.__words) > 0:
            result = self.__words[0].getName()
            for i in range(1, len(self.__words)):
                result = result + " " + self.__words[i].getName()
            return result
        else:
            return ""
