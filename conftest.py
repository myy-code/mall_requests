def pytest_configure(config):
    # 确保 allure 报告输出到项目根目录下的 reports/
    # 不管从哪个目录运行 pytest，都不会在 testcases/ 下生成 reports/
    if config.option.allure_report_dir:
        config.option.allure_report_dir = str(
            config.rootpath / config.option.allure_report_dir
        )
