################################ 学习文档解析的过程 ##############################
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
################################ 学习文档解析的过程 ##############################

from langchain_community.document_loaders import (
    TextLoader, PyPDFLoader, Docx2txtLoader, UnstructuredMarkdownLoader
)

import os


def batch_load_documents(folder_path):
    """
   批量加载文件夹内的所有官方支持格式文档（基于新版加载器）
   :param folder_path: 知识库文件夹路径
   :return: 所有文档的Document对象列表
   """
    all_docx = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # 跳过文件夹，只处理文件
        if os.path.isdir(file_path):
            continue
        # 根据文件后缀，选择对应的官方推荐加载器
        try:
            if filename.endswith(".txt"):
                loader = TextLoader(file_path, encoding="utf-8")
            elif filename.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            elif filename.endswith(".docx"):
                loader = Docx2txtLoader(file_path)
            elif filename.endswith(".md"):
                loader = UnstructuredMarkdownLoader(file_path)
            else:
                print(f"不支持的文件格式:{filename}")
                continue
            # 加载并添加到文档
            docs = loader.load()
            all_docx.extend(docs)
            print(f"成功加载：{filename}，生成{len(docs)}个Document对象")
        except Exception as e:
            print(f"加载失败：{filename}，错误信息：{str(e)}")

    return all_docx
