#################################Description##################################

ftvstt is a France Télévisions python library which encapsulates multiple online speech-to-text APIs, in order to call them as easily as possible.

It currently supports :
Amazon Transcribe
Google Cloud speech-to-text
Vocapia Voxsigma
Bertin Mediaspeech

#################################Quickstart###################################

ftvstt is not currently available through pip, you have to download the package and import it directly :

import ftvstt

#################################Usage######################################

Example of transcription through the services:

Vocapia Voxsigma:

vocapiaTranscriber = ftvstt.Vocapia("https://rest1.vocapia.com:8093/voxsigma")
vocapiaTranscriber.authenticate("EXAMPLE_ID","EXAMPLE_PASS")
transcript = vocapiaTranscriber.transcribe("/path/to/file.wav")
vocapiaTranscriber.deauthenticate()


Bertin Mediaspeech:
bertinTranscriber = ftvstt.Bertin("https://demo02.mediaspeech.com:4433/api")
bertinTranscriber.authenticate("EXAMPLE_ID","EXAMPLE_PASS")
transcript = bertinTranscriber.transcribe("/path/to/file.wav")
bertinTranscriber.deauthenticate()


Amazon transcribe:
amazonTranscriber = ftvstt.Amazon("AMAZON_S3_BUCKET_NAME")
amazonTranscriber.authenticate("/path/to/amazon/credentials.csv")
transcript = amazonTranscriber.transcribe("/path/to/file.wav")
amazonTranscriber.deauthenticate()

You need an amazon AWS S3 bucket besides Amazon AWS Transcribe in order to make transcriptions.


Google cloud speech-to-text:
googleTranscriber = ftvstt.Google()
googleTranscriber.authenticate("/path/to/google/credentials.json")
transcript = googleTranscriber.transcribe("/path/to/file.wav")
googleTranscriber.deauthenticate()


################################Custom vocabulary file##################################

For every provider except Bertin, you can add a custom vocabulary file of probable words as shown :

googleTranscriber = ftvstt.Google()
googleTranscriber.authenticate("/path/to/google/credentials.json")
googleTranscriber.set_vocabulary_file("/path/to/vocabulary/file.txt")
transcript = googleTranscriber.transcribe("/path/to/file.wav")
googleTranscriber.deauthenticate()


The vocabulary file should be of the form:
word1
word2
word3
...

#################################Results handling######################################

Once a transcription is done, the transcribe function of a Transcriber returns a Transcript instance from ftvstt.transcripts sub-module.

A Transcript instance, as transcript in previous codes, has several useful attributes :

transcript.text : a string containing the textual transcript of the audio file.
transcript.words : a list of Word instances from ftvstt.transcripts sub-module, each one has a content (str), a startTime (float), an endTime (float), a speaker (Speaker instance from ftvstt.transcripts sub-module) (and can have a confidence (float) depending on the provider used) attribute.
transcript.speakers : a list of Speaker instances from ftvstt.transcripts sub-module, each one has an id (int), (and can have a gender (str : "M" or "F") depending on the provider used).
transcript.raw : a string containing the raw result of the transcription received from the provider, which type is transcript.rawType (str : "json" or "xml").

#################################Error handling######################################


If an error has occured during transcription, a custom python Exception from the ftvstt.exceptions sub-module will be raised. The error will also be accessbile in the exception attribute of the transcript result, as you can see in this example:

googleTranscriber = ftvstt.Google()
googleTranscriber.authenticate("/path/to/google/credentials.json")
try:
    transcript = googleTranscriber.transcribe("/path/to/file.wav")
except:
    pass
raise transcript.exception
googleTranscriber.deauthenticate()


#################################Testing######################################

Incoming...
