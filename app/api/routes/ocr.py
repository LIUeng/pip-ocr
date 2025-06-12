from paddleocr import PaddleOCR
from fastapi import APIRouter
from PIL import Image
import os

router = APIRouter(prefix="/ocr")
global_ocr = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False, text_det_unclip_ratio=1)

# 获取图片大小、尺寸
def get_image_det(input: str):
    result = {}
    
    result['size'] = os.path.getsize(input)
    img_info = Image.open(input)
    originWidth,originHeight = img_info.size

    result['originWidth'] = originWidth
    result['originHeight'] = originHeight
    
    return result

# 保存输出数据
def save_image_det_json(input: str):
    ocr = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False)
    result = ocr.predict(input=input)
    for res in result:
        res.save_to_json("output")

# 识别文字信息数据格式转换
def get_image_ocr(input: str):
    result = global_ocr.predict(input=input)

    _result = get_image_det(input)
    for res in result:
        locations = []
        # 识别的文字
        rec_texts = res["rec_texts"]
        # 文字四个方向的坐标信息
        rec_boxes = res["rec_boxes"]
        # 匹配度 0<x<1 接近1说明识别度越高
        rec_scores = res['rec_scores']
        for i, v in enumerate(rec_boxes):
            [left, top, right, bottom] = v
            locations.append({
                "text": rec_texts[i],
                "x": float(left),
                "y": float(top),
                "width": float(right - left),
                "height": float(bottom - top),
                "confidence": float(rec_scores[i])
            })
        _result["locations"] = locations

    return _result

# fast api
@router.get("/image")
def read_root():
    try:
        data = get_image_ocr("images/test.jpg")
        return {
            "status": "success",
            "data": data
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }