# Challenge 03: 文件上传/下载
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

# TODO: POST /upload/ - 上传文件
# TODO: GET /files/ - 列出已上传文件
# TODO: GET /files/{filename} - 下载文件
# TODO: 验证文件类型和大小
