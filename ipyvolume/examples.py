import numpy as np
import ipyvolume
from numpy import cos, sin, sqrt, pi

try:
	import scipy.ndimage
	import scipy.special
except:
	pass # it's ok, it's not crucial
__all__ = ["example_ylm"]

def xyz(shape=128, limits=[-3, 3], spherical=False, sparse=True, centers=False):
	dim = 3
	try:
		shape[0]
	except:
		shape = [shape] * dim
	try:
		limits[0][0]
	except:
		limits = [limits] * dim
	if centers:
		#print([(   vmin+(vmax-vmin)/float(N)/2, vmax-(vmax-vmin)/float(N)/4, (vmax-vmin)/float(N)) for (vmin, vmax), N in zip(limits, shape)])
		v = [slice(vmin+(vmax-vmin)/float(N)/2, vmax-(vmax-vmin)/float(N)/4, (vmax-vmin)/float(N)) for (vmin, vmax), N in zip(limits, shape)]
	else:
		v = [slice(vmin, vmax+(vmax-vmin)/float(N)/2, (vmax-vmin)/float(N-1)) for (vmin, vmax), N in zip(limits, shape)]
	if sparse:
		x, y, z = np.ogrid.__getitem__(v)
	else:
		x, y, z = np.mgrid.__getitem__(v)
	if spherical:
		r = np.linalg.norm([x, y, z])
		theta = np.arctan2(y, x)
		phi = np.arccos(z / r)
		return x, y, z, r, theta, phi
	else:
		return x, y, z


def example_ylm(m=0, n=2, shape=128, limits=[-4, 4], **kwargs):
	__, __, __, r, theta, phi = xyz(shape=shape, limits=limits, spherical=True)
	radial = np.exp(-(r - 2) ** 2)
	data = np.abs(scipy.special.sph_harm(m, n, theta, phi) ** 2) * radial
	return ipyvolume.volshow(data=data.T, **kwargs)

def ball(rmax=3, rmin=0, shape=128, limits=[-4, 4], draw=True, show=True, **kwargs):
	import ipyvolume.pylab as p3
	__, __, __, r, theta, phi = xyz(shape=shape, limits=limits, spherical=True)
	data = r * 0
	data[(r < rmax) & (r >= rmin)] = 0.5
	if "data_min" not in kwargs:
		kwargs["data_min"] = 0
	if "data_max" not in kwargs:
		kwargs["data_max"] = 1
	data  = data.T
	if draw:
		vol = p3.volshow(data=data, **kwargs)
		if show:
			p3.show()
		return vol
	else:
		return data

# http://graphics.stanford.edu/data/voldata/

def klein_bottle(draw=True, show=True, figure8=False, endpoint=True, uv=False, wireframe=False, texture=None, both=False, interval=1000):
    import ipyvolume.pylab as p3
    # http://paulbourke.net/geometry/klein/
    u = np.linspace(0, 2 * pi, num=40, endpoint=endpoint)
    v = np.linspace(0, 2 * pi, num=40, endpoint=endpoint)
    u, v = np.meshgrid(u, v)
    if both:
    	x1, y1, z1, u1, v1 = klein_bottle(endpoint=endpoint, draw=False, show=False)
    	x2, y2, z2, u2, v2 = klein_bottle(endpoint=endpoint, draw=False, show=False, figure8=True)
    	x = [x1, x2]
    	y = [y1, y2]
    	z = [z1, z2]
    else:
	    if figure8:
	        #u -= np.pi
	        #v -= np.pi
	        a = 2
	        s = 5
	        x = s * (a + cos(u / 2) * sin(v) - sin(u / 2) * sin(2 * v)/2) * cos(u)
	        y = s * (a + cos(u / 2) * sin(v) - sin(u / 2) * sin(2 * v)/2) * sin(u)
	        z = s * (sin(u / 2) * sin(v) + cos(u / 2) * sin(2 * v)/2)
	    else:
	        r = 4 * (1 - cos(u) / 2)
	        x = 6 * cos(u) * (1 + sin(u)) \
	            + r * cos(u) * cos(v) * (u < pi) \
	            + r * cos(v + pi) * (u >= pi)
	        y = 16 * sin(u) + r * sin(u) * cos(v) * (u < pi)
	        z = r * sin(v)
    if draw:
        if texture:
            uv = True
        if uv:
            mesh = p3.plot_mesh(x, y, np.array([z]), wrapx=not endpoint, wrapy=not endpoint, u=u/(2*np.pi), v=v/(2*np.pi), wireframe=wireframe, texture=texture)
        else:
            mesh = p3.plot_mesh(x, y, np.array([z]), wrapx=not endpoint, wrapy=not endpoint, wireframe=wireframe, texture=texture)
        if show:
            if both:
                p3.animation_control(mesh, interval=interval)
            p3.show()
        return mesh
    else:
        return x, y, z, u, v
