import subprocess

def run_streamlit_app():
    # 运行 streamlit run my_app.py 命令
    subprocess.run(["streamlit", "run", "app.py"])

if __name__ == "__main__":
    run_streamlit_app()