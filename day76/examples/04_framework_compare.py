# Day 76 示例 4: 框架对比 - 同一任务不同实现
\"\"\"
用伪代码对比 LangChain、AutoGen、CrewAI 的实现方式
\"\"\"

# ==========================================
# 框架 1: LangChain / LangGraph 风格
# ==========================================
def langchain_style_example():
    \"\"\"
    LangChain 风格 - 使用 Tool + Agent + Executor
    特点：链式调用，Tool 定义明确
    \"\"\"
    
    # 1. 定义工具
    class WeatherTool:
        name = "get_weather"
        description = "获取指定城市的天气"
        
        def run(self, city: str) -> str:
            return f"{city}天气: 晴, 25°C"
    
    class RestaurantTool:
        name = "recommend_restaurant"
        description = "推荐餐厅"
        
        def run(self, city: str, weather: str) -> str:
            return f"{city}推荐: 根据{weather}推荐户外餐厅"
    
    # 2. 创建 Agent
    tools = [WeatherTool(), RestaurantTool()]
    
    # LangChain 伪代码
    prompt = "你是一个旅行助手，先查天气再推荐餐厅"
    # agent = create_react_agent(llm, tools, prompt)
    # result = agent.invoke({"input": "北京今天适合去哪吃"})
    
    print("LangChain: 链式调用，工具标准化，生态丰富")
    return tools


# ==========================================
# 框架 2: AutoGen 风格
# ==========================================
def autogen_style_example():
    \"\"\"
    AutoGen 风格 - 多 Agent 对话
    特点：Agent 之间通过对话协作
    \"\"\"
    
    # 伪代码 - Agent 定义
    class WeatherAgent:
        system_message = "你是天气专家，负责查询天气"
        
        def get_weather(self, city):
            return f"{city}: 晴, 25°C"
    
    class FoodAgent:
        system_message = "你是美食家，负责推荐餐厅"
        
        def recommend(self, city, weather):
            return f"{city}推荐: {weather}下适合的餐厅"
    
    # AutoGen 伪代码
    # user_proxy = UserProxyAgent("user")
    # weather_agent = WeatherAgent("weather_expert")
    # food_agent = FoodAgent("food_expert")
    # 
    # user_proxy.initiate_chat(
    #     weather_agent,
    #     message="北京今天天气如何？然后推荐餐厅"
    # )
    
    print("AutoGen: 多Agent对话，角色分工，自动协作")
    return [WeatherAgent(), FoodAgent()]


# ==========================================
# 框架 3: CrewAI 风格
# ==========================================
def crewai_style_example():
    \"\"\"
    CrewAI 风格 - 团队协作
    特点：定义角色+任务+流程
    \"\"\"
    
    # 伪代码 - 角色定义
    class Researcher:
        role = "数据研究员"
        goal = "收集准确的天气数据"
        backstory = "你是一个资深的气象学家..."
    
    class Recommender:
        role = "美食推荐官"
        goal = "推荐最佳餐厅"
        backstory = "你是一个美食博主..."
    
    # CrewAI 伪代码
    # researcher = Agent(
    #     role="数据研究员",
    #     goal="收集准确的天气数据",
    #     backstory="你是一个资深的气象学家...",
    #     tools=[WeatherTool()]
    # )
    # 
    # task1 = Task(
    #     description="查询北京今天天气",
    #     agent=researcher
    # )
    # 
    # crew = Crew(
    #     agents=[researcher, recommender],
    #     tasks=[task1, task2],
    #     process=Process.sequential
    # )
    # result = crew.kickoff()
    
    print("CrewAI: 团队协作，角色驱动，流程编排")


# 演示对比
if __name__ == "__main__":
    print("框架对比：查询天气 + 推荐餐厅\n")
    
    print("1. LangChain:")
    langchain_style_example()
    
    print("\n2. AutoGen:")
    autogen_style_example()
    
    print("\n3. CrewAI:")
    crewai_style_example()
    
    print("\n" + "=" * 50)
    print("选择建议:")
    print("  - 通用Agent → LangChain/LangGraph")
    print("  - 多Agent对话 → AutoGen")
    print("  - 团队协作模拟 → CrewAI")
    print("  - 类型安全 → PydanticAI")
