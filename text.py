import requests
import json


BASE_URL = "http://localhost:8091"
# BASE_URL = "http://server.xcyyds.top:50042"

def test_health_check():
    data = {"emotion": "低沉", "content": "愿你于此生平安喜乐"}
    response = requests.post(f"{BASE_URL}/get_music", json=data)
    output_file = "test_downloaded.wav"  # 保存下载的 WAV 文件
    # 检查状态码
    if response.status_code == 200:
        # 保存 WAV 文件
        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    assert response.status_code == 200, "健康检查失败"
    
if __name__ == "__main__":
    print("开始测试API～别怪我吐槽，代码我都写好了！")
    test_health_check()    