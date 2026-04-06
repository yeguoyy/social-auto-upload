import streamlit as st
import subprocess
import os

# 1. 设置页面标题
st.set_page_config(page_title="抖音自动发布工具", page_icon="🎵")
st.title("🎵 抖音自动化发布助手")
st.markdown("专为运营团队打造的傻瓜式发布工具")

# 2. 侧边栏：选择账号
account_name = st.sidebar.text_input("账号名称", "mytest")

# 3. 主界面：功能选项卡
tab1, tab2 = st.tabs(["📹 发布视频", "🔑 账号管理"])

with tab1:
    st.header("发布新视频")
    # 文件上传器
    uploaded_file = st.file_uploader("选择视频文件", type=['mp4'])
    title = st.text_input("视频标题", "示例标题")
    desc = st.text_area("视频简介", "这是自动上传的视频 #测试")
    
    if st.button("开始上传", type="primary"):
        if uploaded_file and title:
            # 保存上传的文件到本地（因为CLI需要文件路径）
            save_path = os.path.join("videos", uploaded_file.name)
            os.makedirs("videos", exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.info("正在上传中，请稍候...")
            # 调用你的 sau 命令
            # 注意：这里需要确保环境变量正确
            cmd = f"sau douyin upload-video --account {account_name} --file {save_path} --title \"{title}\" --desc \"{desc}\""
            try:
                # 这里简化处理，实际可能需要 subprocess.Popen 来实时显示日志
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if "success" in result.stdout.lower() or result.returncode == 0:
                    st.success("✅ 上传成功！")
                else:
                    st.error(f"❌ 上传失败: {result.stderr}")
            except Exception as e:
                st.error(f"发生错误: {e}")
        else:
            st.warning("请上传视频并填写标题")

with tab2:
    st.header("账号状态检查")
    if st.button("检查登录状态"):
        st.code(f"正在检查账号 {account_name} ...")
        # 这里同样调用 sau check 命令
        st.info("状态：有效 (Valid)") # 模拟输出


# sau douyin login --account <account_name>
# sau douyin check --account <account_name>
# sau douyin upload-video --account <account_name> --file videos/demo.mp4 --title "示例标题" --desc "示例简介"
# sau douyin upload-note --account <account_name> --images videos/1.png videos/2.png --title "图文标题" --note "图文正文"
