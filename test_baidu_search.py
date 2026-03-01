import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import platform


def test_baidu_search():
    """百度搜索自动化测试：PyCharm本地运行版（手动指定驱动）"""
    # 初始化Chrome配置
    chrome_options = webdriver.ChromeOptions()

    # ========== 核心配置（按需修改）==========
    # 1. 代理配置（如果本地需要代理才能上网，取消注释并修改代理地址）
    # chrome_options.add_argument('--proxy-server=http://127.0.0.1:7890')  # Clash默认代理
    # chrome_options.add_argument('--proxy-server=http://公司代理IP:端口')  # 公司内网代理

    # 2. 基础配置（无需修改）
    chrome_options.add_argument('--no-sandbox')  # 兼容Windows/Linux
    chrome_options.add_argument('--disable-dev-shm-usage')  # 解决资源限制
    chrome_options.add_argument('--disable-gpu')  # Windows系统禁用GPU加速（避免报错）
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 屏蔽无用日志

    # 3. 手动指定ChromeDriver路径（关键：替换为你实际的驱动路径）
    driver_path = r"C:\Users\Administrator\AppData\Local\Programs\Python\Python313\chromedriver.exe"  # 你的chromedriver.exe路径
    driver_service = Service(executable_path=driver_path)

    # 初始化浏览器
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)

    try:
        # 设置超时时间（避免网络卡顿导致卡死）
        driver.set_page_load_timeout(30)  # 页面加载超时30秒
        driver.implicitly_wait(10)  # 元素定位隐式等待10秒

        # 1. 访问百度首页
        print("=== 开始访问百度首页 ===")
        driver.get("https://www.baidu.com")
        # 验证首页加载成功（通过百度logo定位）
        driver.find_element(By.ID, "lg")
        print("✅ 百度首页加载成功")

        # 2. 输入搜索关键词
        print("=== 输入搜索关键词：Jenkins ===")
        search_box = driver.find_element(By.ID, "chat-textarea")
        search_box.clear()  # 清空搜索框（避免默认内容）
        search_box.send_keys("Jenkins")
        time.sleep(1)  # 输入后稍等（模拟人工操作）

        # 3. 点击搜索按钮
        print("=== 点击搜索按钮 ===")
        search_btn = driver.find_element(By.ID, "chat-submit-button")
        search_btn.click()
        time.sleep(2)  # 等待搜索结果加载

        # 4. 验证搜索结果
        print("=== 验证搜索结果 ===")
        # 验证页面标题包含Jenkins
        assert "Jenkins" in driver.title, f"❌ 页面标题异常，当前标题：{driver.title}"
        print("✅ 搜索结果页面标题验证通过")

        # 验证第一个搜索结果包含Jenkins
        first_result = driver.find_element(By.XPATH, '//div[@id="content_left"]/div[1]')
        assert "Jenkins" in first_result.text, "❌ 第一个搜索结果未包含Jenkins"
        print("✅ 第一个搜索结果验证通过")

        print("\n🎉 所有测试步骤执行成功！")

    except Exception as e:
        print(f"\n❌ 测试执行失败：{str(e)}")
        # 截图保存（可选，失败时保存页面截图到当前目录）
        driver.save_screenshot("baidu_search_error.png")
        print("📸 错误截图已保存为：baidu_search_error.png")
        raise  # 抛出异常，让pytest标记用例失败
    finally:
        # 关闭浏览器
        print("\n=== 关闭浏览器 ===")
        driver.quit()
        print("✅ 浏览器已正常关闭")


# 本地运行入口（PyCharm中直接运行此文件即可）
if __name__ == "__main__":
    # 指定编码（解决Windows控制台中文乱码）
    import sys

    if platform.system() == "Windows":
        sys.stdout.reconfigure(encoding='utf-8')

    # 运行测试用例（-v 显示详细日志）
    pytest.main(["-v", __file__])