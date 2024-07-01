import cv2
import os
import sys

def resize_with_aspect_ratio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation=inter)
    return resized

def add_padding(image, target_width, target_height):
    (h, w) = image.shape[:2]
    top = bottom = left = right = 0

    if h < target_height:
        delta = target_height - h
        top, bottom = delta // 2, delta // 2

    if w < target_width:
        delta = target_width - w
        left, right = delta // 2, delta // 2

    color = [0, 0, 0]
    new_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return new_image

def video_to_frames(video_file, output_dir, target_width=None, target_height=None, frames_per_second=None, roi_x=0, roi_y=0, roi_width=None, roi_height=None):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    cap = cv2.VideoCapture(video_file)
    frame_count = 0
    output_frame_count = 0

    # 获取视频的原始帧率
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = 1 if frames_per_second is None else int(original_fps / frames_per_second)
    while True:
        success, frame = cap.read()
        if not success:
            break
        # 根据设定的帧率跳过一些帧
        if frame_count % frame_interval == 0:
            if roi_width and roi_height:
                frame = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
            frame = resize_with_aspect_ratio(frame, width=target_width, height=target_height)
            frame = add_padding(frame, target_width, target_height)
            frame_file = os.path.join(output_dir, f"frame_{output_frame_count:05d}.jpg")
            cv2.imwrite(frame_file, frame)
            output_frame_count += 1
        frame_count += 1
    cap.release()
    print(f"Total frames extracted: {output_frame_count}")

if __name__ == "__main__":
    if len(sys.argv) != 10:
        # Usage: python video_to_frames.py [video_file] [output_dir] [target_width] [target_height] [frames_per_second] [roi_x] [roi_y] [roi_width] [roi_height]
        # video_file 视频路径
        # output_dir 图片输出路径
        # target_width 图片输出宽度
        # target_height 图片输出高度
        # frames_per_second 每秒钟输出多少张图片
        # roi_x 截图图片的开始位置x
        # roi_y 截图图片的开始位置y
        # roi_width 高度
        # roi_height 宽度
        print("Usage: python video_to_frames.py [video_file] [output_dir] [target_width] [target_height] [frames_per_second] [roi_x] [roi_y] [roi_width] [roi_height]")
        sys.exit(1)

    video_file = sys.argv[1]
    output_dir = sys.argv[2]
    target_width = int(sys.argv[3])
    target_height = int(sys.argv[4])
    frames_per_second = int(sys.argv[5])
    roi_x = int(sys.argv[6])
    roi_y = int(sys.argv[7])
    roi_width = int(sys.argv[8])
    roi_height = int(sys.argv[9])
    video_to_frames(video_file, output_dir, target_width, target_height, frames_per_second, roi_x, roi_y, roi_width, roi_height)