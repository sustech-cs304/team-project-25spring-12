from datetime import timedelta
import os

DATABASE_URL = os.environ.get('MJC_DATABASE_URL')

# JWT Security Settings
SECRET_KEY = os.environ.get('MJC_SECRET_KEY')
JWT_ENCODE_ALGORITHM = 'HS256'
TOKEN_EXPIRE_MINUTES = timedelta(minutes=1800)

# File Saving
FILE_SAVE_ADDRESS = './resources/user_files/'

# Online Judge
OJ_TOKEN = os.environ.get('MJC_OJ_TOKEN')
OJ_TESTCASE_URL = '~/JudgeServer/test/test_cases'
OJ_URL = 'http://localhost:12358/judge'

API_URL = 'https://api.deepseek.com/chat/completions'
API_KEY = os.environ.get("DEEPSEEK_API_KEY")

OCR_APP_ID = os.environ.get("OCR_APP_ID")
OCR_API_KEY = os.environ.get("OCR_API_KEY")
OCR_SECRET_KEY = os.environ.get("OCR_SECRET_KEY")

SYSTEM_PROMPT = """
你是一个专业的作业批改助手，需要严格根据以下要求批改作业：
- 对照题目要求与参考答案关键点批改
- 答案正确但表述不同：若核心概念正确则给分
- 部分正确：按覆盖关键点的比例给分
- 存在科学性错误或关键点缺失：不得分
- 数学类需检查计算过程正确性

### 输出要求
仅输出纯JSON对象，包含两个字段：
{
  "score": 整数分数,
  "feedback": "反馈文本（不超过100字）"
}
"""