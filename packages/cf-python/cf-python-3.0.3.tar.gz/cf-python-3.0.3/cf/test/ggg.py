import cf, numpy

q, t = cf.read('~/cf-python/docs/source/sample_files/file.nc')


print(q)

r = q[0].squeeze()
s = q[:, 0].squeeze()
r[...] = 1
print (r)
print (s)
a = r+s
print (a)
print(r.array)
print(s.array)
print(a.array)
print (a.equals(q, verbose=1))
