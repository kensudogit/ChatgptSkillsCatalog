"""Print rising-edge indices from a simple 0/1 waveform string."""
import sys
wave = sys.argv[1] if len(sys.argv) > 1 else "0011001110"
edges = [i for i in range(1, len(wave)) if wave[i-1] == "0" and wave[i] == "1"]
print(edges)
