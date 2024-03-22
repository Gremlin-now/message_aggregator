from include import *

docsearch = Pinecone.from_existing_index(INDEX_NAME, OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY))

query = "Что делать если я убил человека?"
docs = docsearch.similarity_search(query, include_metadata=True)

llm = OpenAI(temperature=0, model_name="text-davinci-003", openai_api_key=OPENAI_API_KEY)
chain = load_qa_chain(llm, chain_type="stuff")

print(chain.run(input_documents=docs[:3], question=query))