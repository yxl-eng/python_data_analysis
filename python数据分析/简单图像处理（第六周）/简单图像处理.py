from PIL import ImageFilter
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageProcessor(object):
    def __init__(self,img:Image.Image):
        self.img=img
        self.param=[]

    def process(self):
        pass

class GrayProcessor(ImageProcessor):
    def process(self):
        super().process()
        gray=self.img.convert('1')
        # gray.show()
        gray.save("灰度图.png")
        return gray

class ResizeProcessor(ImageProcessor):
    def process(self):
        # self.param =[700,1000]
        super().process()
        print('original size:',self.img.size)
        new_img=self.img.resize((self.param[0],self.param[1]))
        print('now size:',new_img.size)
        # new_img.show()
        new_img.save("调整大小后.png")
        return new_img

    def process1(self):
        self.param=[0,0,700,700]
        super().process()
        print('original size:', self.img.size)
        box=(self.param[0],self.param[1],self.param[2],self.param[3])
        cropped = self.img.crop(box)
        print('now size:', cropped.size)
        # cropped.show()
        cropped.save("裁剪后.png")
        return cropped

class BlurProcessor(ImageProcessor):
    def process(self):
        super().process()
        blur1 =self.img.filter(ImageFilter.BLUR)
        blur2 = self.img.filter(ImageFilter.SMOOTH_MORE)
        # plt.figure()
        # plt.subplot(2, 1, 1)
        # plt.imshow(blur1)
        # plt.subplot(2, 1, 2)
        # plt.imshow(blur2)
        # plt.show()
        return blur1

class EdgeDetectionProcessor(ImageProcessor):
    def process(self):
        super().process()
        blur1 = self.img.filter(ImageFilter.CONTOUR)
        blur2 = self.img.filter(ImageFilter.EMBOSS)
        # plt.figure()
        # plt.subplot(2, 1, 1)
        # plt.imshow(blur1)
        # plt.subplot(2, 1, 2)
        # plt.imshow(blur2)
        # plt.show()
        return blur1

# img=GrayProcessor(Image.open('1.png')).process()
# img=ResizeProcessor(Image.open('1.png')).process()
# img=ResizeProcessor(Image.open('1.png')).process1()
# img=BlurProcessor(Image.open('1.png')).process()
# img=EdgeDetectionProcessor(Image.open('1.png')).process()

class ImageShop(object):
    def __init__(self,img_format: str, img_dir: str):
        self.img_format=img_format
        self.img_dir=img_dir
        self.img_list = []
        self.processed_imgs = []
        self.param=[]

    def load_images(self):
        for file in os.listdir(self.img_dir):
            if file.endswith(self.img_format):
                imgfile=os.path.join(self.img_dir,file)
                img=Image.open(imgfile)
                self.img_list.append(img)

    #此处的Processor表示一个包含process函数的类，如之前定义的几个类
    def __batch_ps(self,Processor):
        for img in self.img_list:
            p = Processor(img)
            p.param=self.param
            p.process()
            self.processed_imgs.append(p.process())

    def batch_ps(self,*args):
        for op_name,op_param in args:
            if op_name=='GrayProcessor':
                self.param=[*op_param]
                self.__batch_ps(GrayProcessor)
            elif op_name=='ResizeProcessor':
                self.param=[*op_param]
                self.__batch_ps(ResizeProcessor)
            elif op_name=='BlurProcessor':
                self.param=[*op_param]
                self.__batch_ps(BlurProcessor)
            elif op_name=='EdgeDetectionProcessor':
                self.param=[*op_param]
                self.__batch_ps(EdgeDetectionProcessor)

    def save(self,output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for i,img in enumerate(self.processed_imgs):
            img.save(os.path.join(output_dir,f"processed_{i}{self.img_format}"))

    def display(self,row,col,size:tuple,num):
        fig, axes = plt.subplots(row, col, figsize=size)
        for i, ax in enumerate(axes.flat):
            if i < num:
                ax.imshow(self.processed_imgs[i])
                ax.axis('off')
            else:
                break
        plt.show()

class TestImageShop(object):
    def test(self):
        img_format='.jpg'
        img_dir=r'C:\Users\86137\PycharmProjects\pythonProject\python数据分析\简单图像处理（第六周）\picture'
        output_dir='result'
        image_shop=ImageShop(img_format,img_dir)
        image_shop.load_images()
        image_shop.batch_ps(("GrayProcessor", []),
                            ("ResizeProcessor", [500,500]),
                            ("BlurProcessor", []),
                            ("EdgeDetectionProcessor", []))
        image_shop.save(output_dir)
        image_shop.display(row=6, col=7, size=(10,10), num=42)


if __name__=="__main__":
    TestImageShop().test()