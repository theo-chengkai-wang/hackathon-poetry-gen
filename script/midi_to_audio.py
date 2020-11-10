import os


def midi2audio(input_mid, output):
    os.system('timidity %s -Ow -o %s' % (input_mid, output))
    return output


if __name__ == '__main__':
    midi2audio('../static/midi/output.mid', './output.wav')
