from ..logger import log_event

from ..questionbase import QuestionBase
from ..questionbase import register_question_class

from ..interval import Interval

from .. import KEYBOARD_INDICES
from .. import CHROMATIC_SHARP
from .. import CHROMATIC_FLAT
from .. import CHROMATIC_TYPE

from ..sequence import Sequence
from ..resolution import Resolution
from ..prequestion import PreQuestion

from random import choice


@register_question_class
class NoteNameQuestion(QuestionBase):
    """Implements a Note Name test.
    """

    name = 'notename'

    @log_event
    def __init__(self, mode='major', tonic='C', octave=4, descending=False,
                 chromatic=False, n_octaves=1, valid_intervals=CHROMATIC_TYPE,
                 user_durations=None, prequestion_method='tonic_only',
                 resolution_method='nearest_tonic', *args, **kwargs):
        """Inits the class.

        Args:
            mode (str): A string representing the mode of the question.
                Eg., 'major' or 'minor'
            tonic (str): A string representing the tonic of the question,
                eg.: 'C'; if omitted, it will be selected randomly.
            octave (int): A scienfic octave notation, for example, 4 for 'C4';
                if not present, it will be randomly chosen.
            descending (bool): Is the question direction in descending, ie.,
                intervals have lower pitch than the tonic.
            chromatic (bool): If the question can have (True) or not (False)
                chromatic intervals, ie., intervals not in the diatonic scale
                of tonic/mode.
            n_octaves (int): Maximum number of octaves of the question.
            valid_intervals (list): A list with intervals (int) valid for
                random choice, 1 is 1st, 2 is second etc. Eg. [1, 4, 5] to
                allow only tonics, fourths and fifths.
            user_durations (str): A string with 9 comma-separated `int` or
                `float`s to set the default duration for the notes played. The
                values are respectively for: pre-question duration (1st),
                pre-question delay (2nd), and pre-question pos-delay (3rd);
                question duration (4th), question delay (5th), and question
                pos-delay (6th); resolution duration (7th), resolution
                delay (8th), and resolution pos-delay (9th).
                duration is the duration in of the note in seconds; delay is
                the time to wait before playing the next note, and pos_delay is
                the time to wait after all the notes of the respective sequence
                have been played. If any of the user durations is `n`, the
                default duration for the type of question will be used instead.
                Example::
                    "2,0.5,1,2,n,0,2.5,n,1"
            prequestion_method (str): Method of playing a cadence or the
                exercise tonic before the question so to affirm the question
                musical tonic key to the ear. Valid ones are registered in the
                `birdears.prequestion.PREQUESION_METHODS` global dict.
            resolution_method (str): Method of playing the resolution of an
                exercise. Valid ones are registered in the
                `birdears.resolution.RESOLUTION_METHODS` global dict.
        """

        default_durations = {
            'preq': {'duration': 2, 'delay': 0.5, 'pos_delay': 1},
            'quest': {'duration': 2, 'delay': 0.5, 'pos_delay': 0},
            'resol': {'duration': 2.5, 'delay': 0.5, 'pos_delay': 1}
        }

        super(NoteNameQuestion, self).\
            __init__(mode=mode, tonic=tonic, octave=octave,
                     descending=descending, chromatic=chromatic,
                     n_octaves=n_octaves, valid_intervals=valid_intervals,
                     user_durations=user_durations,
                     prequestion_method=prequestion_method,
                     resolution_method=resolution_method,
                     default_durations=default_durations, *args, **kwargs)

        self.is_harmonic = False

        self.random_pitch = choice(self.allowed_pitches)

        self.interval = Interval(self.tonic_pitch, self.random_pitch)

        self.pre_question = self.make_pre_question(method=prequestion_method)
        self.question = self.make_question()
        self.resolution = self.make_resolution(method=resolution_method)

    def make_pre_question(self, method):

        prequestion = PreQuestion(method=method, question=self)

        return prequestion()

    def make_question(self):

        question = Sequence([self.random_pitch], **self.durations['quest'])

        return question

    def make_resolution(self, method):

        resolve = Resolution(method=method, question=self)
        resolution = resolve()

        return resolution

    def play_question(self, callback=None, end_callback=None, *args, **kwargs):
        # Other threads can call a thread’s join() method. This blocks the
        # calling thread until the thread whose join() method is called is
        # terminated.
        # https://docs.python.org/3/library/threading.html#thread-objects

        self.display.update({'main_display': ('The tonic is {tonic}.'
                                              'Press the'
                                              'key representing the'
                                              'second note.'
                                              .format(tonic=self.tonic_str))})

        self.pre_question.play(callback=callback, end_callback=end_callback,
                               *args, **kwargs)
        self.question.play(callback=None, end_callback=end_callback,
                           *args, **kwargs)

    def play_resolution(self, callback=None, end_callback=None, *args,
                        **kwargs):

        thread = self.resolution.play(callback=callback,
                                      end_callback=end_callback, *args,
                                      **kwargs)
        thread.join()

    def check_question(self, user_input_char):
        """Checks whether the given answer is correct.
        """

        global INTERVALS

        from ..scale import ChromaticScale
        c_chromatic = ChromaticScale(tonic='C', n_octaves=2)
        # question_tone_chromatic = ChromaticScale(tonic=self.tonic_str,
        #                                         octave=self.octave,
        #                                         n_octaves = self.n_octaves)

        keyboard_index = \
            KEYBOARD_INDICES['chromatic']['ascending']['major']

        user_semitones = keyboard_index.index(user_input_char[0])

        user_pitch = c_chromatic[user_semitones]
        user_note = user_pitch.note

        correct_semitones = abs(int(self.tonic_pitch) - int(self.random_pitch))
        correct_note = self.random_pitch.note

        if user_note in CHROMATIC_SHARP:
            user_semitones = CHROMATIC_SHARP.index(user_note)
        elif user_note in CHROMATIC_FLAT:
            user_semitones = CHROMATIC_SHARP.index(user_note)

        if correct_note in CHROMATIC_SHARP:
            correct_semitones = CHROMATIC_SHARP.index(user_note)
        elif correct_note in CHROMATIC_FLAT:
            correct_semitones = CHROMATIC_FLAT.index(correct_note)

        signal = '✓' if user_semitones == correct_semitones else 'x'  # u2713

        extra_response_str = """\
       “{}”
user {} “{}”
{} semitones
""".format(correct_note, signal, user_note, self.interval['semitones'])

        response = dict(
            is_correct=False,
            # user_interval=user_interval,
            user_note=user_note,
            # correct_interval=correct_interval,
            correct_note=correct_note,
            user_response_str=user_note,
            correct_response_str=correct_note,
            extra_response_str=extra_response_str,
        )

        if user_note == correct_note:
            response.update({'is_correct': True})

        else:
            response.update({'is_correct': False})

        return response
