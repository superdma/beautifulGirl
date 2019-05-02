import base64
import json
import requests
import os
import cv2
import numpy as np

class BaiduPicIndentify:
    def __init__(self, img):
        self.AK = "1GrQPnchdLw8GXwKbBp6jek5"
        self.SK = "Q041EpK4ENe3haz2nneLIFq7xGl551Br"
        self.img_src = img
        self.headers = {
            "Content-Type": "application/json; charset=UTF-8"
        }

    def get_accessToken(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + self.AK + '&client_secret=' + self.SK
        response = requests.get(host, headers=self.headers)
        json_result = json.loads(response.text)
        return json_result['access_token']

    def img_to_BASE64(slef, path):
        try:
            with open(path, 'rb') as f:
                base64_data = base64.b64encode(f.read())
                return base64_data
        except FileNotFoundError:
            print(path)
            print("文件名称出错，或文件不存在 或路径不正确, 请重新输入所需图片路径")
            print("=================分割线=====================")
            return None

    def cv_imread(self):
        # 解决OpenCV的imread函数无法读取中文路径和中文命名的文件的问题
        img_path = os.path.abspath(self.img_src)
        print(img_path)
        cv_img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
        # imdecode读取的是rgb，如果后续需要opencv处理的话，需要转换成bgr，转换后图片颜色会变化
        #cv_img=cv2.cvtColor(cv_img,cv2.COLOR_RGB2BGR)
        return cv_img

    def detect_face(self):
        # 人脸检测与属性分析
        img_BASE64 = self.img_to_BASE64(self.img_src)
        if img_BASE64 is None:
            return
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        post_data = {
            "image": img_BASE64,
            "image_type": "BASE64",
            "face_field": "age,beauty,expression,face_shape,gender,glasses,race,landmark,location",
            "max_face_num": 10,
            "face_type": "LIVE"
        }
        access_token = self.get_accessToken()
        request_url = request_url + "?access_token=" + access_token
        response = requests.post(url=request_url, data=post_data, headers=self.headers)
        json_result = json.loads(response.text)
        if json_result['error_msg'] == 'pic not has face':
            print("请更换较为清楚的图片")
            return
        face_list = json_result['result']['face_list']
        print("人脸数：", json_result['result']['face_num'])
        i = 0
        for i in range(0, len(face_list)):
            print("=================分割线=====================")
            print("年 龄：", face_list[i]['age'])
            print("性 别：", face_list[i]['gender']['type'])
            print("种 族：", face_list[i]['race']['type'])
            print("颜 值：", face_list[i]['beauty'])
            print("表 情：", face_list[i]['expression']['type'])
            print("眼 镜：", face_list[i]['glasses']['type'])
            print("脸 型：", face_list[i]['face_shape']['type'])
            i = i+1

        img = self.cv_imread()
        blue = (202, 235, 216)
        # 框的位置为 左上角、右下角的坐标，颜色，填充的样式
        i = 0
        for i in range(0, len(face_list)):
            left = int(face_list[i]['location']['left'])
            top = int(face_list[i]['location']['top'])
            width = int(face_list[i]['location']['width'])
            height = int(face_list[i]['location']['height'])

            cv2.rectangle(img, (left, top), (left+width, top+height), blue, 1)
            font = cv2.FONT_HERSHEY_COMPLEX
            beauty = str(face_list[i]['beauty'])
            # 字体标注的位置， 内容，字体设置
            red = (255, 0, 0)
            cv2.putText(img, beauty, (left+ int(width/2), top-3), font, 0.5, red, 1)
            i = i + 1
        cv2.namedWindow("defect_result", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("defect_result", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        (filepath, tempfilename) = os.path.split(self.img_src)
        (filename, extension) = os.path.splitext(tempfilename)
        img_save_path = 'G:/img'+tempfilename
        cv2.imencode('.jpg', img)[1].tofile(img_save_path)
        #cv2.imwrite(img_save_path, img)


if __name__ == '__main__':
    while True:
        img_src = input('请输入需要检测的本地图片路径:')
        if img_src == '0':
            break
        baiduDetect = BaiduPicIndentify(img_src)
        baiduDetect.detect_face()
