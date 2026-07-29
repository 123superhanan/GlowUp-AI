#%%

from langchain_community.document_loaders import DirectoryLoader, TextLoader

def load_documents(folder_path: str = "./documents"):
    """Load all markdown files from the local folder"""
    loader = DirectoryLoader(
        path=folder_path,
        glob="**/*.md",
        loader_cls=TextLoader,
        show_progress=True
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} documents")
    return docs






#%%

# from langchain_community.document_loaders import DirectoryLoader ,TextLoader,WebBaseLoader
# import os

# os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
# def load_local_documents(folder_path: str = "./documents"):
#     """Load all markdown files from local folder"""
#     loader = DirectoryLoader(
#         path=folder_path,
#         glob="**/*.md",
#         loader_cls=TextLoader,
#         show_progress=True
#     )
#     docs = loader.lazy_load()
#     print(f"Loaded {len(docs)} local documents")
#     return docs
# # %%
# def load_web_documents(urls: list[str]):
#     loader = WebBaseLoader(urls)
#     docs = loader.load()
#     print(f"Loaded {len(docs)} web documents")
#     return docs 
# #%%
# def load_all_documents():
#     # Local MD files
#     local_docs = load_local_documents("./documents")

#     # Example web sources related to men's style/grooming
#     web_urls = [
#         "https://www.menshealth.com/style/",
#         "https://www.gq.com/style",
#         "https://www.byrdie.com/mens-grooming",
#         "https://www.fashionbeans.com/article/mens-grooming-ultimate-guide",
#         "https://www.daimonbarber.com/blogs/journal",
#         "https://peteandpedro.com/blogs/the-pedro-post"

#     ]
#     web_docs = load_web_documents(web_urls)

#     # Combine both
#     all_docs = local_docs + web_docs
#     print(f"Total documents: {len(all_docs)}")
#     return all_docs
# # %%
