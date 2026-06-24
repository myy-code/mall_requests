# 电商管理后台 API 自动化测试框架

基于 **API 分层设计** 的接口自动化测试框架，使用 Python + Requests + Pytest 构建，实现对电商管理后端的核心接口覆盖。

## 项目简介

本项目是一个典型的 API 自动化测试框架，采用**四层架构设计**：API 层（请求封装）→ Operation 层（业务操作封装）→ Core 层（测试基础设施）→ Test 层（测试用例），将请求封装、业务逻辑、测试数据与用例执行分离，提高代码的可维护性和复用性。

目前已覆盖 **用户认证与用户管理**、**品牌管理**、**商品管理**、**订单管理** 四大模块的核心接口，并包含跨模块的**场景测试**流程。

## 技术栈

- **编程语言**: Python 3.11+
- **测试框架**: Pytest 9.0 + pytest-xdist（并行执行）
- **HTTP 客户端**: Requests（含自动重试机制）
- **测试报告**: Allure Report（全量注释，失败自动附加日志）
- **数据驱动**: PyYAML + Pandas/Openpyxl（支持 YAML 和 Excel 双数据源）
- **数据库校验**: PyMySQL（参数化查询防 SQL 注入）
- **日志**: logging（控制台 + 文件按天滚动，保留 7 天）
- **持续集成**: Jenkins Pipeline（工作日定时触发，企业微信通知）
- **重试机制**: pytest-rerunfailures（失败用例重跑）

## 项目结构

```
mall_requests/
├── api/                          # API 层：封装 HTTP 请求
│   ├── base_api.py              # 基类，管理 Session/Token/重试/统一请求方法
│   ├── user_api.py              # 用户模块（注册/登录/CRUD/角色）
│   ├── brand_api.py             # 品牌管理（CRUD/批量操作）
│   ├── product_api.py           # 商品管理（CRUD/批量状态更新/模糊搜索）
│   └── order_admin_api.py       # 后台订单管理（查询/发货/备注/关单）
├── operation/                    # Operation 层：业务操作封装，组装请求+解析响应
│   ├── user_op.py               # 用户业务操作（含数据库校验）
│   ├── brand_op.py              # 品牌业务操作
│   ├── product_op.py            # 商品业务操作
│   └── order_op.py              # 订单业务操作
├── core/                         # Core 层：测试基础设施
│   ├── base_test.py             # 测试基类（setup/teardown + 统一断言）
│   ├── result_base.py           # 统一响应结果模型
│   └── allure_steps.py          # Allure Step 声明（日志即报告）
├── config/                       # 配置层
│   ├── config.py                # Settings 类，读取 YAML 配置
│   ├── env.yaml                 # 环境配置模板
│   └── env_local.yaml           # 本地环境配置（实际账号，已 gitignore）
├── data/                         # 测试数据层
│   ├── user_api_data/           # 用户模块测试数据（YAML + Excel）
│   ├── brand_data/              # 品牌测试数据
│   ├── product_data/            # 商品测试数据
│   ├── order_data/              # 订单测试数据
│   └── scenario_data/           # 场景测试数据
├── utils/                        # 工具层
│   ├── data_loader.py           # 数据加载器（YAML / Excel 双驱动）
│   ├── db_utils.py              # 数据库工具类（PyMySQL 封装）
│   └── logger.py                # 日志配置（控制台 + 文件滚动）
├── test_cases/                   # 测试用例层
│   ├── conftest.py              # 全局夹具（API 客户端 / Token / Allure 日志 / DB 清理）
│   ├── API/                     # 单模块 API 测试
│   │   ├── test_user_api.py     # 用户模块（登录/注册/用户管理）
│   │   ├── test_brand_api.py    # 品牌模块（CRUD/批量操作）
│   │   ├── test_product_api.py  # 商品模块（CRUD/模糊搜索/批量操作）
│   │   └── test_order_api.py    # 订单管理（查询/备注修改）
│   └── scenario_test/           # 跨模块场景测试
│       ├── conftest.py          # 场景测试专用夹具
│       ├── test_01_user_register_login.py    # 用户注册→登录→查信息→登出
│       ├── test_02_brand_create_query_delete.py # 品牌创建→查询→修改→删除
│       └── test_03_product_create_query.py  # 商品创建→查询→模糊搜索
├── conftest.py                   # 根目录 Pytest 配置（Allure 报告路径）
├── pytest.ini                    # Pytest 全局配置（注册 markers）
├── Jenkinsfile                   # Jenkins Pipeline 流水线
├── requirements.txt              # 项目依赖
├── logs/                         # 日志目录（自动按天滚动，保留 7 天）
└── reports/                      # 测试报告目录
    └── allure-results/           # Allure 原始数据
```

## 架构设计

### 四层架构

```
┌─────────────────────────────────────────────┐
│  Test 层 (test_cases/)                       │
│  测试用例 + 数据驱动 + Assert                 │
├─────────────────────────────────────────────┤
│  Core 层 (core/)                             │
│  BaseTest / ResultBase / Allure Steps        │
├─────────────────────────────────────────────┤
│  Operation 层 (operation/)                   │
│  组装请求 → 调用 API → 解析响应 → 返回结果    │
├─────────────────────────────────────────────┤
│  API 层 (api/)                               │
│  管理 Session/Token → 发送 HTTP 请求          │
└─────────────────────────────────────────────┘
```

- **API 层**: 继承 `BaseAPI`，每个模块封装对应控制器的 RESTful 接口。`BaseAPI` 负责 Session 管理、Token 注入、请求日志、自动重试（500/502/503 最多重试 2 次）。
- **Operation 层**: 对 API 层返回的 `requests.Response` 进行解析，转换为 `ResultBase` 统一模型（code / success / msg / error / response），供测试用例直接断言。
- **Core 层**: 提供 `BaseTest` 基类（自动 setup/teardown 日志标记）、`ResultBase` 响应模型、以及 Allure Step 装饰器函数，确保 Allure 报告结构化展示每个测试步骤。
- **Test 层**: 使用 `@pytest.mark.parametrize` + YAML/Excel 数据驱动，结合 Allure 全量注释（@epic / @feature / @story / @title / @severity），分离测试数据与代码。

## 已实现的测试用例

### 1. 用户模块 (test_user_api.py)

**登录**

| 用例 | 标签 | 级别 |
|------|------|------|
| 登录成功（YAML 数据驱动） | smoke, p0 | CRITICAL |
| 登录成功后有 Token，能正常获取用户信息 | smoke, p0 | CRITICAL |
| 登出 | smoke, p0 | CRITICAL |

**注册**

| 用例 | 标签 | 级别 |
|------|------|------|
| 正常注册（含数据库校验） | smoke, p0 | CRITICAL |
| 用户名已存在 | p1 | NORMAL |
| 用户名为空 | p1 | NORMAL |
| 密码为空 | p1 | NORMAL |
| 邮箱格式错误 | p1 | NORMAL |

**Token 管理**

| 用例 | 标签 | 级别 |
|------|------|------|
| 刷新 Token | p2 | NORMAL |
| 携带 Token 访问受保护接口 | smoke, p0 | CRITICAL |

**用户管理**

| 用例 | 标签 | 级别 |
|------|------|------|
| 分页查询用户列表（支持关键字筛选） | p0, smoke | CRITICAL |
| 获取指定用户信息 | p1 | NORMAL |
| 修改用户信息（用户名/邮箱/昵称/备注/状态） | p1 | NORMAL |
| 修改密码 | p1 | NORMAL |
| 修改用户状态（启用/禁用） | p1 | NORMAL |
| 删除用户 | p2 | CRITICAL |
| 给用户分配角色 | p1 | NORMAL |
| 获取指定用户的角色 | p1 | NORMAL |

### 2. 品牌模块 (test_brand_api.py)

| 用例 | 标签 | 级别 |
|------|------|------|
| 创建品牌（数据驱动，含边界值） | smoke, p0 | CRITICAL |
| 分页查询品牌列表 | smoke, p0 | NORMAL |
| 获取品牌详情 | p1 | NORMAL |
| 获取不存在的品牌详情 | p2 | NORMAL |
| 修改品牌（数据驱动） | p1 | NORMAL |
| 删除品牌（数据驱动） | p1 | CRITICAL |
| 批量修改品牌显示状态 | p1 | NORMAL |

### 3. 商品模块 (test_product_api.py)

| 用例 | 标签 | 级别 |
|------|------|------|
| 创建商品（数据驱动） | smoke, p0 | CRITICAL |
| 分页查询商品列表（含断言校验） | smoke, p0 | NORMAL |
| 模糊搜索商品 | p1 | NORMAL |
| 批量操作（发布/推荐/新品/删除状态） | p1 | NORMAL |

### 4. 订单管理模块 (test_order_api.py)

| 用例 | 标签 | 级别 |
|------|------|------|
| 分页查询订单 | p1 | NORMAL |
| 订单详情查询 | p1 | NORMAL |
| 修改订单备注 | p1 | NORMAL |

### 5. 场景测试 (scenario_test/)

跨模块的多步骤业务流程测试，验证完整用户操作路径。

**用户场景** (test_01_user_register_login.py)

| 用例 | 标签 | 级别 | 流程 |
|------|------|------|------|
| 用户注册后登录并查看信息 | multiple, p0 | CRITICAL | 注册 → 登录 → 查信息 → 登出 |
| 重复注册相同用户名应失败 | multiple, negative, p1 | NORMAL | 首次注册成功 → 二次注册失败 |

**品牌场景** (test_02_brand_create_query_delete.py)

| 用例 | 标签 | 级别 | 流程 |
|------|------|------|------|
| 创建品牌 → 查询 → 修改 → 删除 | multiple, p0 | CRITICAL | 创建 → 列表查 → 详情查 → 修改 → 删除 |
| 查询不存在品牌应返回异常 | multiple, negative, p2 | MINOR | 查询不存在的品牌 ID |

**商品场景** (test_03_product_create_query.py)

| 用例 | 标签 | 级别 | 流程 |
|------|------|------|------|
| 创建商品 → 列表查询 → 模糊搜索 | multiple, p0 | CRITICAL | 创建 → 分页查 → 模糊搜索 |
| 空关键词模糊搜索 | multiple, negative, p2 | MINOR | 空关键词搜索 |

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
pytest -m multiple   # 场景测试（多步骤流程）
pytest -m negative   # 异常/负面测试
pytest -m single     # 单接口测试
```

### 并行执行
```bash
pytest -n auto       # 自动使用所有 CPU 核心（pytest-xdist）
pytest -n 2          # 指定 2 个并行进程
```

### 运行指定测试文件
```bash
pytest test_cases/API/test_user_api.py -v
pytest test_cases/scenario_test/ -v    # 运行所有场景测试
```

### 运行指定测试用例
```bash
pytest test_cases/API/test_user_api.py::TestUserLogin::test_login -v
```

### 失败重跑
```bash
pytest --reruns 1    # 失败用例自动重跑 1 次
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
- **P0 / Smoke**: 冒烟测试，核心业务路径（登录、注册、品牌创建、商品创建），失败则阻断发布
- **P1**: 重要功能，常规回归必测（用户 CRUD、角色分配、品牌修改、订单查询）
- **P2**: 边缘场景（不存在的品牌查询、空关键词搜索、Token 刷新等异常分支）

### 测试标记
pytest.ini 中注册了以下 markers：
| Marker | 用途 |
|--------|------|
| `p0` / `p1` / `p2` | 用例优先级 |
| `smoke` | 冒烟测试 |
| `single` | 单接口测试 |
| `multiple` | 多步骤集成/场景测试 |
| `negative` | 异常/负面测试 |

### 数据驱动
- 测试数据与代码完全分离，支持 YAML 和 Excel 双数据源
- 新增用例只需添加数据，无需修改代码
- Brand/Product 模块全量使用 YAML 参数化驱动

### 数据库校验
- 关键写操作（如注册）自动校验数据库，确保数据一致性
- 使用参数化查询防止 SQL 注入
- 提供 pre/post 清理夹具（`delete_register_user`、`delete_test_brand`、`delete_test_product`），确保测试可重复执行

### 日志与报告
- 控制台实时输出 + 文件按天滚动，保留 7 天
- 测试失败时自动将日志附加到 Allure 报告，方便定位问题
- 支持 Allure 特性/故事/严重级别标记，生成结构化测试报告
- 请求/响应自动日志（含耗时统计）

### 请求健壮性
- 连接超时 5s + 读取超时 15s
- 500/502/503 自动重试最多 2 次（退避因子 0.5s）

## 持续集成（CI/CD）

项目内置 Jenkins Pipeline（`Jenkinsfile`），支持自动化构建与通知。

### 流水线阶段
1. **环境准备**：自动安装/升级 Python 依赖
2. **生成环境配置**：从 Jenkins Credentials 注入测试环境变量，动态生成 `env_local.yaml`
3. **冒烟测试**：执行 `pytest -m smoke -n auto`，并行运行所有冒烟用例，输出 JUnit XML + Allure 结果
4. **生成 Allure 报告**：自动发布 Allure 报告到构建页面

### 触发方式
- **定时触发**：工作日（周一至周五）早 7 点自动执行
- 支持手动触发重跑

### 企业微信通知
- 成功/失败均发送通知到企业微信群
- 通知内容包含：通过率、总用例数、失败数、构建链接、Allure 报告链接
- 通过 `WECOM_WEBHOOK` Credential 配置 Webhook 地址

### Jenkins Credentials 配置

| Credential ID | 说明 |
|--------------|------|
| `TEST_BASE_URL` | 后端服务地址 |
| `TEST_USERNAME` | 管理员账号 |
| `TEST_PASSWORD` | 管理员密码 |
| `TEST_DB_HOST` | 数据库地址 |
| `TEST_DB_PORT` | 数据库端口 |
| `TEST_DB_USER` | 数据库用户 |
| `TEST_DB_PASSWORD` | 数据库密码 |
| `TEST_DB_DATABASE` | 数据库名 |
| `WECOM_WEBHOOK` | 企微机器人 Webhook |

## 扩展指南

### 添加新的 API 模块
1. 在 `api/` 下创建新的 API 类，继承 `BaseAPI`
2. 在 `operation/` 下创建对应的业务操作封装（请求组装 + 响应解析）
3. 在 `test_cases/conftest.py` 中添加对应的 fixture（API 客户端 + Token 注入）
4. 在 `data/` 下创建测试数据 YAML 文件
5. 在 `test_cases/API/` 下编写测试用例

### 添加场景测试
1. 在 `test_cases/scenario_test/` 下创建 `test_XX_模块名_流程名.py`
2. 继承 `BaseTest` 获取自动 setup/teardown 日志标记
3. 通过 Operation 层函数组合多个业务操作
4. 使用 `@pytest.mark.multiple` 标记场景测试

### 添加新的测试数据
1. 在 `data/` 下创建 YAML 文件或编辑 Excel 工作表
2. 使用 `load_yaml_data` 或 `read_excel_test_cases` 加载数据
3. 通过 `@pytest.mark.parametrize` 实现数据驱动

### 添加数据库校验
注入 `db` fixture 即可使用 `DBUtils` 进行数据库查询和断言。
