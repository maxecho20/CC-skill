# Claude Skills 能力文档

> 📖 本文档详细记录了项目中所有可用的 Agent Skills 及其能力说明  
> 🔄 最后更新时间：2025-12-18  
> 📁 Skills 总数：26 个

---

## 📋 目录

1. [什么是 Agent Skills](#什么是-agent-skills)
2. [Skills 总览](#skills-总览)
3. [Skills 触发关键词速查表](#skills-触发关键词速查表)
4. [Skills 详细说明](#skills-详细说明)
   - [Skill Creator](#1-skill-creator)
   - [Skill Converter](#2-skill-converter)
   - [Skill Seekers](#3-skill-seekers)
   - [Web Accessibility - Contrast Fix](#4-web-accessibility---contrast-fix)
   - [Google Official SEO Guide](#5-google-official-seo-guide)
   - [Internationalizing Websites](#6-internationalizing-websites)
   - [Deploying to Production](#7-deploying-to-production)
   - [Doc Sync Tool](#8-doc-sync-tool)
   - [Shipany](#9-shipany)
   - [Document Processing (docx, pdf, xlsx, pptx)](#10-document-processing)
   - [Advanced Development (Superpowers, TDD, etc.)](#11-advanced-development)
   - [Content & Marketing (ComposioHQ)](#12-content--marketing)
   - [Data & Productivity (Organization, Insights)](#13-data--productivity)
5. [如何使用 Skills](#如何使用-skills)
6. [更新日志](#更新日志)

---

## 什么是 Agent Skills

Agent Skills 是模块化的能力包，通过专业知识、工作流程和工具来扩展 Claude 的功能。每个 Skill 包含：

| 组件 | 说明 | 是否必需 |
|------|------|---------|
| `SKILL.md` | 核心指令和工作流程 | ✅ 必需 |
| `scripts/` | 可执行脚本 (Python/Bash/JS) | ⚪ 可选 |
| `references/` | 参考文档和知识库 | ⚪ 可选 |
| `assets/` | 资源文件（模板、图片等）| ⚪ 可选 |

### Skills 的三级加载机制

1. **元数据层** (~100 词) - 始终在上下文中
2. **指令层** (<5k 词) - Skill 触发时加载
3. **资源层** (无限制) - 按需加载脚本和参考

---

## Skills 总览

| # | Skill 名称 | 分类 | 主要能力 | 来源 |
|---|-----------|------|----------|------|
| 1 | **Skill Creator** | 开发工具 | 创建和管理 Skills | Anthropic 官方 |
| 2 | **Skill Converter** | 开发工具 | 转换文档/仓库为 Skills | 本地工具 |
| 3 | **Skill Seekers** | 开发工具 | 自动爬取并生成 Skills | GitHub 开源 |
| 4 | **Web Accessibility** | 性能优化 | 修复网页可访问性问题 | 社区贡献 |
| 5 | **Google SEO Guide** | SEO 优化 | Google 搜索优化最佳实践 | 社区贡献 |
| 6 | **Internationalizing Websites** | 国际化 | Next.js 多语言支持 | 社区贡献 |
| 7 | **Deploying to Production** | 部署 | GitHub + Vercel 自动部署 | 社区贡献 |
| 8 | **Doc Sync Tool** | 工具 | AI Agent 文档同步 | 社区贡献 |
| 9 | **Shipany** | SaaS 框架 | AI SaaS 模板开发指南 | 社区贡献 |
| 10 | **Office Suite (docx, xlsx, pptx)** | 文档处理 | 处理 Word, Excel, PPT | Anthropic 官方 |
| 11 | **PDF Toolkit** | 文档处理 | PDF 提取、合并与注释 | Anthropic 官方 |
| 12 | **TDD & Superpowers** | 开发者 | TDD 模式、Git 管理、头脑风暴 | obra/superpowers |
| 13 | **Web Artifacts & Testing** | 开发者 | 构建和测试 Web 组件 | Anthropic 官方 |
| 14 | **Content & Theme Factory** | 创意媒体 | 深度内容研究、主题生成 | ComposioHQ |
| 15 | **Data & Insights** | 数据分析 | 会议分析、CSV 摘要 | ComposioHQ |
| 16 | **Organizational Tools** | 效率组织 | 文件及发票自动智能整理 | ComposioHQ |

---

## Skills 触发关键词速查表

当你在对话中提到以下关键词时，对应的 Skill 会被自动触发：

| Skill | 中文关键词 | 英文关键词 |
|-------|-----------|-----------|
| **Skill Creator** | 创建技能、新建 skill、技能开发 | create skill, new skill, skill template |
| **Skill Converter** | 转换文档、仓库转技能、PDF转技能 | convert docs, convert repo, conflict detection |
| **Skill Seekers** | 爬取文档、文档转skill、自动生成技能 | scrape docs, skill seekers, unified scraping |
| **Web Accessibility** | 可访问性、对比度、PageSpeed感叹号 | accessibility, contrast, WCAG, Lighthouse |
| **Google SEO Guide** | SEO优化、结构化数据、搜索排名 | SEO, structured data, VideoObject, schema.org |
| **Internationalizing** | 国际化、多语言、i18n、hreflang | i18n, multi-language, translation, localization |
| **Deploying** | 部署、上线、发布、Vercel | deploy, go live, publish, Vercel, GitHub |
| **Doc Sync Tool** | 文档同步、Agent配置同步 | doc sync, Agents.md, claude.md sync |
| **Shipany** | SaaS模板、Shipany、NextAuth、Drizzle | Shipany, SaaS boilerplate, NextAuth, Drizzle ORM |
| **Document Processing** | Word, Excel, PPT, PDF处理 | docx, xlsx, pptx, pdf toolkit |
| **Advanced Dev** | TDD开发、Git Worktrees、Web组件测试 | TDD, web-artifacts, webapp-testing, git worktrees |
| **Composio Content** | 内容研究、主题工厂、会议分析 | content research, theme factory, meeting insights |
| **Office Organization** | 文件整理、发票提取 | file organizer, invoice organizer |

### 使用示例

```
# 触发 Skill Creator
"帮我创建一个新的 skill"

# 触发 Google SEO Guide
"如何添加 VideoObject 结构化数据？"

# 触发 Internationalizing Websites
"给我的网站添加日语支持"

# 触发 Deploying to Production
"帮我把网站部署到 Vercel"

# 触发 Shipany
"我在用 Shipany 框架，如何配置支付？"
```

---

## Skills 详细说明

### 1. Skill Creator

**📍 位置**: `skill-creator/SKILL.md`  
**🏷️ 分类**: 开发工具  
**📦 来源**: Anthropic 官方

#### 能力描述

帮助创建有效的 Agent Skills，提供以下功能：

- 📝 **Skill 结构指导** - 如何组织 SKILL.md 和相关资源
- 🔧 **创建工作流程** - 从需求理解到打包发布的完整流程
- 📋 **最佳实践** - 编写高质量 Skill 的建议和模式

#### 🎯 触发关键词

| 中文 | 英文 |
|------|------|
| 创建技能、新建skill、技能开发、更新技能 | create skill, new skill, skill development, build skill, update skill |

#### 包含资源

| 资源 | 路径 | 说明 |
|------|------|------|
| 初始化脚本 | `scripts/init_skill.py` | 创建新 Skill 模板 |
| 打包脚本 | `scripts/package_skill.py` | 验证并打包 Skill |

#### 使用示例

```bash
# 创建新 Skill
python scripts/init_skill.py my-skill --path ./skills/

# 打包 Skill
python scripts/package_skill.py ./skills/my-skill
```

---

### 2. Skill Converter

**📍 位置**: `skill-creator/skill-converter/SKILL.md`  
**🏷️ 分类**: 开发工具  
**📦 来源**: 本地工具 (基于 Skill Seekers 概念)

#### 能力描述

将各种来源的文档转换为 Claude AI Skills：

- 📂 **GitHub 仓库转换** - 克隆仓库并提取文档和代码示例
- 📄 **文档处理** - 支持 Markdown, HTML, Word, reStructuredText
- 📑 **PDF 提取** - 从 PDF 中提取文本、代码块和结构
- ⚠️ **冲突检测** - 识别文档与实现之间的不一致
- 📦 **技能打包** - 创建可分发的 .zip 文件

#### 🎯 触发关键词

| 中文 | 英文 |
|------|------|
| 转换文档、仓库转skill、PDF转换、冲突检测 | convert documentation, convert repo, convert PDF, conflict detection |

#### 包含脚本

| 脚本 | 用途 |
|------|------|
| `convert_github_repo.py` | 克隆仓库并提取文档 |
| `process_documentation.py` | 处理各种文档格式 |
| `pdf_to_skill.py` | PDF 转换工具 |
| `conflict_detector.py` | 冲突检测引擎 |
| `package_generator.py` | 技能打包 |
| `convert_all.py` | 统一转换接口 |

---

### 3. Skill Seekers

**📍 位置**: `skills/skill-seekers/SKILL.md`  
**🏷️ 分类**: 开发工具 (Python 工具)  
**📦 来源**: [GitHub - Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers)  
**🔧 版本**: v2.1.1 (Production Ready)

#### 能力描述

自动将文档网站、GitHub 仓库和 PDF 转换为生产就绪的 Claude AI Skills：

- 🌐 **文档网站爬取** - 支持 24+ 预设配置
- 🐙 **GitHub 仓库分析** - 深度 AST 解析
- 📄 **PDF 处理** - 提取文本和代码块
- 🔄 **统一多源爬取** - 组合多个来源为一个 Skill
- ⚠️ **冲突检测** - 文档与代码实现对比
- 🤖 **AI 增强** - 自动优化 SKILL.md 质量

#### 🎯 触发关键词

| 中文 | 英文 |
|------|------|
| 爬取文档、文档转skill、自动生成技能 | skill seekers, scrape documentation, create skill from docs, unified scraping |

#### 快速使用

```bash
# 进入目录并安装依赖
cd skills/skill-seekers
pip install -r requirements.txt

# 单源爬取
python src/skill_seekers/cli/doc_scraper.py --config configs/react.json

# 统一多源爬取 (docs + GitHub)
python src/skill_seekers/cli/unified_scraper.py --config configs/react_unified.json

# 打包技能
python src/skill_seekers/cli/package_skill.py output/react/
```

#### 预设配置 (24 个)

| 类别 | 配置 |
|------|------|
| **Web 框架** | react, vue, django, fastapi, laravel, astro, hono |
| **游戏引擎** | godot, godot-large-example |
| **DevOps** | kubernetes, ansible-core |
| **统一配置** | react_unified, django_unified, fastapi_unified, godot_unified |

---

### 4. Web Accessibility - Contrast Fix

**📍 位置**: `skills/web-performance-seo/SKILL.md`  
**🏷️ 分类**: 性能优化 / 可访问性  
**📦 来源**: [AgentSkills.best](https://agentskills.best/zh) 社区贡献

#### 能力描述

诊断并修复 PageSpeed Insights 可访问性审核失败的问题：

- 🔍 **问题诊断** - 识别导致 "!" 分数的根本原因
- 🛠️ **修复流程** - 5 阶段系统化修复工作流
- ✅ **合规验证** - WCAG 2.1 对比度标准符合性检查

#### 🎯 触发关键词

| 中文 | 英文 |
|------|------|
| 可访问性分数、对比度审计、PageSpeed感叹号、WCAG合规 | accessibility score, color contrast, PageSpeed "!", WCAG compliance, Lighthouse accessibility |

#### 核心问题解决

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 分数显示 "!" | 测量失败，非低分 | 移除阻塞因素 |
| CSS Filter 错误 | `backdrop-blur` 等 | 移除或替换 |
| OKLCH 颜色空间 | 对比度计算偏差 | 转换为 HSL |
| 低透明度背景 | canvas 采样不稳定 | 提高至 ≥0.4 |

#### 快速诊断命令

```bash
# 检查颜色空间
grep -r "oklch\|oklab" app/ components/

# 检查低透明度
grep -r "/10\|/20\|/30" components/

# 检查 CSS Filters
grep -r "backdrop-blur\|filter:" components/
```

---

### 5. Google Official SEO Guide

**📍 位置**: `skills/google-official-seo-guide/SKILL.md`  
**🏷️ 分类**: SEO 优化  
**📦 来源**: [AgentSkills.best](https://agentskills.best/zh) 社区贡献

#### 能力描述

基于 Google 官方文档的全面 SEO 优化指南：

- 🔍 **搜索优化** - 提升 Google 搜索排名
- 📊 **结构化数据** - VideoObject, BroadcastEvent, Clip 等
- 🤖 **技术 SEO** - 爬取、索引、移动优先索引
- 📈 **Search Console** - 监控和调试

#### 🎯 触发关键词

| 中文 | 英文 |
|------|------|
| SEO优化、搜索排名、结构化数据、视频SEO | SEO optimization, Google Search ranking, structured data, VideoObject, schema.org, sitemap |

#### 参考资源 (9 个文件, ~450KB)

| 文件 | 内容 |
|------|------|
| `references/apis.md` | Search Console 设置 |
| `references/appearance.md` | 搜索结果展示 (187KB) |
| `references/crawling.md` | 爬取机制 (129KB) |
| `references/fundamentals.md` | SEO 基础 |
| `references/guides.md` | 实施指南 |
| `references/indexing.md` | 索引管理 |
| `references/specialty.md` | 结构化数据 |

#### 常用结构化数据示例

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "视频标题",
  "description": "视频描述",
  "uploadDate": "2024-03-31T08:00:00+08:00",
  "duration": "PT1M54S"
}
```

---

### 6. Internationalizing Websites

**📍 位置**: `skills/internationalizing-websites/SKILL.md`  
**🏷️ 分类**: 国际化 / 多语言  
**📦 来源**: [AgentSkills.best](https://agentskills.best/zh) 社区贡献

#### 能力描述

为 Next.js 网站添加多语言支持：

- 🌍 **多语言配置** - 支持 15+ 种语言
- 🏷️ **hreflang 标签** - 正确的国际 SEO 配置
- 🗺️ **本地化站点地图** - 自动更新 sitemap
- 🔄 **翻译工作流** - AI + 人工翻译最佳实践

#### 🎯 触发关键词

| 中文 | 英文 |
|------|------|
| 国际化、多语言、添加日语/中文、本地化 | i18n, internationalization, multi-language, translation, localization, hreflang |

#### 支持的语言

- **主要市场**: 🇺🇸 English, 🇯🇵 日本語, 🇨🇳 中文
- **扩展支持**: 🇰🇷 한국어, 🇵🇹 Português, 🇪🇸 Español, 🇫🇷 Français, 🇩🇪 Deutsch

#### 包含脚本

| 脚本 | 用途 |
|------|------|
| `scripts/i18n-add-languages.mjs` | 自动添加新语言文件 |
| `scripts/i18n-add-schema.js` | 添加结构化数据翻译 |

---

### 7. Deploying to Production

**📍 位置**: `skills/deploying-to-production/SKILL.md`  
**🏷️ 分类**: 部署  
**📦 来源**: [AgentSkills.best](https://agentskills.best/zh) 社区贡献

#### 能力描述

自动化 GitHub 仓库创建和 Vercel 部署工作流：

- 🚀 **自动化部署** - 一键部署到 Vercel
- 📦 **GitHub 集成** - 自动创建私有仓库
- ✅ **预部署验证** - 构建检查和核心要素检查
- 🔧 **故障排除** - 完整的问题解决指南

#### 🎯 触发关键词

| 中文 | 英文 |
|------|------|
| 部署、上线、发布、推送生产、Vercel部署 | deploy, go live, publish, production, Vercel, GitHub push |

#### 部署工作流程

```
1. ✅ 预部署验证 (npm run build + E-E-A-T 检查)
2. ✅ 创建 GitHub 仓库
3. ✅ 推送代码到 GitHub
4. ✅ 部署到 Vercel
5. ✅ 部署后验证
```

#### 包含脚本

| 脚本 | 用途 |
|------|------|
| `scripts/create-github-repo.sh` | GitHub 仓库创建 |
| `scripts/deploy-to-vercel.sh` | Vercel 部署 |

---

### 8. Doc Sync Tool

**📍 位置**: `skills/doc-sync-tool/SKILL.md`  
**🏷️ 分类**: 工具  
**📦 来源**: [AgentSkills.best](https://agentskills.best/zh) 社区贡献

#### 能力描述

自动同步项目中的 AI Agent 配置文档：

- 🔄 **自动发现** - 递归扫描目录查找配置文档
- 📋 **智能同步** - 保持 `Agents.md`、`claude.md`、`gemini.md` 内容一致
- 👀 **文件监听** - 实时监听文件变化并自动同步

#### 🎯 触发关键词

| 中文 | 英文 |
|------|------|
| 文档同步、Agent配置同步、claude.md同步 | doc sync, sync Agents.md, sync claude.md, agent config sync |

#### 使用方法

```bash
# 安装依赖
cd skills/doc-sync-tool
pnpm install

# 手动同步（单次执行）
pnpm run sync

# 自动监听（持续运行）
pnpm run watch

# 后台运行（推荐）
pm2 start watch.js --name doc-sync
```

---

### 9. Shipany

**📍 位置**: `skills/shipany/SKILL.md`  
**🏷️ 分类**: SaaS 框架  
**📦 来源**: [AgentSkills.best](https://agentskills.best/zh) 社区贡献

#### 能力描述

Shipany AI SaaS 模板框架的完整开发指南：

- 🚀 **快速搭建** - Next.js 15 + TypeScript 模板
- 💳 **支付集成** - Stripe/Creem 支付配置
- 🔐 **认证系统** - NextAuth (Google/GitHub)
- 🌍 **国际化** - next-intl 多语言支持
- 🤖 **AI 集成** - OpenAI, Replicate, Kling AI

#### 🎯 触发关键词

| 中文 | 英文 |
|------|------|
| Shipany框架、SaaS模板、支付集成、NextAuth | Shipany, SaaS boilerplate, Next.js 15, Drizzle ORM, NextAuth, payment integration |

#### 参考文档 (11 个文件)

| 文件 | 内容 |
|------|------|
| `references/getting_started.md` | 快速入门 |
| `references/authentication.md` | 认证系统 |
| `references/database.md` | 数据库配置 (Drizzle ORM) |
| `references/payment.md` | 支付集成 |
| `references/api.md` | API 开发 |
| `references/internationalization.md` | 国际化 |
| `references/deployment.md` | 部署指南 |

#### 技术栈

- **框架**: Next.js 15, TypeScript
- **数据库**: Drizzle ORM
- **认证**: NextAuth (Google/GitHub)
- **支付**: Stripe, Creem
- **邮件**: Resend
- **AI**: OpenAI, Replicate, Kling AI
- **国际化**: next-intl

---

### 10. Document Processing (docx, pdf, xlsx, pptx)

**📍 位置**: `skills/anthropics/[docx, pdf, xlsx, pptx]/SKILL.md`  
**🏷️ 分类**: 文档处理  
**📦 来源**: Anthropic 官方

#### 能力描述
- **docx**: 编辑文档、合并文档、甚至支持 OOXML 脚本验证。
- **xlsx**: 数据过滤、透视表建议以及复杂的图表生成。
- **pptx**: 幻灯片布局自动化，支持 master 模板。
- **pdf**: 支持 PDF 的批量拆分、字段提取及元数据清理。

#### 🎯 触发关键词
| 中文 | 英文 |
|------|------|
| Word 文档编辑、Excel 数据透视、PPT 布局设计、PDF 合并 | edit docx, xlsx pivot, pptx master, pdf merge |

---

### 11. Advanced Development (Superpowers, TDD, etc.)

**📍 位置**: `skills/superpowers/`, `skills/anthropics/`  
**🏷️ 分类**: 开发工具  
**📦 来源**: obra/superpowers, Anthropic 官方

#### 主要工具与工作流
- **TDD (Test-Driven Development)**: 强制采用“红色-绿色-重构”循环。
- **Systematic Debugging**: 通过假设推导（Hypothesis-driven）来定位复杂 Bug。
- **Web Artifacts**: 使用 `artifacts-builder` 快速生成交互式 UI。
- **Git Worktrees**: 使用 `using-git-worktrees` 在不切换分支的情况下处理紧急修复。

#### 🎯 触发关键词
| 中文 | 英文 |
|------|------|
| 红色-绿色工作流、系统化调试、UI 画布构建、Git 多树管理 | red-green-refactor, hypothesis debugging, web artifacts, git worktree |

---

### 12. Content & Marketing (ComposioHQ)

**📍 位置**: `skills/composio/`  
**🏷️ 分类**: 创意媒体 / 商业营销  
**📦 来源**: ComposioHQ

#### 核心能力
- **Content Research Writer**: 跨网页搜索并合成深度研究报告。
- **Theme Factory**: 提供 'Cyberpunk', 'Minimalist', 'Professional' 等 10 种样式。
- **Changelog**: 自动扫描 `git log` 并生成分版本的更新通告。

#### 🎯 触发关键词
| 中文 | 英文 |
|------|------|
| 研究综述、风格主题化、发版说明生成 | research report, theme application, generate changelog |

---

### 13. Data & Productivity (Organization, Insights)

**📍 位置**: `skills/composio/`  
**🏷️ 分类**: 数据分析 / 效率组织  
**📦 来源**: ComposioHQ

#### 自动化能力
- **Meeting Insights**: 识别会议中的参与度不均、决策点遗漏等隐性信息。
- **File Organizer**: 自动将 `Downloads` 文件夹按文件类别和项目上下文归档。
- **Invoice Organizer**: 识别发票金额、税号及到期日，输出 CSV 清单。

#### 🎯 触发关键词
| 中文 | 英文 |
|------|------|
| 会议参与度分析、 Downloads 整理、发票收据自动归档 | meeting dynamics, auto file organization, expense tracking |

---

## 如何使用 Skills

### 在 Antigravity 中使用

#### 方式一：直接指定 Skill

```
请使用 google-official-seo-guide skill，帮我添加视频结构化数据
```

```
参考 internationalizing-websites skill，为我的网站添加日语支持
```

```
使用 deploying-to-production skill，帮我把网站部署到 Vercel
```
```
请使用 docx 技能，帮我检查一下合同里的修订建议
```

#### 方式二：描述问题 (自动匹配关键词)

```
我的 PageSpeed Insights 可访问性分数显示感叹号，怎么修复？
→ 自动触发 Web Accessibility skill
```

```
如何配置 hreflang 标签实现多语言 SEO？
→ 自动触发 Internationalizing Websites skill
```

```
我在用 Shipany 框架，如何配置 Stripe 支付？
→ 自动触发 Shipany skill
```
```
帮我整理一下最近一个月的发票并生成 CSV
→ 自动触发 Invoice Organizer
```

### 在 Claude Code CLI 中使用

```bash
# 添加 Skill
claude code skills add ./skills/google-official-seo-guide

# 列出已安装的 Skills
claude code skills list
```

---

## 目录结构

```
claude skills/
├── SKILLS_DOCUMENTATION.md       # 📖 本文档
├── skill-creator/                # Skill 创建工具
│   ├── SKILL.md
│   ├── scripts/
│   └── skill-converter/          # 文档转换工具
│       ├── SKILL.md
│       └── scripts/ (6 files)
└── skills/                       # 已安装的 Skills
    ├── README.md
    ├── skill-seekers/            # 文档爬取工具 (Python)
    │   ├── SKILL.md
    │   ├── CLAUDE.md
    │   ├── configs/ (24 files)
    │   └── src/skill_seekers/
    ├── web-performance-seo/      # 可访问性修复
    │   ├── SKILL.md
    │   └── README.md
    ├── google-official-seo-guide/  # Google SEO 指南
    │   ├── SKILL.md
    │   └── references/ (9 files)
    ├── internationalizing-websites/  # 国际化
    │   ├── SKILL.md
    │   ├── WORKFLOW.md
    │   ├── scripts/ (2 files)
    │   └── reference/ (3 files)
    ├── deploying-to-production/  # 部署工具
    │   ├── SKILL.md
    │   ├── CHECKLIST.md
    │   ├── TROUBLESHOOTING.md
    │   └── scripts/ (2 files)
    ├── doc-sync-tool/            # 文档同步工具
    │   ├── SKILL.md
    │   ├── sync.js
    │   └── watch.js
    └── shipany/                  # SaaS 模板框架
        ├── SKILL.md
        └── references/ (11 files)
```

---

## 更新日志

### 2025-12-18
- **总数增加至 26 个**
- 批量导入 **Anthropic 官方办公套装** (4)
- 批量导入 **Superpowers 开发增强包** (4)
- 批量导入 **ComposioHQ 生产力套装** (5)
- 新增分类 **10. 文档处理**, **11. 高级开发**, **12. 内容营销**, **13. 数据洞察**。

**文档更新:**
- 新增 "触发关键词速查表" 章节
- 每个 Skill 添加详细的中英文触发关键词
- 更新目录结构

**来源:**
- [AgentSkills.best](https://agentskills.best/zh)
- [Anthropic Official Skills](https://github.com/anthropics/skills)
- [Awesome Agent Skills](https://github.com/littleben/awesomeAgentskills)
- [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers)

---

> 💡 **提示**: 如需获取某个特定 Skill 的详细文档，可以搜索项目中的 `SKILL.md` 文件。

---

## 贡献新 Skill

如需添加新 Skill，请遵循以下步骤：

1. 将 Skill 文件夹复制到 `skills/` 目录
2. 确保包含有效的 `SKILL.md` 文件（含 YAML frontmatter）
3. 更新本文档的 Skills 总览和详细说明
4. 在更新日志中记录变更

### Skill 文档模板

```markdown
### [新 Skill 名称]

**📍 位置**: `skills/[skill-name]/SKILL.md`  
**🏷️ 分类**: [分类]  
**📦 来源**: [来源]

#### 能力描述
[描述该 Skill 的核心功能]

#### 🎯 触发关键词

| 中文 | 英文 |
|------|------|
| [中文关键词] | [英文关键词] |

#### 包含资源
[列出 scripts/references/assets]
```

---

> 💡 **提示**: 当你需要使用某个 Skill 时，只需在对话中提及相关关键词或直接指定 Skill 名称，我就会自动应用相关知识和工作流程。
