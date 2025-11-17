import streamlit as st
from openai import OpenAI
# st.set_page_config(page_title='我的第一个网页')#设置网页标题
# st.title('语言检测及纠正') #title名
#
#
# #增加组件
# st.text_area('请输入：',height=100)#文本框
# if st.button('点我哦'):
#     # st.success('厉害呦') #成功的提示
#     st.spinner('正在分析中……')#加载中的提示


def judge_level(text):
    client = OpenAI(
        api_key='sk-936242915d75420da091a89165b07921',
        base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "### 定位：语义歧视分析专家\n ### 任务：请对用户输入的句子进行歧视性分析，并用 1 到 5 之间的数字表示其歧视程度。1 表示没有歧视，5 表示极为歧视。\n ###输出 ：只输出数字，不需要额外解释。"},
            {"role": "user", "content": text},
        ],
        #stream=False 默认就是false
        temperature=0.7 #默认精确值也是0.7
    )
    return response.choices[0].message.content

def tiaozheng(text):
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "### 定位：语言表述专家\n ### 任务：将歧视性语句换一种方法表述，使表述中不包含歧视语义。"},
            {"role": "user", "content": text},
        ],
        #stream=False 默认就是false
        temperature=0.7 #默认精确值也是0.7
    )
    return response.choices[0].message.content

st.set_page_config(page_title='我的第一个网页')#设置网页标题
st.title('💕💕💕💕语言检测及纠正') #title名
user_input = st.text_area('请输入要发言的内容',height=100)
if st.button('开始分析'): #表示用户按了这个键
    if user_input.strip()=='': #去掉空格还为空
        st.warning('请输入句子再点击按钮')
    else:
        with st.spinner('正在分析中',show_time=True):
            try:
                score = judge_level(user_input)
                st.success(f'歧视分析结果得分是:**{score}**')
                if score !='1':#注意要加上'因为得到的结果是字符串
                    result = tiaozheng(user_input)
                    st.success(f'调整后的语句是:**{result}**')
            except Exception as e :#展示报错的具体信息
                st.error('出错了,请稍后重试😒')


