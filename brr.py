import numpy as np
import simpleaudio as sa

fs = 44100
duration = 10  # seconds
t = np.arange(fs * duration)
b = t / fs

def G(d, p, v, a=0, m=5, n=5):
    T = 8.8 * b - d
    # JS: (T/a & 31) - 17  -- JS bitwise ops coerce to int32
    if a:
        w = np.abs((np.floor(T / a).astype(int) & 31) - 17)
    else:
        w = 0
    # JS: (T>>5)%4  -- JS bitwise ops coerce to int32
    T_int = T.astype(int)
    idx = ((T_int >> 5) % 4).astype(int)
    # JS: '6202'[(T>>5)%4] - 3
    scale = np.array([int('6202'[i]) for i in idx]) - 3
    # JS: b/224&1?5:4  -- JS: (int(b/224)&1) ? 5 : 4
    k = np.where((b / 224).astype(int) & 1, 5, 4)
    # JS: (w % m)
    w_mod_m = (w % m).astype(int) if a else 0
    # JS: (5514 >> (w % m) * k) & 15
    if a:
        shift = w_mod_m * k
        mask = ((5514 >> shift) & 15) / 12
        extra = (np.floor(w / n) - mask)
    else:
        extra = 0
    return (t + v * np.sin(5 * T)) * 2 ** (
        p + scale / 12 + (a and extra)
    )

def S(x): return ((x.astype(int) & 128) / 4)
def I(x): return np.abs((x.astype(int) & 255) - 128) / 4

def E(f, c, w, q, d, p, v, a, m=5, n=5):
    o = np.zeros_like(w, dtype=float)
    for i in range(4):
        # JS: (i==0)||(c==i%2)||(1-q)
        mask = (i == 0) | (c == i % 2) | (np.abs(1 - q) > 1e-8)
        # mask is bool, f(G(...)) is array, so mask * array is fine
        o += mask * f(G(d * i, p, v, a, m, n)) / (i + 1)
    return w * o

def R(s, l, x=1):
    return np.where(b < s, 0, np.where(b < s + l, (b - s) / l, x))

def F(s, l):
    return np.where(b < s, 1, np.where(b < s + l, 1 - (b - s) / l, 0))

def D(t_, h): return 1 - (8.8 * b) % (t_ / h)
def P(c, v, p=0.5): return v * (np.abs((b + 4 * c) % 8 / 4 - 1) - p) + 1

f = F(192, 32)

def A(c, v):
    return 1.2 * (
        E(S, c, R(0, 8, F(32, 32)), 0.6, 2 + R(8, 24, 1.2), 1, v, 1) +
        E(I, c, R(32, 16, F(64, 16)), 1, 3, 1, 2 * v, 1) +
        E(S, c, R(64, 8, F(96, 32)), 0.2, 3, 1, v, 1, 4)
    )

def U(c, v):
    return 1.2 * D(2, 4) * E(S, c, R(112, 32, F(160, 32)), 0.5, 3, 0, v, 2, 4, 4) + \
           1.5 * D(2, 4 + 8 * R(176, 16)) * E(I, c, R(144, 16, f), 0, 3, 1, v, 2)

def B(c, v):
    return R(12, 20, F(128, 96)) * (0.7 * S(G(0, -1, v)) + 0.2 * S(G(0, -2, v)))

def L(c):
    return f * (
        0.7 * E(S, c, R(24, 32), 0.5, 3, 1, 14, 8) +
        E(I, c, R(80, 16), 0.5, 3, 1, 16, 8, 4, 4)
    )

r = R(0, 32)
left = A(0, 10) * P(0, r) + U(0, 10) * P(0, 0.8, 0.8) + B(0, 12) + L(0) * P(1, 0.8)
right = A(1, -8) * P(1, r) + U(1, -8) * P(1, 0.8, 0.8) + B(1, -10) + L(1) * P(0, 0.8)

# Mix and normalize
audio = np.stack([left, right], axis=1)
audio /= np.max(np.abs(audio))
audio = (audio * (2**15 - 1)).astype(np.int16)

# Play
play_obj = sa.play_buffer(audio, 2, 2, fs)
play_obj.wait_done()