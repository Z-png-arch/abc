import threading
import queue
import time
import random

# 定义Agent类
class Agent(threading.Thread):
    def __init__(self, agent_id, task_queue, result_queue):
        super().__init__()
        self.agent_id = agent_id
        self.task_queue = task_queue
        self.result_queue = result_queue
    
    def run(self):
        while True:
            # 获取任务
            task = self.task_queue.get()
            if task is None:  # 使用None作为退出信号
                break
            print(f"Agent {self.agent_id} executing task: {task}")
            # 模拟任务执行
            time.sleep(random.uniform(1, 3))  # 随机模拟执行时间
            result = f"Result of {task} by Agent {self.agent_id}"
            # 将结果放入结果队列
            self.result_queue.put(result)
            self.task_queue.task_done()

# 定义任务调度系统
class TaskScheduler:
    def __init__(self, num_agents):
        self.num_agents = num_agents
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.agents = []
    
    def create_agents(self):
        for i in range(self.num_agents):
            agent = Agent(i, self.task_queue, self.result_queue)
            self.agents.append(agent)
    
    def start_agents(self):
        for agent in self.agents:
            agent.start()
    
    def assign_tasks(self, tasks):
        for task in tasks:
            self.task_queue.put(task)
    
    def collect_results(self):
        self.task_queue.join()  # 等待所有任务完成
        results = []
        while not self.result_queue.empty():
            results.append(self.result_queue.get())
        return results
    
    def stop_agents(self):
        for _ in self.agents:
            self.task_queue.put(None)  # 发送停止信号
        for agent in self.agents:
            agent.join()  # 等待所有Agent完成

# 测试代码
if __name__ == "__main__":
    tasks = ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5", "Task 6"]
    scheduler = TaskScheduler(num_agents=3)
    scheduler.create_agents()
    scheduler.start_agents()
    scheduler.assign_tasks(tasks)
    
    # 收集结果
    results = scheduler.collect_results()
    print("All tasks completed. Results:")
    for result in results:
        print(result)
    
    scheduler.stop_agents()
