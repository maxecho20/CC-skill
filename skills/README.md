# Claude Skills 集合

本目录包含了从 [AgentSkills.best](https://agentskills.best/zh)、Anthropic 官方、Superpowers 及 ComposioHQ 等来源下载的 Claude AI Skills。

## 📦 已安装的 Skills (26 个)

### 🛠️ 开发工具与高级开发
包含自动化测试、架构设计、Git 管理及 TDD 工作流。

| Skill | 目录 | 用途 | 来源 |
|-------|------|------|------|
| **Skill Seekers** | `skill-seekers/` | 自动爬取文档并生成 skills | GitHub 开源 |
| **test-driven-development** | `superpowers/test-driven-development/` | TDD 开发模式指导 | Superpowers |
| **using-git-worktrees** | `superpowers/using-git-worktrees/` | 智能管理 Git 工作树 | Superpowers |
| **systematic-debugging** | `superpowers/systematic-debugging/` | 系统化 Bug 诊断逻辑 | Superpowers |
| **brainstorming** | `superpowers/brainstorming/` | 结构化头脑风暴转方案 | Superpowers |
| **web-artifacts-builder** | `anthropics/web-artifacts-builder/` | 构建 React+Tailwind 组件 | Anthropic 官方 |
| **mcp-builder** | `anthropics/mcp-builder/` | 引导创建 MCP 服务器 | Anthropic 官方 |
| **webapp-testing** | `anthropics/webapp-testing/` | Playwright 自动化测试 | Anthropic 官方 |
| **Changelog Generator** | `composio/changelog-generator/` | 生成用户友好更新日志 | ComposioHQ |

### � 文档处理类
强大的 Office 文档与 PDF 处理能力。

| Skill | 目录 | 用途 | 来源 |
|-------|------|------|------|
| **docx** | `anthropics/docx/` | 处理 Word 文档（编辑/批注） | Anthropic 官方 |
| **xlsx** | `anthropics/xlsx/` | 处理 Excel 表格（分析/图表） | Anthropic 官方 |
| **pptx** | `anthropics/pptx/` | 处理 PPT 幻灯片（生成/调整） | Anthropic 官方 |
| **pdf** | `anthropics/pdf/` | PDF 工具箱（提取/合并/注释） | Anthropic 官方 |

### � 创意内容与营销
辅助研究、写作及品牌设计。

| Skill | 目录 | 用途 | 来源 |
|-------|------|------|------|
| **content-research-writer** | `composio/content-research-writer/` | 深度内容研究与引用写作 | ComposioHQ |
| **theme-factory** | `composio/theme-factory/` | 快速应用专业视觉主题 | ComposioHQ |
| **Internationalizing** | `internationalizing-websites/` | Next.js 多语言支持 | 社区贡献 |
| **Shipany** | `shipany/` | AI SaaS 模板开发指南 | 社区贡献 |

### � 数据分析与分析
从数据和记录中提取深度洞察。

| Skill | 目录 | 用途 | 来源 |
|-------|------|------|------|
| **meeting-insights-analyzer** | `composio/meeting-insights-analyzer/` | 会议记录行为模式分析 | ComposioHQ |
| **Google SEO Guide** | `google-official-seo-guide/` | Google 搜索优化最佳实践 | 社区贡献 |

### ⚙️ 效率、组织与性能
优化日常办公流程与网页性能。

| Skill | 目录 | 用途 | 来源 |
|-------|------|------|------|
| **file-organizer** | `composio/file-organizer/` | 智能文件识别与自动归档 | ComposioHQ |
| **invoice-organizer** | `composio/invoice-organizer/` | 自动整理发票与收据 | ComposioHQ |
| **Web Accessibility** | `web-performance-seo/` | 修复 PageSpeed 可访问性问题 | 社区贡献 |
| **Deploying** | `deploying-to-production/` | GitHub + Vercel 自动化部署 | 社区贡献 |
| **Doc Sync Tool** | `doc-sync-tool/` | AI Agent 配置文档同步 | 社区贡献 |

---

## 🚀 快速开始

### 使用 Skill Seekers 创建新 Skill

```bash
# 进入目录
cd skills/skill-seekers

# 估算页面数量
/Users/maxecho/Library/Python/3.13/bin/skill-seekers estimate configs/react.json

# 爬取文档
/Users/maxecho/Library/Python/3.13/bin/skill-seekers scrape --config configs/react.json
```

---

## 📖 完整能力手册

查看根目录下的 [**SKILLS_DOCUMENTATION.md**](../SKILLS_DOCUMENTATION.md) 获取：
- **触发关键词速查表** (中英文对照)
- 26 个 Skills 的详细功能说明
- 完整目录结构与更新日志

---

## 🔗 来源链接

- [AgentSkills.best](https://agentskills.best/zh)
- [Anthropic Official Skills](https://github.com/anthropics/skills)
- [Awesome Agent Skills](https://github.com/littleben/awesomeAgentskills)
- [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers)
- [obra/superpowers](https://github.com/obra/superpowers)
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
