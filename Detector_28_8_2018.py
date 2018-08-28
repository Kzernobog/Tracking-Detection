import numpy as np
import cv2
import pdb
from ctypes import *
import os
import re

class _BOX(Structure):
	_fields_ = [("x", c_float),
				("y", c_float),
				("w", c_float),
				("h", c_float)]

class _DETECTION(Structure):
	_fields_ = [("bbox", _BOX),
				("classes", c_int),
				("prob", POINTER(c_float)),
				("mask", POINTER(c_float)),
				("objectness", c_float),
				("sort_class", c_int)]


class _IMAGE(Structure):
	_fields_ = [("w", c_int),
				("h", c_int),
				("c", c_int),
				("data", POINTER(c_float))]

class _METADATA(Structure):
	_fields_ = [("classes", c_int),
				("names", POINTER(c_char_p))]


class YOLODetector(object):
	#constructor
	def __init__(self, config_path="tank-tiny.cfg", weight_path="tank-tiny_17500.weights", meta_path="tank.data" ):
		"""Initializes an object of this class"""
		self.lib = None
		self.netMain=None
		self.metaMain=None
		self.altNames=None
		self.thresh=0.25
		self.configPath = config_path
		self.weightPath = weight_path
		self.metaPath= meta_path
		self.showImage= True 
		self.makeImageOnly = False
		self.initOnly= False
		self.get_network_boxes = None
		self.free_detections = None
		self.load_net_custom = None
		self.do_nms_sort = None
		self.load_meta = None
		self.predict_image= None
		self._initialize_functions_fromSO()
		self._initialize_other_shit()
		

	
	def _initialize_other_shit(self):
		if self.netMain is None:
			self.netMain = self.load_net_custom(self.configPath.encode("ascii"), self.weightPath.encode("ascii"), 0, 1)  # batch size = 1
			print("TYPE OF NETMAIN:", type(self.netMain))
		if self.metaMain is None:
			self.metaMain = self.load_meta(self.metaPath.encode("ascii"))
			print("TYPE OF METAMAIN:", type(self.metaMain))
		if self.altNames is None:
			# In Python 3, the metafile default access craps out on Windows (but not Linux)
			# Read the names file and create a list to feed to detect
			try:
				with open(self.metaPath) as metaFH:
					metaContents = metaFH.read()
					match = re.search("names *= *(.*)$", metaContents, re.IGNORECASE | re.MULTILINE)
					if match:
						result = match.group(1)
					else:
						result = None
					try:
						if os.path.exists(result):
							with open(result) as namesFH:
								namesList = namesFH.read().strip().split("\n")
								self.altNames = [x.strip() for x in namesList]
					except TypeError:
						pass
			except Exception:
				pass
		if self.initOnly:
			pass
	#print("Initialized detector")
			return None
		


	def _initialize_functions_fromSO(self):
		hasGPU = True
		if os.name == "nt":
			cwd = os.path.dirname(__file__)
			os.environ['PATH'] = cwd + ';' + os.environ['PATH']
			winGPUdll = os.path.join(cwd, "yolo_cpp_dll.dll")
			winNoGPUdll = os.path.join(cwd, "yolo_cpp_dll_nogpu.dll")
			envKeys = list()
			for k, v in os.environ.items():
				envKeys.append(k)
			try:
				try:
					tmp = os.environ["FORCE_CPU"].lower()
					if tmp in ["1", "true", "yes", "on"]:
						raise ValueError("ForceCPU")
					else:
						print("Flag value '"+tmp+"' not forcing CPU mode")
				except KeyError:
					# We never set the flag
					if 'CUDA_VISIBLE_DEVICES' in envKeys:
						if int(os.environ['CUDA_VISIBLE_DEVICES']) < 0:
							raise ValueError("ForceCPU")
					##### uncomment to force CPU
					# try:
					# 	global DARKNET_FORCE_CPU
					# 	if DARKNET_FORCE_CPU:
					# 		raise ValueError("ForceCPU")
					# except NameError:
					# 	pass


					# print(os.environ.keys())
					# print("FORCE_CPU flag undefined, proceeding with GPU")
				if not os.path.exists(winGPUdll):
					raise ValueError("NoDLL")
				self.lib = CDLL(winGPUdll, RTLD_GLOBAL)
			except (KeyError, ValueError):
				hasGPU = False
				if os.path.exists(winNoGPUdll):
					self.lib = CDLL(winNoGPUdll, RTLD_GLOBAL)
					print("Notice: CPU-only mode")
				else:
					# Try the other way, in case no_gpu was
					# compile but not renamed
					self.lib = CDLL(winGPUdll, RTLD_GLOBAL)
					print("Environment variables indicated a CPU run, but we didn't find `"+winNoGPUdll+"`. Trying a GPU run anyway.")
		else:
			self.lib = CDLL("./darknet.so", RTLD_GLOBAL)
		self.lib.network_width.argtypes = [c_void_p]
		self.lib.network_width.restype = c_int
		self.lib.network_height.argtypes = [c_void_p]
		self.lib.network_height.restype = c_int

		predict = self.lib.network_predict
		predict.argtypes = [c_void_p, POINTER(c_float)]
		predict.restype = POINTER(c_float)

		if hasGPU:
			set_gpu = self.lib.cuda_set_device
			set_gpu.argtypes = [c_int]

		make_image = self.lib.make_image
		make_image.argtypes = [c_int, c_int, c_int]
		make_image.restype = _IMAGE

		self.get_network_boxes = self.lib.get_network_boxes
		self.get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int), c_int]
		self.get_network_boxes.restype = POINTER(_DETECTION)

		make_network_boxes = self.lib.make_network_boxes
		make_network_boxes.argtypes = [c_void_p]
		make_network_boxes.restype = POINTER(_DETECTION)

		self.free_detections = self.lib.free_detections
		self.free_detections.argtypes = [POINTER(_DETECTION), c_int]

		free_ptrs = self.lib.free_ptrs
		free_ptrs.argtypes = [POINTER(c_void_p), c_int]

		network_predict = self.lib.network_predict
		network_predict.argtypes = [c_void_p, POINTER(c_float)]

		reset_rnn = self.lib.reset_rnn
		reset_rnn.argtypes = [c_void_p]

		load_net = self.lib.load_network
		load_net.argtypes = [c_char_p, c_char_p, c_int]
		load_net.restype = c_void_p

		self.load_net_custom = self.lib.load_network_custom
		self.load_net_custom.argtypes = [c_char_p, c_char_p, c_int, c_int]
		self.load_net_custom.restype = c_void_p

		do_nms_obj = self.lib.do_nms_obj
		do_nms_obj.argtypes = [POINTER(_DETECTION), c_int, c_int, c_float]

		self.do_nms_sort = self.lib.do_nms_sort
		self.do_nms_sort.argtypes = [POINTER(_DETECTION), c_int, c_int, c_float]

		free_image = self.lib.free_image
		free_image.argtypes = [_IMAGE]

		letterbox_image = self.lib.letterbox_image
		letterbox_image.argtypes = [_IMAGE, c_int, c_int]
		letterbox_image.restype = _IMAGE

		self.load_meta = self.lib.get_metadata
		self.lib.get_metadata.argtypes = [c_char_p]
		self.lib.get_metadata.restype = _METADATA

		load_image = self.lib.load_image_color
		load_image.argtypes = [c_char_p, c_int, c_int]
		load_image.restype = _IMAGE

		rgbgr_image = self.lib.rgbgr_image
		rgbgr_image.argtypes = [_IMAGE]

		self.predict_image = self.lib.network_predict_image
		self.predict_image.argtypes = [c_void_p, _IMAGE]
		self.predict_image.restype = POINTER(c_float)
	

	def _array_to_image(self, arr):
		import numpy as np
		# need to return old values to avoid python freeing memory
		arr = arr.transpose(2,0,1)
		c = arr.shape[0]
		h = arr.shape[1]
		w = arr.shape[2]
		arr = np.ascontiguousarray(arr.flat, dtype=np.float32) / 255.0
		data = arr.ctypes.data_as(POINTER(c_float))
		im = _IMAGE(w,h,c,data)
		return im, arr

	def _classify(self, net, meta, im):
		out = self.predict_image(net, im)
		res = []
		for i in range(meta.classes):
			if self.altNames is None:
				nameTag = meta.names[i]
			else:
				nameTag = self.altNames[i]
			res.append((nameTag, out[i]))
		res = sorted(res, key=lambda x: -x[1])
		return res

	def _detect(self, net, meta, img, thresh=.5, hier_thresh=.5, nms=.45, debug= False):
		"""
		Performs the meat of the detection
		"""
		#pylint: disable= C0321
		#im = load_image(image, 0, 0)
		#import cv2
		#custom_image_bgr = cv2.imread(image) # use: detect(,,imagePath,)
		custom_image_bgr=img
		custom_image = cv2.cvtColor(custom_image_bgr, cv2.COLOR_BGR2RGB)
		custom_image = cv2.resize(img,(self.lib.network_width(net), self.lib.network_height(net)), interpolation = cv2.INTER_LINEAR)
		#import scipy.misc
		#custom_image = scipy.misc.imread(image)
		im, arr = self._array_to_image(custom_image)		# you should comment line below: free_image(im)
		if debug: print("Loaded image")
		num = c_int(0)
		if debug: print("Assigned num")
		pnum = pointer(num)
		if debug: print("Assigned pnum")
		self.predict_image(net, im)
		if debug: print("did prediction")
		dets = self.get_network_boxes(net, custom_image_bgr.shape[1], custom_image_bgr.shape[0], thresh, hier_thresh, None, 0, pnum, 0) # OpenCV
		#dets = self.get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum, 0)
		if debug: print("Got dets")
		num = pnum[0]
		if debug: print("got zeroth index of pnum")
		if nms:
			self.do_nms_sort(dets, num, meta.classes, nms)
		if debug: print("did sort")
		res = []
		if debug: print("about to range")
		for j in range(num):
			if debug: print("Ranging on "+str(j)+" of "+str(num))
			if debug: print("Classes: "+str(meta), meta.classes, meta.names)
			for i in range(meta.classes):
				if debug: print("Class-ranging on "+str(i)+" of "+str(meta.classes)+"= "+str(dets[j].prob[i]))
				if dets[j].prob[i] > 0:
					b = dets[j].bbox
					if self.altNames is None:
						nameTag = meta.names[i]
					else:
						nameTag = self.altNames[i]
					if debug:
						print("Got bbox", b)
						print(nameTag)
						print(dets[j].prob[i])
						print((b.x, b.y, b.w, b.h))
					res.append((nameTag, dets[j].prob[i], (b.x, b.y, b.w, b.h)))
		if debug: print("did range")
		res = sorted(res, key=lambda x: -x[1])
		if debug: print("did sort")
		#free_image(im)
		if debug: print("freed image")
		self.free_detections(dets, num)
		if debug: print("freed detections")
		return res


	def detect(self, img, thresh= 0.25, showImage= True, makeImageOnly = False, initOnly= False):

		# Do the detection		
		height, width = img.shape[:2]
		detections = self._detect(self.netMain, self.metaMain, img, thresh)
		
		imcaption = []
		detected_list=[]
		for detection in detections: 
			label = detection[0]
			confidence = detection[1]
			pstring = label+": "+str(np.rint(100 * confidence))+"%"
			imcaption.append(pstring)
			bounds = detection[2]
			shape = img.shape
			yExtent = int(bounds[3])
			xEntent = int(bounds[2])
		
			# Coordinates are around the center
			xCoord = int(bounds[0] - bounds[2]/2)
			yCoord = int(bounds[1] - bounds[3]/2)
			boundingBox = [
				[xCoord, yCoord],
				[xCoord, yCoord + yExtent],
				[xCoord + xEntent, yCoord + yExtent],
				[xCoord + xEntent, yCoord]
			]
			detected_list.append([boundingBox[0][0],boundingBox[0][1],
			boundingBox[2][0],boundingBox[2][1]])
			cv2.rectangle(img, (int(xCoord), int(yCoord)), (int(xCoord + xEntent), int(yCoord + yExtent)), [0,0,255], 2)
		return img, detected_list


if __name__=='__main__':
		yolo=YOLODetector()
		img=cv2.cv2.imread(r"C:\Users\ujjawal\Pictures\object_detection\images\test\COCO_val2014_000000582594.jpg")
		frame,detected_list=yolo.detect(img)
		cv2.cv2.imshow('detection', frame)
		cv2.cv2.waitKey(0)
		print(type(frame), type(detected_list))
		print(frame,detected_list)
		