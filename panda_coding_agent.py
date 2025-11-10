# pip install -qU "langchain[anthropic]" to call the model

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
# from langchain_deepseek import ChatDeepSeek
# from langchain_ollama.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import HumanInTheLoopMiddleware
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
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: File {file_path} not found."
    except Exception as e:
        return f"Error: {e}"

def write_file(file_path: str, content: str) -> str:
    """Write content to a file."""
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error: {e}"

def finish_agent() -> str:
    """Finish the agent execution."""
    return "finish"

def grep() -> str:
    """find some code definition in current repo"""
    return ""

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
        tools=[get_weather, get_city, read_file, write_file, finish_agent],
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
        tools=[get_weather, get_city, read_file, write_file, finish_agent],
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
        system_prompt="你是一个资深的工程师，你的目的是根据用户输入的需求，完成代码编写。你应该根据以下步骤完成："
                      "1、先根据当前目录下代码仓库信息，2、做任务规划，生成ToDo，3、对每一个ToDo，编写相关的代码 4、执行测试。 "
                      "你可以使用的工具如下：read_file、write_file、grep",
    )

    ## 场景1：只输出最终的结果
    # result = agent.invoke(
    #     {'messages': '开始'},
    #     stream_mode="values"
    # )
    # result = result["messages"][-1].content
    # print(f"result: {result}")

    ## 场景2：走流式输出
    question = '写一个mcp工具，可以做search网页中的最新内容'
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

if __name__ == '__main__':
    # exeWeatherAgent()
    exeCodingAgent()