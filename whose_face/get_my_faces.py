import cv2
import dlib
import os
import sys
import random

output_dir = './faces'
size = 64
# 创建放人脸照片的目录
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 改变图片的亮度与对比度
def relight(img, light=1, bias=0):
    w = img.shape[1]
    h = img.shape[0]
    #image = []
    for i in range(w):
        for j in range(h):
            for c in range(3):  #三通道
                tmp = int(img[j, i, c]*light + bias)
                if tmp > 255:
                    tmp = 255
                elif tmp < 0:
                    tmp = 0
                img[j, i, c] = tmp
    return img

student_number = input("please input student number")
# 去除首位空格
student_number = student_number.strip()
# 去除尾部 \ 符号
student_number = student_number.rstrip("\\")
new_path = output_dir+"/"+student_number
isExists = os.path.exists(new_path)

# 判断结果
if not isExists:
    # 如果不存在则创建目录
    # 创建目录操作函数
    os.makedirs(new_path)

    print(new_path + ' 创建成功')
else:
    # 如果目录存在则不创建，并提示目录已存在
    print(new_path + ' 目录已存在')



# 使用dlib自带的frontal_face_detector作为我们的特征提取器
detector = dlib.get_frontal_face_detector()
# 打开摄像头 参数为输入流，可以为摄像头或视频文件
camera = cv2.VideoCapture(0)

capture_number = 4 #拍摄为实际数量-1
#10000

index = 0
while True:
    if index <= capture_number:
        print('Being processed picture %s' % index)
        # 从摄像头读取照片
        success, img = camera.read()
        # 转为灰度图片
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 使用detector进行人脸检测
        dets = detector(gray_img, 1)

        for i, d in enumerate(dets):
            x1 = d.top() if d.top() > 0 else 0
            y1 = d.bottom() if d.bottom() > 0 else 0
            x2 = d.left() if d.left() > 0 else 0
            y2 = d.right() if d.right() > 0 else 0
            #把人脸切出来
            face = img[x1:y1, x2:y2]
            # 调整图片的对比度与亮度， 对比度与亮度值都取随机数，这样能增加样本的多样性
            #face = relight(face, random.uniform(0.5, 1.5), random.randint(-50, 50))

            face = cv2.resize(face, (size, size))

            cv2.imshow('image', face)

            cv2.imwrite(output_dir+"/"+student_number+"/"+student_number+"_"+str(index)+".bmp", face)

            index += 1
        key = cv2.waitKey(30) & 0xff
        if key == 27:
            break
    else:
        print('Finished!')
        camera.release()
        break