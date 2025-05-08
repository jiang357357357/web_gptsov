import os
import shutil
import time
from gradio_client import Client, file
from train_music import Check_text,train_model

#
class Make_modle:
    def __init__(self, client):
        # 链接
        self.client = client
        self.make_client = None
        
    # 选择模型并且打开
    def use_music_http(self,
                       gpt="",
                       sovits="",
                       enabled=False
                       ):
        make_result = self.client.predict(
            bert_path="GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large",
            cnhubert_base_path="GPT_SoVITS/pretrained_models/chinese-hubert-base",
            gpu_number="0",
            gpt_path=f"GPT_weights_v2/{gpt}.ckpt",
            sovits_path=f"SoVITS_weights_v2/{sovits}.pth",
            batched_infer_enabled=enabled,
            api_name="/change_tts_inference"
        )
        print("打开声音推理") 
        print(make_result)   
        return make_result
    
    def start_clent(self):
        self.make_client = Client("http://localhost:9872/")
    
    # 语音合成
    def synthesis_music(self,
                        wav_path=file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
                        wav_text="",
                        wav_language="中文",
                        pro_text="",
                        pro_language="中文",
                        music_speed=1,
                        ref_if_wav=False,
                        ):
        file_path = self.make_client.predict(
            ref_wav_path=wav_path,
            prompt_text=wav_text,
            prompt_language=wav_language,
            text=pro_text,
            text_language=pro_language,
            how_to_cut="凑四句一切",
            top_k=15,
            top_p=1,
            temperature=1,
            ref_free=False,
            speed=music_speed,
            if_freeze=ref_if_wav,
            inp_refs=[],
            api_name="/get_tts_wav"
        )
        print("文件路径")
        print(file_path)
        self.file_walk(file_path, "req/get")
        music_path = os.path.join("req/get", "audio.wav")
        return music_path
    
    # 切换模型
    def switch_model(self, gpt, sovits):
        gpt_result = self.make_client.predict(
            gpt_path=f"GPT_weights_v2/{gpt}.ckpt",
            api_name="/change_gpt_weights"
        )
        sovits_result = self.make_client.predict(
            sovits_path=f"SoVITS_weights_v2/{sovits}.pth",
            prompt_language="中文",
            text_language="中文",
            api_name="/change_sovits_weights"
        )
    
    
    # 辅助方法，用来移动文件和删除
    def file_walk(self, old_path,now_path):
        # 获取当前移动目录
        target_path = os.path.join(now_path, "audio.wav")
        # 移动文件
        try:
            shutil.move(old_path, target_path)
            print(f"文件已移动到: {target_path}")
        except FileNotFoundError:
            print("文件未找到，请检查路径！")
        except Exception as e:
            print(f"移动文件出错: {e}")
            
        # 获取上层文件夹路径（要删除的文件夹）
        folder_to_delete = os.path.dirname(old_path)  # 直接父目录
        shutil.rmtree(folder_to_delete)
        print(f"文件夹 {folder_to_delete} 已删除")
            
if __name__ == "__main__":
    check_text = Check_text()
    # check_text.check_choice()
    # 查看基础信息
    make_modle = Make_modle(check_text.client)
    
    req = make_modle.use_music_http(sovits='SoVITS_weights_v2/缪尔赛斯_e8_s184.pth',
                                    gpt='GPT_weights_v2/缪尔赛斯-e15.ckpt')
    time.sleep(30)
    if req:
        make_modle.start_clent()
        print("打开声音推理成功")
        req = make_modle.synthesis_music(
            wav_path=file('req/test_wav/平常.wav'),
            pro_text="当然可以",
            ref_if_wav=True
        )
        print(req)
    
    