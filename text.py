import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    data = {"emotion": "低沉", "content": "为什么会这样呢"}
    response = requests.get(f"{BASE_URL}/get_music", json=data)
    output_file = "test_downloaded.wav"  # 保存下载的 WAV 文件
    # 检查状态码
    if response.status_code == 200:
        # 保存 WAV 文件
        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    assert response.status_code == 200, "健康检查失败！老哥你服务没跑起来吧～"
    
if __name__ == "__main__":
    print("开始测试API～别怪我吐槽，代码我都写好了！")
    test_health_check()    