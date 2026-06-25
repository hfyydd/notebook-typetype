from ai_prompter import Prompter
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

from open_notebook.ai.provision import provision_langchain_model
from open_notebook.domain.notebook import Source
from open_notebook.domain.transformation import DefaultPrompts, Transformation
from open_notebook.exceptions import OpenNotebookError
from open_notebook.utils import clean_thinking_content
from open_notebook.utils.error_classifier import classify_error
from open_notebook.utils.text_utils import extract_text_content


class TransformationState(TypedDict, total=False):
    input_text: str
    source: Source
    transformation: Transformation
    locale: str
    output: str


async def run_transformation(state: dict, config: RunnableConfig) -> dict:
    source_obj = state.get("source")
    source: Source | None = source_obj if isinstance(source_obj, Source) else None
    content = state.get("input_text")
    assert source or content, "No content to transform"
    transformation: Transformation = state["transformation"]
    locale = (
        state.get("locale")
        or config.get("configurable", {}).get("locale")
        or "en-US"
    )

    try:
        if not content and source:
            content = source.full_text

        localized_fields = transformation.resolve_localized_fields(locale)
        transformation_template_text = localized_fields["prompt"]
        default_prompts: DefaultPrompts = await DefaultPrompts.get_instance()  # type: ignore[assignment]
        default_prompt_text = default_prompts.resolve_transformation_instructions(locale)
        if default_prompt_text:
            transformation_template_text = (
                f"{default_prompt_text}\n\n{transformation_template_text}"
            )

        transformation_template_text = f"{transformation_template_text}\n\n# INPUT"

        system_prompt = Prompter(template_text=transformation_template_text).render(
            data=state
        )
        content_str = str(content) if content else ""
        payload = [SystemMessage(content=system_prompt), HumanMessage(content=content_str)]
        chain = await provision_langchain_model(
            str(payload),
            config.get("configurable", {}).get("model_id"),
            "transformation",
            max_tokens=8192,
        )

        response = await chain.ainvoke(payload)

        response_content = extract_text_content(response.content)
        cleaned_content = clean_thinking_content(response_content)

        if source:
            await source.add_insight(localized_fields["title"], cleaned_content)

        return {
            "output": cleaned_content,
        }
    except OpenNotebookError:
        raise
    except Exception as e:
        error_class, user_message = classify_error(e)
        raise error_class(user_message) from e


agent_state = StateGraph(TransformationState)
agent_state.add_node("agent", run_transformation)  # type: ignore[type-var]
agent_state.add_edge(START, "agent")
agent_state.add_edge("agent", END)
graph = agent_state.compile()
