import base64
import json
import requests
import os
import cv2
from PIL import Image


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
        print(path)
        with open(path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            return base64_data

    def detect_face(self):
        # 人脸检测与属性分析
        img_BASE64 = self.img_to_BASE64(self.img_src)
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
            #print("位 置：", face_list[i]['location']['left'], face_list[i]['location']['top'],
            #face_list[i]['location']['width'], face_list[i]['location']['height'] )
            i = i+1
        img_path = os.path.abspath(self.img_src)
        img = cv2.imread(img_path)
        blue = (65, 105, 225)
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
            red = (176, 23, 31)
            cv2.putText(img, beauty, (left+ int(width/2), top-3), font, 0.5, red, 1)
            i = i + 1
        cv2.namedWindow(self.img_src, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(self.img_src, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        img_save_path = 'G:/'+self.img_src
        cv2.imwrite(img_save_path, img)


if __name__ == '__main__':
    while True:
        img_src = input('请输入需要检测的本地图片路径:')
        if img_src == '0':
            break
        baiduDetect = BaiduPicIndentify(img_src)
        baiduDetect.detect_face()
