from gradio_client import Client
from enum import Enum

# 定义枚举类型
class ASRModel(Enum):
    DAMO_ASR = "达摩 ASR (中文)"
    FASTER_WHISPER = "Faster Whisper (多语种)"

class ASRLanguage(Enum):
    ZH = "zh"
    YUE = "yue"


# 查看信息的类
class Check_text:
    def __init__(self, http_text="http://localhost:9874/"):
        # 开始链接
        self.client = Client(http_text)
        self.file_path = "模型列表.txt"

    def check_choice(self, lang_text="达摩 ASR (中文)",):
        # 获取能选的语言项
        # 下面是可选的语言项
        # "达摩 ASR (中文)"
        # "Faster Whisper (多语种)"
        lang_result = self.client.predict(
            key=lang_text,
            api_name="/change_lang_choices"
        )
        
        # 获取能选的语言模型
        lang_size_result = self.client.predict(
            key=lang_text,
            api_name="/change_size_choices"
        )
        
        # 获取能选的数据精度
        lang_pre_result = self.client.predict(
            key=ASRModel.DAMO_ASR.value,
		    api_name="/change_precision_choices"
        )
        
        
        modle_result = self.client.predict(
		api_name="/change_choices"
        )
        
        print("可选语言项")
        print(lang_result) 

        print("可选语言模型大小")
        print(lang_size_result)
        
        print("可选数据精度")
        print(lang_pre_result)
        
        print("可选的模型")
        with open(self.file_path, 'w', encoding='utf-8') as file:
            for x in modle_result:
                # print(type(x))
                # 这里的x对应不同的模型分类，SoVITS模型列表和GPT模型列表
                y = x['choices']
                for a_mod in y:
                    print(a_mod[0])
                    file.write(f"{a_mod[0]}\n")
                file.write("\n")

# 训练模型的类
class train_model:
    def __init__(self,
                 client,
                 inp_path,
                 asr_path,
                 ):
        
        # 链接
        self.client = client
        
        # 输入的音乐文件路径
        self.inp_path = inp_path 
        
        # 输出的asr文件路径
        self.asr_opt_dir = asr_path


    # asr的训练
    def train_asr(self,
                # 语言模型
                asr_model=ASRModel.DAMO_ASR.value,
                # 语言模型大小
                model_size="large",
                # 语言
                lang=ASRLanguage.ZH.value,
                # 语音模型精度
                asr_precision="float32"
                ):
        asr_result = self.client.predict(
            # 输入的音乐文件路径
            asr_inp_dir=self.inp_path,
            asr_opt_dir=self.asr_opt_dir,
            asr_model=asr_model,
            asr_model_size=model_size,
            asr_lang=lang,
            asr_precision=asr_precision,
            api_name="/open_asr"
        )
        print("asr的训练结果")
        print(asr_result)
    
    # 音乐文件的切分
    def train_slicer(self,
            # 输出的切分文件
            slicer_opt_path,
            # 切分的时候，确认音量小于这个值视作静音的备选切割点
            threshold="-34",
            # 每段最小多长
            min_length="4000",
            # 最短切割间隔
            min_interval="300",
            # 怎么算音量曲线，越小精度越大计算量越高
            hop_size="10",
            # 切完后静音最多留多长
            max_sil_kept="500",
            # 归一化后最大值多少
            _max=0.9,
            # 混多少比例归一化后音频进来
            alpha=0.25,
            # 切割使用的进程数
            n_parts=4,
        ):
        # 音乐文件的切分
        slice_result = self.client.predict(
            inp=self.inp_path,
            opt_root=slicer_opt_path,
            threshold=threshold,
            min_length=min_length,
            min_interval=min_interval,
            hop_size=hop_size,
            max_sil_kept=max_sil_kept,
            _max=_max,
            alpha=alpha,
            n_parts=n_parts,
            api_name="/open_slice"
        )
        print("slice的训练结果")
        print(slice_result)
        
    # 模型一键三连
    def train_abc(self):
        abc_result = self.client.predict(
            inp_text=self.asr_opt_dir,
            inp_wav_dir=self.slicer_opt_dir,
            exp_name="xxx",
            gpu_numbers1a="0-0",
            gpu_numbers1Ba="0-0",
            gpu_numbers1c="0-0",
            bert_pretrained_dir="GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large",
            ssl_pretrained_dir="GPT_SoVITS/pretrained_models/chinese-hubert-base",
            pretrained_s2G_path="GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s2G2333k.pth",
            api_name="/open1abc"
        )
        print("abc的训练结果")
        print(abc_result)
    
    # 训练SoVITS模型
    def train_sovits(self,
                     # 每张显卡的batch_size
                     size=3,
                     # 总训练轮数total_epoch
                     epoch=8,
                     # 模型名
                     name="xxx",
                     # 文本模块学习率权重
                     rate=0.4,
                     # 保存频率
                     save_epoch=4
                     ):
        sovits_result = self.client.predict(
            batch_size=size,
            total_epoch=epoch,
            exp_name=name,
            text_low_lr_rate=rate,
            if_save_latest=True,
            if_save_every_weights=True,
            save_every_epoch=save_epoch,
            gpu_numbers1Ba="0",
            pretrained_s2G="GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s2G2333k.pth",
            pretrained_s2D="GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s2D2333k.pth",
            api_name="/open1Ba"
        )
        print("sovits的训练结果")
        print(sovits_result)
    
     # 训练gpt模型
    def train_gpt(self,
                     # 每张显卡的batch_size
                     size=3,
                     # 总训练轮数total_epoch
                     epoch=8,
                     # 模型名
                     name="xxx",
                     # 保存频率
                     save_epoch=4
                     ):
        gpt_result = self.client.predict(
            batch_size=size,
            total_epoch=epoch,
            exp_name=name,
            if_dpo=False,
            if_save_latest=True,
            if_save_every_weights=True,
            save_every_epoch=save_epoch,
            gpu_numbers="0",
            pretrained_s1="GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s1bert25hz-5kh-longer-epoch=12-step=369668.ckpt",
            api_name="/open1Bb"
        )
        print("gpt的训练结果")
        print(gpt_result)
        
    
    
    
if __name__ == "__main__":
    check_text = Check_text("http://localhost:9874/")
    check_text.check_choice()