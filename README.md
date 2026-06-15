# 电商管理后台 API 自动化测试框架

基于 **API 分层设计** 的接口自动化测试框架，使用 Python + Requests + Pytest 构建，实现对电商管理后端的核心接口覆盖。

## 项目简介

本项目是一个典型的 API 自动化测试框架，采用分层架构设计，将请求封装、业务逻辑、测试数据与用例执行分离，提高代码的可维护性和复用性。目前已覆盖用户认证与用户管理两大模块的核心接口，包含登录、注册、用户 CRUD、角色分配等功能。

## 技术栈

- **编程语言**: Python
- **测试框架**: Pytest
- **HTTP 客户端**: Requests
- **测试报告**: Allure Report
- **数据驱动**: PyYAML + Pandas/Openpyxl (支持 YAML 和 Excel)
- **数据库校验**: PyMySQL
- **日志**: logging (TimedRotatingFileHandler)

## 项目结构

```
mall_requests/
├── api/                          # API 层
│   ├── __init__.py
│   ├── base_api.py              # API 基类，封装 Session、Token、统一请求方法
│   └── user_api.py              # 用户模块 API 封装（登录/注册/CRUD/角色）
├── config/                       # 配置层
│   ├── __init__.py
│   ├── config.py                # Settings 类，读取 YAML 配置
│   ├── env.yaml                 # 环境配置模板
│   └── env_local.yaml           # 本地环境配置（实际账号，已 gitignore）
├── data/                         # 测试数据层
│   ├── __init__.py
│   └── user_api_data/
│       ├── login_data.yaml          # 登录测试数据
│       ├── register_test_data.yaml  # 注册测试数据
│       └── api_test_data.xlsx       # Excel 数据驱动
├── utils/                        # 工具层
│   ├── __init__.py
│   ├── data_loader.py           # 数据加载器（YAML / Excel）
│   ├── db_utils.py              # 数据库工具类（PyMySQL 封装）
│   └── logger.py                # 日志配置（控制台 + 文件滚动）
├── test_cases/                   # 测试用例层
│   ├── __init__.py
│   ├── conftest.py              # Pytest 夹具（API 客户端 / Token / Allure 日志 / 数据库连接）
│   └── API/
│       ├── __init__.py
│       └── test_user_api.py     # 用户模块测试用例
├── conftest.py                   # 根目录 Pytest 配置（Allure 报告路径）
├── pytest.ini                    # Pytest 全局配置
├── requirements.txt              # 项目依赖
├── logs/                         # 日志目录（自动按天滚动，保留 7 天）
└── reports/                      # 测试报告目录
    └── allure-results/           # Allure 原始数据
```

## 已实现的测试用例

### 1. 登录模块 (test_user_api.py :: TestUserLogin)
- ✅ 登录成功（数据驱动，支持 YAML / Excel 双数据源）
- ✅ 登录成功后有 Token，能正常获取用户信息
- ✅ 登出

### 2. 注册模块 (test_user_api.py :: TestUserLogin)
- ✅ 正常注册（含数据库校验）
- ✅ 用户名已存在
- ✅ 用户名为空
- ✅ 密码为空
- ✅ 邮箱格式错误

### 3. Token 管理
- ✅ 刷新 Token
- ✅ 携带 Token 访问受保护接口

### 4. 用户管理
- ✅ 分页查询用户列表（支持关键字筛选）
- ✅ 获取指定用户信息
- ✅ 修改用户信息（用户名 / 邮箱 / 昵称 / 备注 / 状态）
- ✅ 修改密码
- ✅ 修改用户状态（启用 / 禁用）
- ✅ 删除用户
- ✅ 给用户分配角色
- ✅ 获取指定用户的角色

## 环境准备

### 前置要求
- Python 3.8+
- 被测试的电商管理后端服务已启动

### 安装步骤

1. **安装依赖**
```bash
pip install -r requirements.txt
```

2. **配置测试环境**

   复制 `config/env.yaml` 为 `config/env_local.yaml`，填入实际环境信息：
```yaml
test:
  base_url: "http://localhost:8080"       # 后端服务地址
  username: "admin"                       # 管理员账号
  password: "your_password"               # 管理员密码
  db_host: "localhost"                    # 数据库地址
  db_port: 3307                           # 数据库端口
  db_user: "root"                         # 数据库用户
  db_password: "your_db_password"         # 数据库密码
  db_database: "mall"                     # 数据库名
```

## 运行测试

### 运行所有测试
```bash
pytest
```

### 按标签运行
```bash
pytest -m smoke      # 冒烟测试（核心流程）
pytest -m p0         # P0 级别（阻塞用例）
pytest -m p1         # P1 级别（重要功能）
pytest -m p2         # P2 级别（边缘场景）
```

### 运行指定测试文件
```bash
pytest test_cases/API/test_user_api.py -v
```

### 运行指定测试用例
```bash
pytest test_cases/API/test_user_api.py::TestUserLogin::test_login -v
```

### 数据源切换

测试用例支持 YAML 和 Excel 两种数据源，在测试类中切换注释即可：

```python
# YAML 数据驱动
login_case = load_yaml_data("user_api_data/login_data.yaml", key="login_cases")

# Excel 数据驱动
login_case = read_excel_test_cases(
    "user_api_data/api_test_data.xlsx",
    sheet_name="登录测试数据",
    skiprows=0,
    required_columns=["username", "password"]
)
```

### 生成 Allure 报告
```bash
# 执行测试（自动收集 Allure 数据）
pytest

# 启动 Allure Web 服务查看报告
allure serve reports/allure-results
```

## 测试策略

### 用例分级
- **P0 / Smoke**: 冒烟测试，核心业务路径（登录、注册、登出），失败则阻断发布
- **P1**: 重要功能，常规回归必测（用户 CRUD、角色分配）
- **P2**: 边缘场景（Token 刷新、删除用户等需谨慎操作的功能）

### 数据驱动
- 测试数据与代码完全分离，支持 YAML 和 Excel 双数据源
- 新增用例只需添加数据，无需修改代码

### 数据库校验
- 关键写操作（如注册）自动校验数据库，确保数据一致性
- 使用参数化查询防止 SQL 注入

### 日志与报告
- 控制台实时输出 + 文件按天滚动，保留 7 天
- 测试失败时自动将日志附加到 Allure 报告，方便定位问题
- 支持 Allure 特性/故事/严重级别标记，生成结构化测试报告

## 扩展指南

### 添加新的 API 模块
1. 在 `api/` 下创建新的 API 类，继承 `BaseAPI`
2. 封装对应接口的请求方法
3. 在 `test_cases/conftest.py` 中添加对应的 fixture

### 添加新的测试数据
1. 在 `data/` 下创建 YAML 文件或编辑 Excel 工作表
2. 使用 `load_yaml_data` 或 `read_excel_test_cases` 加载数据
3. 通过 `@pytest.mark.parametrize` 实现数据驱动

### 添加数据库校验
注入 `db` fixture 即可使用 `DBUtils` 进行数据库查询和断言。
