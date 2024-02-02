import scipy.io.wavfile as wav
import sys

if len(sys.argv) < 2:
  print("Usage: python3 wavlist2sec.py wav.list")
  sys.exit(1)

with open(sys.argv[1]) as wav_list:
  file_n = 0
  total_secs = 0
  for wav_path in wav_list:
    file_n += 1
    rate, sig = wav.read(wav_path.strip())
    total_secs += sig.shape[0] / rate

print("Total files: %d, Total Time in seconds: %.3f, in hours: %.3f"%(file_n, total_secs, total_secs / 3600.0))


