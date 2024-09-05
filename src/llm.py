import os
from openai import OpenAI  # 导入OpenAI库用于访问GPT模型
from logger import LOG  # 导入日志模块

class LLM:
    def __init__(self):
        # 创建一个OpenAI客户端实例
        self.client = OpenAI(api_key="sk-56d3e6db885a4a62b8246aa69de2870e", base_url="https://api.deepseek.com")
        # 配置日志文件，当文件大小达到1MB时自动轮转，日志级别为DEBUG
        LOG.add("daily_progress/llm_logs.log", rotation="1 MB", level="DEBUG")

    def generate_daily_report(self, markdown_content, dry_run=False):
        # 构建一个用于生成报告的提示文本，要求生成的报告包含新增功能、主要改进和问题修复
        prompt = f"以下是项目的最新进展，根据功能合并同类项，形成一份简报，至少包含：1）新增功能；2）主要改进；3）修复问题；:\n\n{markdown_content}"
        system_role = """你是一名专业的报告撰写助手，负责帮助用户生成高质量、稳定的报告。在对话过程中，请确保以下几点：
           a. 充分理解用户需求，明确报告的主题和目的；
           b. 提供有针对性的建议，帮助用户完善报告结构；
           c. 在回答问题时，确保信息准确、全面，避免产生误导；
           d. 遵循相关规范和格式要求，提高报告的可读性。"""
        if dry_run:
            # 如果启用了dry_run模式，将不会调用模型，而是将提示信息保存到文件中
            LOG.info("Dry run mode enabled. Saving prompt to file.")
            with open("daily_progress/prompt.txt", "w+") as f:
                f.write(prompt)
            LOG.debug("Prompt saved to daily_progress/prompt.txt")
            return "DRY RUN"

        # 日志记录开始生成报告
        LOG.info("Starting report generation using GPT model.")
        
        try:
            # 调用OpenAI GPT模型生成报告
            response = self.client.chat.completions.create(
                # model="gpt-3.5-turbo",  # 指定使用的模型版本
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": prompt}  # 提交用户角色的消息
                ]
            )
            LOG.debug("GPT response: {}", response)
            # 返回模型生成的内容
            return response.choices[0].message.content
        except Exception as e:
            # 如果在请求过程中出现异常，记录错误并抛出
            LOG.error("An error occurred while generating the report: {}", e)
            raise
