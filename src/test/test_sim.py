from ctypes import *

sim = cdll.LoadLibrary("c_lib/libsim.so")
sim.find.argtypes = [c_char_p, c_char_p]
sim.find.restype = POINTER(c_char_p)

res = sim.find(b"1134 Kepler", b"/home/litian/dbpedia/subject.text")
#print(res)

print(res[0])
print(res[1])
#print(res.decode("utf-8"))