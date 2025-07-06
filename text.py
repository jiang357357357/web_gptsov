import requests
import json


BASE_URL = "http://localhost:50042"
# BASE_URL = "http://server.xcyyds.top:50042"

def test_health_check():
    data = {
        "role": "玛恩纳",
        "emotion": "平常", 
        "content": "未来也需要你"
    }
    response = requests.post(f"{BASE_URL}/get_role_music", json=data)
    output_file = "test_缪尔赛斯_低沉.wav"  # 保存下载的 WAV 文件
    # 检查状态码
    if response.status_code == 200:
        # 保存 WAV 文件
        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"✅ 测试成功！已保存文件: {output_file}")
    else:
        print(f"❌ 测试失败！状态码: {response.status_code}")
        try:
            error_data = response.json()
            print(f"错误信息: {error_data}")
        except:
            print("无法解析错误信息")
    
    assert response.status_code == 200, "健康检查失败"
    
if __name__ == "__main__":
    print("开始测试指定角色缪尔赛斯的API")
    test_health_check()    