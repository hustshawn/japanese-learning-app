# JLPT Sensei 语法爬虫系统设计

**日期：** 2026-01-17
**目标：** 从 JLPT Sensei 网站爬取 150-180 个日语语法点，扩充学习应用数据库

## 背景

当前应用有 8 个手动编写的语法点，需要扩展到 200-500 个语法点以覆盖 JLPT N5-N2 的完整语法体系。

## 设计目标

- 快速获得高质量数据（优先 JLPT Sensei 一个来源）
- 保持数据质量和一致性
- 个人学习使用（遵守网站使用条款）
- 可扩展的架构（未来可添加其他数据源）

## 技术方案：渐进式爬虫系统

### 整体架构

**三层结构：**
1. **爬虫层** - 从网站抓取数据
2. **处理层** - 标准化、生成罗马音
3. **翻译层** - 人工辅助翻译（使用 Claude）

**工作流程：**
```
JLPT Sensei → Python爬虫 → grammar_raw.json → 人工翻译 → grammar.json → 合并到应用
```

### 目标网站：JLPT Sensei

**选择原因：**
- 结构化程度高（⭐⭐⭐⭐⭐）
- JLPT 分级清晰（N5-N2）
- 例句丰富且格式统一
- 预计产出：150-180 个语法点

**网站结构：**
- 语法列表页：按 JLPT 级别分类
- 语法详情页：包含解释和多个例句
- 数据格式：静态 HTML（不需要 JavaScript 渲染）

## 数据结构设计

### 中间格式（grammar_raw.json）

```json
{
  "id": "grammar-point-id",
  "title": "语法点标题（日语）",
  "titleRomaji": "romaji",
  "explanationEN": "English explanation",
  "examples": [
    {
      "japanese": "日语例句",
      "romaji": "romaji",
      "englishTranslation": "English translation"
    }
  ],
  "jlptLevel": "N5",
  "source": "JLPT Sensei",
  "url": "https://jlptsensei.com/..."
}
```

### 最终格式（grammar.json）

与现有应用格式保持一致：
```json
{
  "id": "grammar-point-id",
  "title": "语法点标题",
  "titleRomaji": "romaji",
  "explanation": "中文解释",
  "examples": [
    {
      "japanese": "日语例句",
      "romaji": "romaji",
      "english": "中文翻译"
    }
  ]
}
```

**新增字段（可选）：**
- `jlptLevel`: JLPT 级别（N5/N4/N3/N2）
- `source`: 数据来源

## 实现分两个阶段

### 阶段 1：自动爬取（Python 脚本）

**功能：**
1. 爬取 JLPT N5/N4/N3/N2 的语法列表页
2. 提取每个语法点的链接
3. 访问详情页，提取：
   - 语法标题（日语）
   - 英文解释
   - 例句（日语 + 英文）
4. 使用 pykakasi 自动生成罗马音
5. 输出 `grammar_raw.json`

**技术栈：**
- Python 3.13
- requests（HTTP 请求）
- BeautifulSoup4（HTML 解析）
- pykakasi（日语转罗马音）

**关键特性：**
- 断点续爬：保存进度，支持中断后继续
- 速率控制：1-2 秒/请求，避免触发反爬
- 错误重试：失败请求自动重试 3 次
- 详细日志：记录爬取过程和错误
- 数据验证：确保字段完整性

### 阶段 2：批量翻译（人工辅助）

**流程：**
1. 用户运行爬虫，生成 `grammar_raw.json`
2. 用户将文件内容发送给 Claude
3. Claude 批量翻译：
   - `explanationEN` → 中文解释
   - `englishTranslation` → 中文翻译
4. Claude 返回翻译后的完整数据
5. 用户保存为 `grammar.json`
6. 合并到应用的 `data/grammar.json`

**翻译优势：**
- 翻译质量高（理解日语语法细微差别）
- 可分批处理（每次 20-30 个）
- 保留原始数据，方便重新翻译
- 无 API 成本

## 项目结构

```
jp-learning-app/
├── scripts/
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── jlpt_sensei_scraper.py  # 主爬虫逻辑
│   │   ├── models.py                # 数据模型
│   │   └── utils.py                 # 工具函数（日志、重试等）
│   ├── requirements.txt             # Python 依赖
│   └── run_scraper.py               # 命令行入口
├── data/
│   ├── grammar.json                 # 现有数据（8 个语法点）
│   ├── grammar_raw.json             # 爬取的原始数据（新）
│   └── grammar_backup.json          # 备份（新）
└── docs/
    └── plans/
        └── 2026-01-17-jlpt-sensei-scraper-design.md
```

## 爬虫实现细节

### URL 模式分析

**列表页：**
- N5: `https://jlptsensei.com/jlpt-n5-grammar-list/`
- N4: `https://jlptsensei.com/jlpt-n4-grammar-list/`
- N3: `https://jlptsensei.com/jlpt-n3-grammar-list/`
- N2: `https://jlptsensei.com/jlpt-n2-grammar-list/`

**详情页：**
- 格式: `https://jlptsensei.com/learn-japanese-grammar/[grammar-slug]/`

### 数据提取策略

1. **列表页提取：**
   - 查找语法点链接（通常在表格或列表中）
   - 提取语法标题和链接

2. **详情页提取：**
   - 标题：通常在 `<h1>` 或特定 class 中
   - 解释：查找包含 "meaning" 或 "explanation" 的部分
   - 例句：通常在特定的例句区块中，包含日语和英文

3. **罗马音生成：**
   - 使用 pykakasi 转换日语文本
   - 处理特殊情况（汉字、假名混合）

### 错误处理

**常见错误：**
- 网络超时：重试 3 次，间隔递增
- 解析失败：记录错误，跳过该条目
- 编码问题：强制使用 UTF-8

**日志级别：**
- INFO: 爬取进度（已完成 X/Y）
- WARNING: 跳过的条目
- ERROR: 严重错误（需要人工检查）

## 使用方法

### 1. 安装依赖

```bash
cd scripts
pip install -r requirements.txt
```

### 2. 运行爬虫

```bash
python run_scraper.py --levels N5 N4 N3 N2 --output ../data/grammar_raw.json
```

**参数：**
- `--levels`: JLPT 级别（可选多个）
- `--output`: 输出文件路径
- `--delay`: 请求间隔（秒，默认 1.5）
- `--resume`: 断点续爬

### 3. 翻译数据

将 `grammar_raw.json` 发送给 Claude 进行翻译。

### 4. 合并数据

```bash
# 备份现有数据
cp data/grammar.json data/grammar_backup.json

# 合并新数据（手动或使用合并脚本）
python scripts/merge_grammar.py
```

## 数据质量保证

### 验证检查

1. **必填字段检查：**
   - 所有字段都存在且非空
   - 例句数量 ≥ 2

2. **格式检查：**
   - JSON 格式正确
   - 罗马音格式合理

3. **去重检查：**
   - ID 唯一性
   - 避免重复的语法点

### 人工审核

建议对以下情况进行人工审核：
- 罗马音生成异常（过短或过长）
- 例句数量异常（<2 或 >10）
- 解释文本过短（<20 字符）

## 扩展性考虑

### 未来可添加的数据源

**优先级 2：**
- JTest4You（补充例句）
- Tae Kim's Guide（深度解释）

**集成方式：**
- 为每个数据源创建独立爬虫
- 使用统一的数据模型
- 实现智能合并逻辑（去重、补充）

### 可能的增强功能

1. **自动去重：** 检测相似语法点
2. **质量评分：** 根据例句数量、解释长度等评分
3. **差异检测：** 对比不同来源的相同语法点
4. **增量更新：** 只爬取新增的语法点

## 时间预估

**阶段 1（爬虫开发）：** 4-6 小时
- 爬虫核心逻辑：2 小时
- 错误处理和测试：1-2 小时
- 文档和调试：1-2 小时

**阶段 2（数据爬取）：** 1-2 小时
- 实际爬取时间：30-60 分钟（取决于速率限制）
- 数据验证：30 分钟

**阶段 3（翻译）：** 2-3 小时（分批进行）

**总计：** 约 1-2 天完成

## 风险和缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 网站结构变化 | 爬虫失效 | 添加验证检查，及时发现 |
| IP 被封 | 无法继续爬取 | 速率限制、使用代理 |
| 数据质量问题 | 翻译困难 | 人工审核，分批处理 |
| 编码问题 | 日语显示异常 | 强制 UTF-8，测试多种场景 |

## 成功标准

- ✅ 成功爬取 150+ 个语法点
- ✅ 数据格式与现有应用兼容
- ✅ 每个语法点至少 2 个例句
- ✅ 罗马音生成准确率 >95%
- ✅ 无重大错误或数据丢失
- ✅ 完整的 JLPT 分级信息

## 后续优化

1. **应用端增强：**
   - 按 JLPT 级别筛选
   - 显示数据来源
   - 搜索功能

2. **数据管理：**
   - 版本控制（追踪数据变更）
   - 定期更新（6 个月一次）
   - 用户反馈机制（标记错误）

3. **学习功能：**
   - 根据 JLPT 级别推荐
   - 难度渐进学习路径
   - 错题集功能

## Implementation Status

✅ Scraper implemented and tested
- All components working
- Full integration tested with N5 level
- Ready for production scraping

Next: Run full scrape for N5-N2 levels
