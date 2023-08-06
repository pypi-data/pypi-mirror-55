import os, hmac, hashlib, base64, time, uuid, json
import requests
import pymysql
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import logging

#上传文件到腾讯云cos，需要安装腾讯云cos包
# pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -U cos-python-sdk-v5

class COSImageUploader:
	def __init__(self):
		self._bucket = 'mtime-1252014125'
		secret_id = "AKIDFQRHzVkCIC2iCUoVEm7HG5iATaWFA9JH"
		secret_key = "wjLky0sdCcqsmU0KaifQ3YiiW9dv1vd9"
		region = 'ap-guangzhou'     # 替换为用户的 Region
		scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
		config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Scheme=scheme)
		# 2. 获取客户端对象
		self.client = CosS3Client(config)

	#上传文件到腾讯云cos
	# file：要上传的文件
	# cos_path: cos上保存文件的路径+文件名
	# return: 成功返回 cos_path, 失败返回空字符串。
	def upload_image(self, file, cos_path):
		response = self.client.put_object_from_local_file(
		    Bucket=self._bucket,
		    LocalFilePath=file,
		    Key=cos_path
		)
		print(response)
		return cos_path;
