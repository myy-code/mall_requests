pipeline {
    agent any

    environment {
        TEST_BASE_URL    = credentials('TEST_BASE_URL')
        TEST_USERNAME    = credentials('TEST_USERNAME')
        TEST_PASSWORD    = credentials('TEST_PASSWORD')
        TEST_DB_HOST     = credentials('TEST_DB_HOST')
        TEST_DB_PORT     = credentials('TEST_DB_PORT')
        TEST_DB_USER     = credentials('TEST_DB_USER')
        TEST_DB_PASSWORD = credentials('TEST_DB_PASSWORD')
        TEST_DB_DATABASE = credentials('TEST_DB_DATABASE')
    }

    stages {
        stage('环境准备') {
            steps {
                bat '"C:/Users/LENOVO/AppData/Local/Programs/Python/Python311/python.exe" -m pip install --upgrade pip'
                bat '"C:/Users/LENOVO/AppData/Local/Programs/Python/Python311/python.exe" -m pip install -r requirements.txt'
            }
        }

        stage('生成环境配置') {
            steps {
                script {
                    def cfg = """test:
  base_url: ${TEST_BASE_URL}
  username: ${TEST_USERNAME}
  password: ${TEST_PASSWORD}
  db_host: ${TEST_DB_HOST}
  db_port: ${TEST_DB_PORT}
  db_user: ${TEST_DB_USER}
  db_password: ${TEST_DB_PASSWORD}
  db_database: ${TEST_DB_DATABASE}"""
                    writeFile file: 'config/env_local.yaml', text: cfg
                }
            }
        }

        stage('冒烟测试') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    bat '"C:/Users/LENOVO/AppData/Local/Programs/Python/Python311/Scripts/pytest.exe" -m smoke -v --junitxml=reports/junit.xml --alluredir=reports/allure-results --tb=short'
                }
            }
        }

        stage('生成Allure报告') {
            steps {
                bat '"C:\\Users\\LENOVO\\AppData\\Local\\allure-2.32.2\\bin\\allure.bat" generate reports/allure-results -o reports/allure-report --clean'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/*.xml', allowEmptyArchive: true
        }
        success {
            echo '✅ 冒烟测试全部通过'
        }
        failure {
            echo '❌ 测试有失败，查看 Allure 报告定位'
        }
    }
}