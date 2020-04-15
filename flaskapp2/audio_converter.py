from pydub import AudioSegment 


def audio_convert(source_filepath,dest_filepath):
    range = AudioSegment.from_file(source_filepath) 
    print("Gkiri3 :",range)
    myname = source_filepath.rsplit(".", 1)[0]
    dest_filepath = myname + str("2") + str(".wav")

    range.export(dest_filepath, format = 'wav')
    print("Gkiri4 :",dest_filepath)
    print("Gkiri5 :",range)
