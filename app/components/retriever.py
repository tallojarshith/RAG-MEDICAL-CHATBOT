from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from app.components.llm import load_llm
from app.components.vector_store import load_vector_store
from app.config.config import HUGGINGFACE_REPO_ID, HF_TOKEN
from app.common.logger import get_logger
from app.common.custom_exception import CustomException


logger = get_logger(__name__)


CUSTOM_PROMPT_TEMPLATE = """
You are a medical information assistant.

Answer the question in 2-3 lines maximum using only the information
provided in the context.

If the answer is not present in the context, say:
"I could not find this information in the provided medical documents."

Context:
{context}

Question:
{input}

Answer:
"""


def set_custom_prompt():
    return ChatPromptTemplate.from_template(
        CUSTOM_PROMPT_TEMPLATE
    )


def create_qa_chain():
    try:
        logger.info("Loading vector store for context")

        db = load_vector_store()

        if db is None:
            raise ValueError("Vector store not present or empty")

        logger.info("Loading LLM")

        llm = load_llm(
            huggingface_repo_id=HUGGINGFACE_REPO_ID,
            hf_token=HF_TOKEN
        )

        if llm is None:
            raise ValueError("LLM not loaded")

        retriever = db.as_retriever(
            search_kwargs={"k": 3}
        )

        prompt = set_custom_prompt()

        document_chain = create_stuff_documents_chain(
            llm,
            prompt
        )

        qa_chain = create_retrieval_chain(
            retriever,
            document_chain
        )

        logger.info("Successfully created QA chain")

        return qa_chain

    except Exception as e:
        error_message = CustomException(
            "Failed to create QA chain",
            e
        )

        logger.error(str(error_message))
        raise error_message