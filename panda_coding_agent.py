# pip install -qU "langchain[anthropic]" to call the model

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, FunctionMessage
# from langchain_deepseek import ChatDeepSeek
# from langchain_ollama.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import HumanInTheLoopMiddleware

from prompt.coding_v1_prompt import plan_act_prompt
from tools.grep.custom_grep_tool import custom_grep


# from langgraph.checkpoint.memory import InMemorySaver


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    if city == "杭州":
        return f"晴天： {city}!"
    if city == "北京":
        return f"下雨： {city}!"
    if city == "上海":
        return f"多云： {city}!"
    return f"未知城市： {city}!"


def get_city(city: str) -> str:
    """Get weather for a given city."""
    return f"当前是杭州!"


def read_file(file_path: str) -> str:
    """Read the content of a file."""
    try:
        print("will read file")
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: File {file_path} not found."
    except Exception as e:
        return f"Error: {e}"


def write_file(file_path: str, content: str) -> str:
    """Write content to a file."""
    try:
        print("will write file")
        with open(file_path, 'w') as file:
            file.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error: {e}"


def finish_agent() -> str:
    """Finish the agent execution."""
    return "finish"


def local_grep() -> str:
    """A powerful search tool built on ripgrep for searching file contents with regex patterns.

    ALWAYS use this tool for search tasks. NEVER invoke `grep` or `rg` as a Bash command.
    Supports full regex syntax, file filtering, and various output modes.

    Args:
        pattern: The regular expression pattern to search for in file contents.
                Uses ripgrep syntax - literal braces need escaping (e.g., `interface\\{\\}` for `interface{}`).
        path: File or directory to search in. Defaults to current working directory if not specified.
        glob: Glob pattern to filter files (e.g., "*.js", "*.{ts,tsx}").
        output_mode: Output mode - "content" shows matching lines with optional context,
                    "files_with_matches" shows only file paths (default),
                    "count" shows match counts per file.
        B: Number of lines to show before each match. Only works with output_mode="content".
        A: Number of lines to show after each match. Only works with output_mode="content".
        C: Number of lines to show before and after each match. Only works with output_mode="content".
        n: Show line numbers in output. Only works with output_mode="content".
        i: Enable case insensitive search.
        type: File type to search (e.g., "js", "py", "rust", "go", "java").
             More efficient than glob for standard file types.
        head_limit: Limit output to first N lines/entries. Works across all output modes.
        multiline: Enable multiline mode where patterns can span lines and . matches newlines.
                  Default is False (single-line matching only).

    Returns:
        Search results as a string, formatted according to the output_mode."""
    return ""


def sequential_thinking() -> str:
    """A detailed tool for dynamic and reflective problem-solving through thoughts.
This tool helps analyze problems through a flexible thinking process that can adapt and evolve.
Each thought can build on, question, or revise previous insights as understanding deepens.

When to use this tool:
- Breaking down complex problems into steps
- Planning and design with room for revision
- Analysis that might need course correction
- Problems where the full scope might not be clear initially
- Problems that require a multi-step solution
- Tasks that need to maintain context over multiple steps
- Situations where irrelevant information needs to be filtered out

Key features:
- You can adjust total_thoughts up or down as you progress
- You can question or revise previous thoughts
- You can add more thoughts even after reaching what seemed like the end
- You can express uncertainty and explore alternative approaches
- Not every thought needs to build linearly - you can branch or backtrack
- Generates a solution hypothesis
- Verifies the hypothesis based on the Chain of Thought steps
- Repeats the process until satisfied
- Provides a correct answer

Parameters explained:
- thought: Your current thinking step, which can include:
  * Regular analytical steps
  * Revisions of previous thoughts
  * Questions about previous decisions
  * Realizations about needing more analysis
  * Changes in approach
  * Hypothesis generation
  * Hypothesis verification
- next_thought_needed: True if you need more thinking, even if at what seemed like the end
- thought_number: Current number in sequence (can go beyond initial total if needed)
- total_thoughts: Current estimate of thoughts needed (can be adjusted up/down)
- is_revision: A boolean indicating if this thought revises previous thinking
- revises_thought: If is_revision is true, which thought number is being reconsidered
- branch_from_thought: If branching, which thought number is the branching point
- branch_id: Identifier for the current branch (if any)
- needs_more_thoughts: If reaching end but realizing more thoughts needed"""
    return "current thinking result is: %s"


# model = ChatDeepSeek(model="deepseek-chat", api_key="sk-xxxx", )
# model = ChatOllama(base_url="http://127.0.0.1:11434/", model="deepseek-r1:14b", temperature=0.7, keep_alive="5m", )
# model = init_chat_model(
#         model="deepseek-chat",
#         base_url="https://api.deepseek.com",
#         api_key=""
#     )

# model = init_chat_model(
#         model="doubao-seed-1-6-250615",
#         base_url="https://ark.cn-beijing.volces.com/api/v3",
#         api_key=""
#     )


def exeWeatherAgent():
    model = ChatOpenAI(
        # model="doubao-seed-1-6-251015",
        model="",
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key="",  # 替换为你自己的 Key
        temperature=0,
        max_tokens=8 * 1024,
        extra_body={
            "thinking": {
                "type": "disabled"  # 如果需要推理，这里可以设置为 "auto"
            }
        }
    )

    agent = create_agent(
        model=model,
        tools=[get_weather, get_city, read_file, write_file, finish_agent, sequential_thinking],
        middleware=[HumanInTheLoopMiddleware(
            interrupt_on={
                # "write_file": True,  # All decisions (approve, edit, reject) allowed
                "execute_sql": {"allowed_decisions": ["approve", "reject"]},  # No editing allowed
                # "read_data": True, # 读文件需要中断
                # "read_file": True, # 读文件需要中断
            },
            # Prefix for interrupt messages - combined with tool name and args to form the full message
            # e.g., "Tool execution pending approval: execute_sql with query='DELETE FROM...'"
            # Individual tools can override this by specifying a "description" in their interrupt config
            description_prefix="Tool execution pending approval",
        )],
        # checkpointer=InMemorySaver(),
        system_prompt="从本地文件city.json中读取所有的城市，获取当前城市的天气。 必须完成2轮判断，你才可以使用finish工具结束任务。并将最终结果写入到文件weather.json中",
    )

    ## 场景1：只输出最终的结果
    # result = agent.invoke(
    #     {'messages': '开始'},
    #     stream_mode="values"
    # )
    # result = result["messages"][-1].content
    # print(f"result: {result}")

    ## 场景2：走流式输出
    question = ''
    for step in agent.stream(
            {'messages': question},
            stream_mode="values"
    ):
        ## 存在key为"messages"的元素，则打印
        if "messages" in step:
            step["messages"][-1].pretty_print()
        elif "__interrupt__" in step:
            print(f'step["__interrupt__"]: {step["__interrupt__"]}')
            # 人工确认是否继续
            user_input = input("是否继续执行该工具？输入 yes 继续，其他键放弃：").strip().lower()
            if user_input == "yes":
                # 用户同意，继续后续流程
                print("用户确认继续，工具将被调用…")
                continue
            else:
                print("放弃")


def exeCodingAgent():
    model = ChatOpenAI(
        # model="doubao-seed-1-6-251015",
        model="",
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key="",  # 替换为你自己的 Key
        temperature=0,
        max_tokens=8 * 1024,
        extra_body={
            "thinking": {
                "type": "disabled"  # 如果需要推理，这里可以设置为 "auto"
            }
        }
    )

    agent = create_agent(
        model=model,
        tools=[get_weather, get_city, read_file, write_file, finish_agent, sequential_thinking, custom_grep],
        middleware=[HumanInTheLoopMiddleware(
            interrupt_on={
                # "write_file": True,  # All decisions (approve, edit, reject) allowed
                "execute_sql": {"allowed_decisions": ["approve", "reject"]},  # No editing allowed
                # "read_data": True, # 读文件需要中断
                # "read_file": True, # 读文件需要中断
            },
            # Prefix for interrupt messages - combined with tool name and args to form the full message
            # e.g., "Tool execution pending approval: execute_sql with query='DELETE FROM...'"
            # Individual tools can override this by specifying a "description" in their interrupt config
            description_prefix="Tool execution pending approval",
        )],
        # checkpointer=InMemorySaver(),
        system_prompt=plan_act_prompt,
    )

    ## 场景1：只输出最终的结果
    # result = agent.invoke(
    #     {'messages': '开始'},
    #     stream_mode="values"
    # )
    # result = result["messages"][-1].content
    # print(f"result: {result}")

    ## 场景2：走流式输出
    question = '根据custom_grep的注释，实现自定义的custom_grep工具'
    for step in agent.stream(
            {'messages': question},
            stream_mode="values"
    ):
        message = step["messages"][-1]
        if isinstance(message, HumanMessage):
            print(f'human message: {message}')
        if isinstance(message, AIMessage):
            print(f'ai message: {message}')
        if isinstance(message, ToolMessage):
            print(f'tool message: {message}')
        if isinstance(message, FunctionMessage):
            print(f'function message: {message}')
        ## 存在key为"messages"的元素，则打印
        if "messages" in step:
            step["messages"][-1].pretty_print()
        elif "__interrupt__" in step:
            print(f'step["__interrupt__"]: {step["__interrupt__"]}')
            # 人工确认是否继续
            user_input = input("是否继续执行该工具？输入 yes 继续，其他键放弃：").strip().lower()
            if user_input == "yes":
                # 用户同意，继续后续流程
                print("用户确认继续，工具将被调用…")
                continue
            else:
                print("放弃")


if __name__ == '__main__':
    # exeWeatherAgent()
    exeCodingAgent()
