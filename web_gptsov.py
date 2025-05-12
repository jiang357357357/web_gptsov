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

dict = {'缪尔赛斯' : {
        '平常': '你就得做什么了，博士，哎呀，现在反悔已经来不及了',
        '低沉': '表情一点都不可爱，算了，我们换个话题',
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
    id: int
    gpt: str
    sovits: str

# 定义获取声音的请求体模型
class DataItem(BaseModel):
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
    # 从请求体获取信息
    item_id = item.id
    item_content = item.content
    item_gpt = item.gpt
    item_sovits = item.sovits
    make_modle.use_music_http(sovits=item_sovits,
                                gpt=item_gpt)
    return {"status": "OK",
            "message": "服务跑得飞快～别怀疑我的能力！"}

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=50042)