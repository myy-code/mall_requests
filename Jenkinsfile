import groovy.json.JsonOutput

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

    triggers {
        cron('H 7 * * 1-5')
    }

    stages {
        stage('环境准备') {
            steps {
                bat '''
                    "C:/Users/LENOVO/AppData/Local/Programs/Python/Python311/python.exe" -m pip install --upgrade pip
                '''
                bat '''
                    "C:/Users/LENOVO/AppData/Local/Programs/Python/Python311/python.exe" -m pip install -r requirements.txt
                '''
            }
        }

        stage('生成环境配置') {
            steps {
                script {
                    def cfg = """test:
                        |  base_url: ${TEST_BASE_URL}
                        |  username: ${TEST_USERNAME}
                        |  password: ${TEST_PASSWORD}
                        |  db_host: ${TEST_DB_HOST}
                        |  db_port: ${TEST_DB_PORT}
                        |  db_user: ${TEST_DB_USER}
                        |  db_password: ${TEST_DB_PASSWORD}
                        |  db_database: ${TEST_DB_DATABASE}""".stripMargin()
                    writeFile file: 'config/env_local.yaml', text: cfg
                }
            }
        }

        stage('冒烟测试') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    bat '''
                        "C:/Users/LENOVO/AppData/Local/Programs/Python/Python311/Scripts/pytest.exe" ^
                            -m smoke ^
                            -v ^
                            -n auto ^
                            --junitxml=reports/junit.xml ^
                            --alluredir=reports/allure-results ^
                            --tb=short
                    '''
                }
            }
        }

        stage('生成Allure报告') {
            steps {
                allure includeProperties: false,
                      results: [[path: 'reports/allure-results']]
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/junit.xml', allowEmptyArchive: true
        }
        success {
            script {
                try {
                    def results = parseTestResults()
                    sendWeCom('success', results)
                } catch (Exception e) {
                    echo "发送通知失败: ${e.message}"
                }
            }
        }
        failure {
            script {
                try {
                    def results = parseTestResults()
                    sendWeCom('failure', results)
                } catch (Exception e) {
                    echo "发送通知失败: ${e.message}"
                }
            }
        }
    }
}

def parseTestResults() {
    try {
        def xml = readFile file: 'reports/junit.xml'
        // 用字符串查找替代 XmlSlurper，避免 Jenkins 安全沙箱限制
        def extract = { attr ->
            def key = "${attr}=\""
            def start = xml.indexOf(key)
            if (start < 0) return '0'
            start += key.length()
            xml.substring(start, xml.indexOf('"', start))
        }
        def total   = extract('tests').toInteger()
        def failures = extract('failures').toInteger()
        def errors  = extract('errors').toInteger()
        def skipped = extract('skipped').toInteger()
        def passed  = total - failures - errors - skipped
        return [total: total, passed: passed, failed: failures + errors, skipped: skipped]
    } catch (Exception e) {
        echo "解析测试结果失败: ${e.message}"
        return null
    }
}

def sendWeCom(status, results) {
    withCredentials([string(credentialsId: 'WECOM_WEBHOOK', variable: 'WECOM_WEBHOOK')]) {
        def content = ''
        if (results) {
            def passRate = results.total > 0 ? Math.round(results.passed * 100f / results.total) : 0
            if (status == 'success') {
                content = """✅ 冒烟测试通过
> 项目: ${env.JOB_NAME}
> 通过率: ${passRate}% (${results.passed}/${results.total})
> 构建: #${env.BUILD_NUMBER}
> 报告: [Allure Report](${env.BUILD_URL}allure/)"""
            } else {
                content = """❌ 冒烟测试失败
> 项目: ${env.JOB_NAME}
> 通过率: ${passRate}% (${results.passed}/${results.total})
> 失败: ${results.failed} 个用例
> 构建: #${env.BUILD_NUMBER}
> 日志: [Console](${env.BUILD_URL}console)
> 报告: [Allure Report](${env.BUILD_URL}allure/)"""
            }
        } else {
            def icon = status == 'success' ? '✅' : '❌'
            content = "${icon} ${env.JOB_NAME} #${env.BUILD_NUMBER} ${status == 'success' ? '通过' : '失败'}"
        }

        def payload = JsonOutput.toJson([
            msgtype: 'markdown',
            markdown: [content: content]
        ])

        writeFile file: 'wecom_payload.json', text: payload
        bat 'powershell -Command "Invoke-RestMethod -Uri %WECOM_WEBHOOK% -Method Post -ContentType \'application/json\' -InFile wecom_payload.json"'
        bat 'if exist wecom_payload.json del wecom_payload.json'
    }
}
