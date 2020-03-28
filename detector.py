import cv2, sys
#import pkg_resources
from os import listdir, path
from mtcnn.mtcnn import MTCNN
from keras.preprocessing import image
from keras_vggface.vggface import VGGFace
from scipy.spatial.distance import cosine
from keras_vggface.utils import preprocess_input

#weights_file=pkg_resources.resource_stream('mtcnn', 'data/mtcnn_weights.npy')
#steps_threshold=[0.6, 0.7, 0.7]
detector = MTCNN(min_face_size=20, scale_factor=0.709)
network = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')

class RTAS():

	def __init__(self):
		self.path='pictures/'
		self.label='target'
		self.size=(224, 224)
		self.unknown='?'
		self.mindist=0.4
		self.metadata={}
		self.password='Ap31cp5767*' # ubuntu password
		self.traindata()

	def getfeatures(self, img):
		try:
			results = detector.detect_faces(img)
			if results:
				resized = []
				for result in results:
					x, y, w, h = result['box']
					he, wi, cs = img.shape
					a, b, c, d = max(0, x), min(x+w, wi), max(0, y), min(y+h, he)
					resized.append(cv2.resize(img[c:d, a:b], dsize=self.size))
				return network.predict(preprocess_input(resized)), results
		except Exception as error: print(error)
		return None, None

	def traindata(self):
		for file in listdir(self.path):
			try:
				feature, results = self.getfeatures(image.img_to_array(cv2.cvtColor(cv2.imread(self.path+file, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)))
				if feature.any():
					if not self.label in self.metadata:
						self.metadata[self.label] = []
					self.metadata[self.label].extend(feature)
			except Exception as error: print(error)

	def recognizefaces(self, img):
		labels = []
		testfeatures, results = self.getfeatures(img)
		if results:
			for testfeature in testfeatures:
				label, mindist = self.unknown, 1.0
				for key in self.metadata.keys():
					for trainedfeature in self.metadata[key]:
						dist = cosine(trainedfeature, testfeature)
						if mindist > dist: label, mindist = key, dist
				labels.append(self.unknown) if mindist >= self.mindist else labels.append(label)
			return labels

	def upload(self):
		if self.metadata:
			cap = cv2.VideoCapture(-1)
			while(True):
				ret, frame = cap.read()
				if ret:
					labels = self.recognizefaces(image.img_to_array(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
					if labels and self.label in labels:
						sys.stdout = open('output.txt', 'w')
						print(self.password)
						os.system("python3 unlock.py")
						os.system("rm output.txt")
						break
				if cv2.waitKey(1) & 0xFF == 27:
					break
			cap.release()
		else:
			print("message: no faces in pictures")

if __name__ == "__main__":
	recognizer = RTAS()
	recognizer.upload()