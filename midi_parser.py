import mido

class Note:
    def __init__(self, time, midi_note, duration, strong):
        self.time = time  # Time in seconds when the note should be hit        
        self.midi_note = midi_note  # MIDI note that will play when the note reaches the bottom
        self.duration = duration  # Duration of the note in seconds
        self.strong = strong

    def __str__(self) -> str:
        return f"Time: {self.time}, MIDI Note: {self.midi_note}, Duration: {self.duration}, Strong: {self.strong}"
        

class Track:
    def __init__(self):
        self.notes = []
        self.time_signature = (4, 4)
        self.bpm = 120
    
    def __str__(self) -> str:
        text = f"Time Signature: {self.time_signature}, BPM: {self.bpm}\n"
        for note in self.notes:
            text += f"Note: {note}\n"
        return text

class Song:
    def __init__(self, midi_file):
        self.tracks = []
        self.midi_file = midi_file
        self.ticks_per_beat = 480

        self._parse_midi()

    def __str__(self) -> str:
        text = f"Song: ticks_per_beat:{self.ticks_per_beat}\n"
        for track in self.tracks:
            text += f"Track: {track}\n"            
        return text

    def _parse_midi(self):
        midi = mido.MidiFile(self.midi_file)        
        time = 0  # Keep track of the running time in the MIDI file        

        self.ticks_per_beat = midi.ticks_per_beat
        
        for midi_track in midi.tracks:        
            
            track = Track()
            
            # current note
            playing_note_start_time = 0
            strong = False

            for message in midi_track:

                if message.type == 'time_signature':
                    track.time_signature = (message.numerator, message.denominator)

                if message.type == 'set_tempo':
                    track.bpm = 60 / (message.tempo / 1000000)

                time += message.time
                            
                
                if message.type == 'note_on' and message.velocity > 0:
                    start_time = (time / self.ticks_per_beat) * (60 / track.bpm)
                    playing_note_start_time = start_time

                    (time_signature_numerator, time_signature_denominator) = track.time_signature
                    strong = (time % (self.ticks_per_beat * time_signature_numerator) == 0)

                elif message.type == 'note_off' or (message.type == 'note_on' and message.velocity == 0):                                        
                    end_time = (time / self.ticks_per_beat) * (60 / track.bpm)
                    duration = end_time - playing_note_start_time                    
                    track.notes.append(Note(playing_note_start_time, message.note, duration, strong))


            self.tracks.append(track)    

#print(Song("simple.mid"))
