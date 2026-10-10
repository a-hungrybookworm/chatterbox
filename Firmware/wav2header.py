""" Converts WAV recordings into C header files """

import os
import re
import struct
import sys
import wave

TARGET_RATE = 16000           # must match audio_sample_rate on esp32
PEAK_LEVEL = 0.9              # loudest point of each sound scaled to 90% of maximum
VALUES_PER_LINE = 12          

def read_wav(path):
    """ return (mono samples as floats from -1.0 to 1.0, sample rate) """
    try: 
        wav = wave.open(path, "rb")       # reads binary data
    except wave.Error as error:           # if file isn't a wav (with signed 16-bit PCM)
        sys.exit(f"{path}: {error}\n"
            "make sure the file is a WAV with encoding 'signed 16-bit PCM'. ")
    with wav:
        channels = wav.getnchannels()        # mono/ stereo
        width = wav.getsampwidth()           # bytes per sample
        rate = wav.getframerate()            # file's sample rate
        raw = wav.readframes(wav.getnframes())

    count = len(raw) // width  # for each sample
    # convert every value to fraction (between -1 and 1)
    if width == 1:       # 8-bit wav is unsigned 
        values = [(b - 128) / 128 for b in raw]
    elif width == 2:
        values = [v / 32768 for v in struct.unpack(f"<{count}h", raw)] 
    elif width == 3:
        values =[int.from_bytes(raw[i: i + 3], "little", signed = True)/ 8388608
                 for i in range(0, count * 3, 3)]
    elif width == 4:
        values = [v / 2147483648 for v in struct.unpack(f"<{count}i", raw)]
    else:
        sys.exit(f"{path}: sample width ({width} bytes) not supported.")

    if channels > 1: # averages each pair of values in stereo channels
        values = [sum(values[i: i + channels]) / channels
                  for i in range(0, len(values) - channels + 1, channels)]
    return values, rate

def resample(samples, source_rate, target_rate):
    if source_rate == target_rate or not samples: 
        return samples # return samples unchanged in such cases
    step = source_rate/ target_rate

    # smoothen sound before shrinking rate so high pitch doesn't become harsh
    # simple moving average low-pass filter

    window = int(step)
    if window > 1:
        smoothed, running = [], 0 
        for i, value in enumerate(samples): 
            running += value 
            if i >= window:
                running -= samples[i - window]
            smoothed.append(running / min(i + 1, window))
        samples = smoothed

    out = []
    for i in range(int(len(samples) / step)): # loops once per output sample
        position = i * step
        j = int(position)
        fraction = position - j
        a = samples[j]
        b = samples[j + 1] if j + 1 < len(samples) else a # prevents reading beyond end of list
        out.append(a + (b - a) * fraction) # finds the value at a fraction of distance between a and b
    return out

def write_header(path, samples, source_name):
    stem = os.path.splitext(os.path.basename(source_name))[0] # file name (1st part)
    name = re.sub(r"[^0-9a-zA-Z]+", "_", stem).strip("_").lower() or "sound" # name safe for C++
    array_name = f"SOUND_{name.upper()}" 
    header_path = os.path.join(os.path.dirname(path) or ".", f"sound_{name}.h")  # same folder

    values = [max(-32768, min(32767, round(s * 32767))) for s in samples] # turns each -1..1 value to 16-bit int
    seconds = len(values) / TARGET_RATE # clip length

    lines = [
        "#pragma once",
        "#include <stdint.h>", # defines int16_t
        "#include <stddef.h>", # defines size_t
        "",
        f"const int16_t {array_name}[] = {{",
    ]
    for i in range(0, len(values), VALUES_PER_LINE): # writes numbers 12 per line
        chunk = values[i: i + VALUES_PER_LINE]
        lines.append("  " + ", ".join(str(v) for v in chunk) + ",")
    lines +=[
        "};", # closes array
        f"const size_t {array_name}_LENGTH = " # adds length constraint
        f"sizeof({array_name}) / sizeof({array_name}[0]);",
        "",
    ]
    with open(header_path, "w", newline="\n") as file: # identical file on Windows and Mac
        file.write("\n".join(lines)) # joins all lines with newline chars into one big string
    return header_path, seconds, len(values) * 2 # last is size in bytes

def main():
    if len(sys.argv) < 2: # words on command line i.e. if no other file thr
        sys.exit(__doc__)  

    total_bytes = 0
    for path in sys.argv[1:]: # for each wav file
        samples, rate = read_wav(path)
        samples = resample(samples, rate, TARGET_RATE) # read, decode, convert to 16kHz
        peak = max((abs(s) for s in samples), default=0.0) # loudest point, allows for empty files
        if peak > 0:
            samples = [s * PEAK_LEVEL / peak for s in samples] # adjusting loudness, make sure no division by 0
        header, seconds, size = write_header(path, samples, path)
        total_bytes += size # adds filesize to running total
        
    if total_bytes > 700 * 1024:
        print("High file size!")

if __name__ == "__main__": # only call if file run directly
    main() 