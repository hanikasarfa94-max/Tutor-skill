# 研究导师 Skill

把一位真实的学术导师——他的研究判断力、提问方式、督导逻辑——蒸馏成一个可以反复使用的 Claude Code Skill。

---

## 这是什么

**不是**一个模仿导师说话腔调的聊天机器人。

**是**一个把导师的学术方法和督导行为结构化、可纠正、可迭代的工作系统。

它能做的事：

- 诊断你的研究问题是否真的成立
- 指出草稿里最核心的那个问题（不是一份清单——是排过序的判断）
- 告诉你这周该做什么、做成什么样子
- 记住你上次遗留的问题，在你以为翻篇的时候重新提起

---

## 快速开始

### 安装

```bash
# macOS / Linux
git clone https://github.com/hanikasarfa94-max/Tutor-skill.git ~/.claude/skills/tutor-skill

# Windows
git clone https://github.com/hanikasarfa94-max/Tutor-skill.git %USERPROFILE%\.claude\skills\tutor-skill
```

更多安装细节见 [INSTALL.md](./INSTALL.md)。

### 先试试内置的原型

不需要任何准备材料，直接运行：

```
/mentor example-archetype diagnose
```

把你现在的研究困惑说出来，看看它怎么回应。

### 蒸馏你自己的导师

```
/create-mentor
```

按提示输入导师信息和你拥有的材料，系统会引导你完成全部流程。

---

## 三种工作模式

| 模式 | 适用场景 | 输出结构 |
|------|----------|----------|
| **诊断 Diagnose** | 研究问题模糊、方向不稳定 | 真正的问题是什么 / 为什么尚未成立 / 缺少什么前提 / 下一步做什么 / 现在不该做什么 |
| **审稿 Review** | 有提纲、草稿、段落需要评审 | 最核心的问题 / 严重缺陷 / 次要缺陷 / 修改优先级 / 具体修改建议 |
| **推进 Advance** | 卡住了、拖延了、阶段迷失 | 当前阶段诊断 / 卡住的根本原因 / 本周最小可执行任务 / 可交付物格式 / 下一个检查点 |

---

## 它是怎么工作的

系统使用三层架构，每层分离处理：

```
方法层 (method.md)      ← 学术判断系统：什么是好问题、好论证、好文献综述
    ↓
人格层 (persona.md)     ← 督导行为系统：如何提问、如何反馈、如何布置任务
    ↓
记忆层 (memory.md)      ← 学生成长记录：当前阶段、反复出现的问题、待完成任务
```

**方法层**来自论文、著作、讲座等学术材料，提取导师的研究问题意识、概念标准、方法偏好、论证风格。

**人格层**来自邮件、批注、聊天记录、会议笔记，提取导师如何与学生互动：怎么问、怎么批、怎么布置任务。

**记忆层**在使用过程中持续积累，追踪你的研究课题、当前阶段、反复出现的弱点和待办事项。

---

## 命令一览

### 创建与管理

| 命令 | 说明 |
|------|------|
| `/create-mentor` | 从材料中蒸馏一位新导师 |
| `/update-mentor {slug}` | 添加新材料，或纠正已有行为 |
| `/list-mentors` | 查看所有已生成的导师 Skill |
| `/mentor-rollback {slug} {version}` | 回滚到某个历史版本 |
| `/delete-mentor {slug}` | 删除一个导师 Skill |

### 使用

| 命令 | 说明 |
|------|------|
| `/mentor {slug}` | 激活一位导师，开始对话 |
| `/mentor {slug} diagnose` | 直接进入诊断模式 |
| `/mentor {slug} review` | 直接进入审稿模式 |
| `/mentor {slug} advance` | 直接进入推进模式 |

---

## 材料分类

创建导师时，你的材料会被分成三类，分别送入不同的分析管道：

| 类别 | 用途 | 示例 |
|------|------|------|
| **A 类：学术思想材料** | 提取方法层 | 论文、著作章节、学术访谈、序言、书评 |
| **B 类：督导行为材料** | 提取人格层 | 邮件、批注、聊天记录、组会笔记、学生回忆 |
| **C 类：桥接材料** | 连接方法层与人格层 | 课堂录音/文字稿、答辩评语、招生宣讲 |

没有材料也能用：系统会通过问卷帮你描述导师，置信度较低，但可以随时纠正和补充。

---

## 蒸馏一位真实的导师

如果你有这些材料中的任意一种：

- 导师发给你的邮件
- 他在你稿子上写的批注
- 他写的论文或著作（哪怕只有几章）
- 你整理的组会记录或讨论笔记
- 课程录音或讲义

都可以开始蒸馏。材料越丰富，结果越准确。材料不足的维度会被标注出来，方便你决定要不要补充。

---

## 纠正与迭代

第一次生成的结果可能不够准确。系统支持以下纠正方式：

- **局部纠正**：「这个回答不像他」
- **规则替换**：「把这条行为规则改成……」
- **增量补充**：「他在 X 情况下还会 Y」
- **语气纠正**：「他不会这样说话」

每次纠正都有版本记录，可以随时回滚。

---

## 目录结构

```
tutor-skill/
├── SKILL.md                    ← Claude Code 入口
├── README.md                   ← 英文说明
├── README_zh.md                ← 中文说明（此文件）
├── INSTALL.md                  ← 安装指南
├── prompts/
│   ├── intake.md               ← 信息收集
│   ├── method_analyzer.md      ← 方法层提取
│   ├── mentoring_style_analyzer.md  ← 人格层提取
│   ├── bridge_analyzer.md      ← 桥接层处理
│   ├── mentor_builder.md       ← 整合与生成
│   ├── use_mentor.md           ← 运行时 prompt
│   ├── session_closer.md       ← 会话结束记忆更新
│   ├── merger.md               ← 增量材料合并
│   └── correction_handler.md  ← 纠正处理
├── tools/
│   ├── paper_parser.py         ← 论文/著作解析
│   ├── annotation_parser.py    ← 批注解析
│   ├── email_parser.py         ← 邮件解析
│   ├── chat_parser.py          ← 聊天记录解析
│   ├── lecture_parser.py       ← 讲座文稿解析
│   ├── skill_writer.py         ← 导师文件读写
│   └── version_manager.py     ← 版本管理
├── mentors/
│   ├── generated/              ← 已生成的导师（本地，不上传）
│   └── archives/               ← 历史版本快照
└── docs/
    ├── schema.md               ← 数据结构文档
    └── intro_zh.md             ← 中文推广文案
```

---

## Python 依赖（可选）

解析器工具需要 Python 3.11+：

```bash
pip install -r requirements.txt
```

不安装也可以正常使用 Skill——解析器只是帮你把原始材料格式化，方便粘贴给 Claude。

---

## 隐私说明

`mentors/generated/` 和 `mentors/archives/` 目录已被 `.gitignore` 排除。  
你从真实邮件、批注等材料中生成的导师 Skill 文件只存在于本地，不会被提交到任何仓库。

---

## 开发阶段

- [x] Phase 1：核心骨架（intake、分析、构建、读写、版本管理）
- [x] Phase 2：运行时 prompt、会话记忆、纠正机制、学科专项维度
- [ ] Phase 3：解析器自动化（论文、邮件、聊天、讲座）
- [ ] Phase 4：导师原型模板（精读型、方法论型、严格推进型）
- [ ] Phase 5：长期督导记忆强化（跨会话反馈追踪）

---

## 相关项目

本项目的架构参考了：
- [colleague-skill](https://github.com/titanwings/colleague-skill) — 同事 Skill 蒸馏框架
- [ex-skill](https://github.com/therealXiaomanChu/ex-skill) — 同类 Skill 框架
