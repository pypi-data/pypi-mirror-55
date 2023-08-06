class Transcript:
    def __init__(self, raw=None, provider=None):
        if provider is None or raw is None:
            self.success = None
            self.raw = None
            self.text = None
            self.inputPath = None
            self.exception = None
            self.provider = None
            self.rawType = None
            self.exception = None

            self.words = None
            self.speakers = None
        else:
            self.raw = raw
            self.provider = provider
            self.inputPath = None
            self.rawType = provider.rawType
            provider.set_text(self)
            provider.set_words(self)
            self.success = True
            self.exception = None


    def dump_raw_result(self, outputPath):
        if self.success:
            with open(outputPath, 'w') as outputFile:
                outputFile.write(self.raw)
        else:
            raise self.exception

    def dump_text_result(self, outputPath):
        if self.success:
            with open(outputPath, 'w') as outputFile:
                outputFile.write(self.text)
        else:
            raise self.exception


class Word:
    def __init__(self, content, startTime=None, endTime=None, speaker=None, confidence=None):
        self.content = content
        self.startTime = startTime
        self.endTime = endTime
        self.speaker = speaker
        self.confidence = confidence


class Speaker:
    def __init__(self, id, gender=None):
        self.id = id
        self.gender = gender

    def __eq__(self, other) :
        if self.__class__ != other.__class__:
            return False
        return self.__dict__ == other.__dict__
