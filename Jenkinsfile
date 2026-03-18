pipeline {
    agent any // 在任何可用的 Jenkins 节点上运行

    stages {
        stage('Checkout Code') {
            steps {
                // 从 GitHub 拉取代码 (Jenkins 会自动处理，这里只是显式声明)
                checkout scm
                echo '代码拉取成功！'
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // 创建虚拟环境 (推荐做法，避免污染服务器全局环境)
                    // 如果 Jenkins 节点是 Linux/Mac
                    sh '''
                        pip3 install --user --upgrade pip
                        pip3 install --user -r requirements.txt
                    '''
                    // 如果是 Windows 节点，命令略有不同:
                    // bat '''
                    //     python -m venv venv
                    //     venv\Scripts\activate
                    //     pip install -r requirements.txt
                    // '''
                }
            }
        }

        stage('Run Tests & Generate Report') {
            steps {
                script {
                    // 激活虚拟环境并运行测试
                    // --junitxml=report.xml 是关键：生成 JUnit 格式的 XML 报告
                    sh '''
                        export PATH=$HOME/.local/bin:$PATH
                        pytest test_baidu_search.py --junitxml=test-results/results.xml -v
                    '''
                }
            }
        }
    }

    post {
        always {
            // 【关键】无论测试成功还是失败，都执行此块来收集报告
            // 告诉 Jenkins 去解析生成的 XML 文件
            sh 'mkdir -p test-results'
            junit allowEmptyResults: true, testResults: 'test-results/*.xml'
        }
        failure {
            echo '构建失败！'
        }
        success {
            echo '构建成功！'
        }
    }
}
