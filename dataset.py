from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone

# Инициализация Pinecone и создание индекса
pc = Pinecone(api_key="159e533b-5d20-4f3c-93c1-5277f3df9cdb")
index = pc.Index("secon-1", dimension=1536)  # Укажите желаемую размерность векторов

# Пример строки текста
text = "Привет, как дела?"

# Инициализация OpenAIEmbeddings
embeddings = OpenAIEmbeddings(api_key='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')

# Получение вектора для текста
vector = embeddings.embed_query(text)

# Добавление вектора в индекс Pinecone
index.upsert(vectors=[{"id": "some_id", "values": vector}])

print(index)
