from langchain.text_splitter import CharacterTextSplitter
import re
import logging
from typing import List
from configs.model_config import SENTENCE_SIZE

LOG_FORMAT = "%(levelname) -5s %(asctime)s" "-1d: %(message)s"
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format=LOG_FORMAT)

class QATextSplitter(CharacterTextSplitter):
    def __init__(self, pdf: bool = False, sentence_size: int = 500, **kwargs):
        super().__init__(**kwargs)
        self.pdf = pdf
        self.sentence_size = sentence_size

    def split_text(self, text: str) -> List[str]:   ##此处需要进一步优化逻辑
        text = text.rstrip()  # 段尾如果有多余的\n就去掉它
        ls = [i.replace("#@@#","") for i in re.split(r"(?=#@@#)", text) if i]
        for ele in ls:
            if len(ele) > self.sentence_size:
                ele1 = re.sub(r'([,，.]["’”」』]{0,2})([^,，.])', r'\1\n\2', ele)
                ele1_ls = ele1.split("\n")
                for ele_ele1 in ele1_ls:
                    if len(ele_ele1) > self.sentence_size:
                        ele_ele2 = re.sub(r'([\n]{1,}| {2,}["’”」』]{0,2})([^\s])', r'\1\n\2', ele_ele1)
                        ele2_ls = ele_ele2.split("\n")
                        for ele_ele2 in ele2_ls:
                            if len(ele_ele2) > self.sentence_size:
                                ele_ele3 = re.sub('( ["’”」』]{0,2})([^ ])', r'\1\n\2', ele_ele2)
                                ele2_id = ele2_ls.index(ele_ele2)
                                ele2_ls = ele2_ls[:ele2_id] + [i for i in ele_ele3.split("\n") if i] + ele2_ls[
                                                                                                       ele2_id + 1:]
                        ele_id = ele1_ls.index(ele_ele1)
                        ele1_ls = ele1_ls[:ele_id] + [i for i in ele2_ls if i] + ele1_ls[ele_id + 1:]

                id = ls.index(ele)
                ls = ls[:id] + [i for i in ele1_ls if i] + ls[id + 1:]
        return ls

    if __name__ == '__main__':
        text = split_text("问题:云盾或者iSany扫码之后，手机提示人脸认证成功，或者免人脸登录，电脑二维码没有任何变化\t\t答案:登录页右上角查看服务器地址是否是站点浮动地址（查看周围能扫码登录的电脑登录页右上角\n" +
            "地址，请拨打0731-84038666处理）\n" +
            "问题:进入三一应用市场后，点击“isany”下载，选择浏览器后，不自动跳转进行下载\t\t答案:飞书跳转链接的问题，请飞书联系（伍勇-wuy81）进行处理\n" +
            "问题:iSany和云盾有什么区别？\t\t答案:iSany就是云盾的升级版本，其中里面的扫一扫功能就是云盾的扫一扫功能。\n" +
            "问题:vivo手机在iSany应用中无法上传文件\t\t答案:vivo手机H5读取文件需要悬浮窗权限，权限设置：手机-设置-应用设置中添加权限\n" +
            "问题:鸿蒙手机无法通过点击通知栏的推送打开应用\t\t答案:鸿蒙手机需要打开后台弹窗的权限，点击通知栏的推送才能打开应用")
        logging.info(text)
