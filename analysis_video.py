# -*- coding: UTF-8 -*-
import cv2
import os
import threadpool

# 常量定义区、
# 查询视频路径
QUERY_VIDEO_PATH = "H:/home/video/006"
# 图片保存路径
IMAGE_SAVE_PATH = "C:/Users/Administrator/Desktop/output/image/"
# 一个视频保存图片数量
IMAGE_SUM = 30
# 线程池数量-文件夹
THREAD_POOL_SUM_FILE = 10
# 线程池数量-图片
THREAD_POOL_SUM_IMAGE = 1


# 定义保存图片函数
# image:要保存的图片名字
# addr；图片地址与相片名字的前部分
# num: 相片，名字的后缀。int 类型
def save_image(video):

    # 获取视频
    video_capture = video.video_capture
    # 设置视频帧位置
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, video.video_frame_position)
    # 读取指定位置的视频帧
    success, frame = video_capture.read()
    # 如果设置帧数读取视频成功保存截图到磁盘
    if success:
        address = video.save_image_path + str(video.video_frame_position) + '.jpg'
        # 不允许中文路径名
        # cv2.imwrite(address, image)
        # 运行中文路径名
        cv2.imencode('.jpg', frame)[1].tofile(address)


def parse_video_frame(video_frame_list):
    thread_pool_processor(video_frame_list, save_image, THREAD_POOL_SUM_IMAGE)


# 读取单个视频
def read_video(video_all_path_name, save_image_path):
    # 读取视频文件
    video_capture = cv2.VideoCapture(video_all_path_name)
    # 通过摄像头的方式
    # videoCapture=cv2.VideoCapture(1)
    # 获取视频总帧数
    frame_num = video_capture.get(7)
    # 一个视频保存30张截图
    image_num = IMAGE_SUM
    # 保留截图的帧数间隔，大视频就间隔大些，小视频就间隔小些
    base_scope = frame_num / image_num

    video_frame_list = []
    for frame_position in range(int(base_scope), int(frame_num), int(base_scope)):
        video_frame = Video(video_capture, save_image_path, frame_position)
        video_frame_list.append(video_frame)
    return video_frame_list


class Video:
    def __init__(self, video_capture, save_image_path, video_frame_position):
        self.video_capture = video_capture
        self.save_image_path = save_image_path
        self.video_frame_position = video_frame_position


# 读取文件夹内容
def read_dir(path):
    # 得到文件夹下的所有文件名称
    files = os.listdir(path)
    thread_pool_processor(files, file_executor, THREAD_POOL_SUM_FILE)


# 线程池执行
def thread_pool_processor(sources, thread_function, thread_sum):
    task_pool = threadpool.ThreadPool(thread_sum)
    requests = threadpool.makeRequests(thread_function, sources)
    [task_pool.putRequest(req) for req in requests]
    # 等待执行完
    task_pool.wait()


def file_executor(file):
    try:
        # 判断是否是文件夹，不是文件夹才打开
        if not os.path.isdir(file):
            # 打开文件
            print(file)
            f = open(QUERY_VIDEO_PATH + "/" + file)
            full_file_name = f.name
            file_name_and_type = os.path.basename(full_file_name)
            file_name, file_type = os.path.splitext(file_name_and_type)
            image_save_path = IMAGE_SAVE_PATH + file_name + "/"
            if not os.path.exists(image_save_path):
                os.makedirs(image_save_path)
                print(file_name + "创建成功")
            video_frame_list = read_video(full_file_name, image_save_path)
            parse_video_frame(video_frame_list)
    except Exception:
        print("thread_executor#read_video")


if __name__ == '__main__':
    read_dir(QUERY_VIDEO_PATH)
