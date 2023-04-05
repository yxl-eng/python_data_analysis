from PIL import Image
import PIL
import imagehash
import scipy
import logging
import numpy as np
import os
from PIL import ImageFile
import matplotlib.pyplot as plt
import math
ImageFile.LOAD_TRUNCATED_IMAGES = True

logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.ERROR,
                    filename='ERROR.log',
                    filemode='a')

class ImageQueryError(BaseException):
	pass

class ImageQueryShapeNotMatchError(ImageQueryError):
	def __init__(self,shape1,shape2):
		self.shape1=shape1
		self.shape2=shape2

	def __str__(self):
		return f"shape of img1:{self.shape1} is not equal with shape of img2:{self.shape2}"

class ImageQueryNoSimilarImageFoundError(ImageQueryError):
	def __init__(self):
		pass

	def __str__(self):
		return "ImageQueryNoSimilarImageFoundError"

class ImageQuery(object):
	def __init__(self):
		self.images={}

	def _create_and_image(self,img_path):
		try :
			img= PIL.Image.open(img_path)
		except FileNotFoundError as error1:
			# logging.error(f"ImagePathNotFound:{error1}")
			print(f"ImagePathNotFound:{error1}")
			return None
		except PIL.UnidentifiedImageError as error2:
			# logging.error(f"UnidentifiedImage:{error2}")
			print(f"UnidentifiedImage:{error2}")
			return None
		else:
			return img

	def load_images(self,images_dir):
		for filepath,dirnames,filenames in os.walk(images_dir):
			for file in filenames:
				if file.endswith('jpg') or file.endswith('png') or file.endswith('jpeg'):
					imgfile = os.path.join(filepath, file)
					img = self._create_and_image(imgfile)
					self.images[imgfile]=img


	def pixel_difference(self,img1_path,img2_path):
		img1=self._create_and_image(img1_path)
		img2 = self._create_and_image(img2_path)
		shape1=img1.size
		shape2=img2.size
		if shape1!=shape2:
			raise ImageQueryShapeNotMatchError(shape1,shape2)
		img11=np.array(img1)
		img22=np.array(img2)
		pixel_diff=np.abs(img11-img22)
		return np.sum(pixel_diff)/(img1.width*img1.height)

	def histogram_similarity(self,img1_path,img2_path):
		img1 = self._create_and_image(img1_path)
		img2 = self._create_and_image(img2_path)
		c_hist_1 = img1.histogram()
		c_hist_2 = img2.histogram()
		p_cor = scipy.stats.pearsonr(c_hist_1, c_hist_2)
		s_cor = scipy.stats.spearmanr(c_hist_1, c_hist_2)
		k_cor = scipy.stats.kendalltau(c_hist_1, c_hist_2)
		return p_cor,s_cor,k_cor

	def hash_similarity(self,img1_path,img2_path,method="average"):
		img1 = self._create_and_image(img1_path)
		img2 = self._create_and_image(img2_path)
		if method == "average":
			hash1 = imagehash.average_hash(img1)
			hash2 = imagehash.average_hash(img2)
		elif method == "phash":
			hash1 = imagehash.phash(img1)
			hash2 = imagehash.phash(img2)
		elif method == "dhash":
			hash1 = imagehash.dhash(img1)
			hash2 = imagehash.dhash(img2)
		elif method == "whash":
			hash1 = imagehash.whash(img1)
			hash2 = imagehash.whash(img2)
		hamming_distance = hash1 - hash2
		similarity = 1 - hamming_distance / len(hash1.hash)
		return similarity

	def search_image(self,img_path,key,n,threshold):
		similarity={}
		for k in self.images.keys():
			hash_cor=self.hash_similarity(img_path,k)
			pixel_cor=self.pixel_difference(img_path,k)
			p_cor, s_cor, k_cor=self.histogram_similarity(img_path,k)
			if key=='pearson':
				similarity[k]= p_cor
			elif key=='spearman':
				similarity[k] = s_cor
			elif key=='kendall':
				similarity[k] = k_cor
			elif key=='hash':
				similarity[k] = hash_cor
			elif key=='pixel':
				similarity[k] = pixel_cor
		sorted_similarity=sorted(similarity.items(),key=lambda d:d[1],reverse=True)
		print(sorted_similarity[1][1])
		if key=='pixel':
			if float(sorted_similarity[-2][1]) > threshold:
				raise ImageQueryNoSimilarImageFoundError
			else:
				for i, j in enumerate(sorted_similarity[-n:]):
					plt.subplot(int(math.sqrt(n)) + 1, int(math.sqrt(n)) + 1, i + 1)
					plt.imshow(self.images[j[0]])
				plt.show()
		if key=='hash':
			if float(sorted_similarity[1][1]) < threshold:
				raise ImageQueryNoSimilarImageFoundError
			else:
				for i, j in enumerate(sorted_similarity[:n]):
					plt.subplot(int(math.sqrt(n)) + 1, int(math.sqrt(n)) + 1, i + 1)
					plt.imshow(self.images[j[0]])
				plt.show()
		if key=="pearson" or key=='spearman' or key=='kendall':
			rou, p = sorted_similarity[1][1]
			if float(rou) < threshold:
				raise ImageQueryNoSimilarImageFoundError
			else:
				for i, j in enumerate(sorted_similarity[:n]):
					plt.subplot(int(math.sqrt(n)) + 1, int(math.sqrt(n)) + 1, i + 1)
					plt.imshow(self.images[j[0]])
				plt.show()

# img=ImageQuery()
# img._create_and_image("cats/741.jpg")

# try :
# 	print(img.pixel_difference("C:\\Users\\86137\\PycharmProjects\\pythonProject\\python数据分析\\异常与图像检索（第七周）\\lfw\Alex_Barros\\Alex_Barros_0001.jpg", "C:\\Users\\86137\\PycharmProjects\\pythonProject\\python数据分析\\异常与图像检索（第七周）\\lfw\Alex_Barros\\Alex_Barros_0002.jpg"))
# except ImageQueryShapeNotMatchError as e:
# 	print(e)
# print(Image.open("C:\\Users\\86137\\PycharmProjects\\pythonProject\\python数据分析\\异常与图像检索（第七周）\\lfw\Alex_Barros\\Alex_Barros_0001.jpg").size)
# print(Image.open("C:\\Users\\86137\\PycharmProjects\\pythonProject\\python数据分析\\异常与图像检索（第七周）\\lfw\Alex_Barros\\Alex_Barros_0002.jpg").size)
# try :
# 	print(img.pixel_difference("C:\\Users\\86137\\PycharmProjects\\pythonProject\\python数据分析\\异常与图像检索（第七周）\\lfw\\Arminio_Fraga\\Arminio_Fraga_0003.jpg", "C:\\Users\\86137\\PycharmProjects\\pythonProject\\python数据分析\\异常与图像检索（第七周）\\lfw\\Arminio_Fraga\\Arminio_Fraga_0004.jpg"))
# except ImageQueryShapeNotMatchError as e:
# 	print(e)
# print(Image.open("C:\\Users\\86137\\PycharmProjects\\pythonProject\\python数据分析\\异常与图像检索（第七周）\\lfw\\Arminio_Fraga\\Arminio_Fraga_0003.jpg").size)
# print(Image.open("C:\\Users\\86137\\PycharmProjects\\pythonProject\\python数据分析\\异常与图像检索（第七周）\\lfw\\Arminio_Fraga\\Arminio_Fraga_0004.jpg").size)

# p_cor, s_cor, k_cor=img.histogram_similarity("C:\\Users\\86137\\PycharmProjects\\pythonProject\\python数据分析\\异常与图像检索（第七周）\\lfw\Alex_Barros\\Alex_Barros_0001.jpg","C:\\Users\\86137\\PycharmProjects\\pythonProject\\python数据分析\\异常与图像检索（第七周）\\lfw\Alex_Barros\\Alex_Barros_0002.jpg")
# print(p_cor,s_cor,k_cor)

# print(img.hash_similarity("C:\\Users\\86137\\PycharmProjects\\pythonProject\\python数据分析\\异常与图像检索（第七周）\\lfw\\Arminio_Fraga\\Arminio_Fraga_0003.jpg","C:\\Users\\86137\\PycharmProjects\\pythonProject\\python数据分析\\异常与图像检索（第七周）\\lfw\\Arminio_Fraga\\Arminio_Fraga_0004.jpg"))
# print(img.hash_similarity("C:\\Users\\86137\\PycharmProjects\\pythonProject\\python数据分析\\异常与图像检索（第七周）\\lfw\\Alex_Barros\\Alex_Barros_0001.jpg","C:\\Users\\86137\\PycharmProjects\\pythonProject\\python数据分析\\异常与图像检索（第七周）\\lfw\\Alex_Barros\\Alex_Barros_0002.jpg"))

# img.load_images("C:/Users/86137/PycharmProjects/pythonProject/python数据分析/异常与图像检索（第七周）/lfw")
# print(img.images)
# try:
# 	img.search_image('C:/Users/86137/PycharmProjects/pythonProject/python数据分析/异常与图像检索（第七周）/lfw/Gerhard_Schroeder/Gerhard_Schroeder_0001.jpg', 'hash',8,0.1)
# except ImageQueryNoSimilarImageFoundError as e:
# 	logging.error('ImageQueryNoSimilarImageFoundError')
# 	print(e)

