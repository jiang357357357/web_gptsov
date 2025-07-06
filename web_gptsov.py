import os
import time
from fastapi import FastAPI
from gradio_client import file
from pydantic import BaseModel
import uvicorn
from fastapi.responses import FileResponse
from pathlib import Path

from train_music import Check_text,train_model
from make_music import Make_modle

# 定义角色-模型映射字典
role_model_map = {
    "缪尔赛斯": {
        "gpt": "缪尔赛斯-e15",
        "sovits": "缪尔赛斯_e8_s184"
    },
    "雾岛遥": {
        "gpt": "雾岛遥-gpt",
        "sovits": "雾岛遥_sovits"
    },
    "玛恩纳": {
        "gpt": "玛恩纳_二版-e20",
        "sovits": "玛恩纳_二版_e16_s336"
    }
    # 可以继续添加其他角色
}

dict = {
    '缪尔赛斯' : {
        '平常': '你就得做什么了，博士，哎呀，现在反悔已经来不及了',
        '低沉': '表情一点都不可爱，算了，我们换个话题',
        '开心': '开心',
        '生气': '生气',
        '悲伤': '悲伤',
        '惊讶': '惊讶',
        '无聊': '无聊',
        '害怕': '害怕',
        '失落': '失落'
    },
    "玛恩纳": {
        '平常': '只有被允许的成功。看来玛嘉烈还保留着那个闹剧里的绰号',
        '低沉': '玛恩纳，你今天看起来很失落啊',
        '开心': '开心',
        '生气': '生气',
        '悲伤': '悲伤',
        '惊讶': '惊讶',
        '无聊': '无聊',
        '害怕': '害怕',
        '失落': '失落'
    }
}

now_model = '缪尔赛斯'

app = FastAPI()

# 定义切换模型的请求体模型
class SwitchItem(BaseModel):
    role: str

# 定义获取声音的请求体模型
class DataItem(BaseModel):
    emotion: str
    content: str

# 定义指定角色获取声音的请求体模型
class RoleDataItem(BaseModel):
    role: str
    emotion: str
    content: str

# 开始运行
check_text = Check_text()
# check_text.check_choice()
# 查看基础信息
make_modle = Make_modle(check_text.client)
make_modle.use_music_http(sovits='缪尔赛斯_e8_s184',
                                gpt='缪尔赛斯-e15')
time.sleep(30)
make_modle.start_clent()

# 

# 切换模型
@app.post("/switch_model")
async def switch_model(item: SwitchItem):
    global now_model
    role = item.role
    if role not in role_model_map:
        return {"status": "error", "message": f"角色 {role} 不存在"}
    
    now_model = role
    item_gpt = role_model_map[role]["gpt"]
    item_sovits = role_model_map[role]["sovits"]
    make_modle.switch_model(gpt=item_gpt, sovits=item_sovits)
    return {"status": "OK",
            "message": f"已切换到角色 {role}，服务跑得飞快～别怀疑我的能力！"}

# 获取声音
@app.post("/get_music")
async def switch_model(item: DataItem):
    # 从请求体获取信息
    item_emotion = item.emotion
    item_content = item.content
    music_path = make_modle.synthesis_music(
            wav_path = file(os.path.join(f'pro_music/{now_model}', f'{item_emotion}.wav')),
            wav_text=dict[now_model][item_emotion],
            pro_text=item_content,
            ref_if_wav=False
        )
    # 返回文件
    return FileResponse(
        path=music_path,
        filename="audio.wav",  # 客户端下载时的文件名
        media_type="audio/wav"      # MIME 类型
    )

# 获取指定角色的声音
@app.post("/get_role_music")
async def get_role_music(item: RoleDataItem):
    # 从请求体获取信息
    role = item.role
    item_emotion = item.emotion
    item_content = item.content
    
    # 检查角色是否存在
    if role not in role_model_map:
        return {"status": "error", "message": f"角色 {role} 不存在"}
    
    # 检查角色是否有对应的情感配置
    if role not in dict:
        return {"status": "error", "message": f"角色 {role} 没有配置情感数据"}
    
    # 检查情感是否存在
    if item_emotion not in dict[role]:
        return {"status": "error", "message": f"角色 {role} 没有 {item_emotion} 情感配置"}
    
    # 临时切换到指定角色的模型
    item_gpt = role_model_map[role]["gpt"]
    item_sovits = role_model_map[role]["sovits"]
    make_modle.switch_model(gpt=item_gpt, sovits=item_sovits)
    
    # 合成音乐
    music_path = make_modle.synthesis_music(
            wav_path = file(os.path.join(f'pro_music/{role}', f'{item_emotion}.wav')),
            wav_text=dict[role][item_emotion],
            pro_text=item_content,
            ref_if_wav=False
        )
    
    # 返回文件
    return FileResponse(
        path=music_path,
        filename=f"{role}_{item_emotion}_audio.wav",  # 客户端下载时的文件名
        media_type="audio/wav"      # MIME 类型
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=50042)