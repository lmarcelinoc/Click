# agent_manager.py

class Agent:
    def __init__(self, name):
        self.name = name

    def perform_task(self, task):
        print(f"{self.name} is performing: {task}")

class AgentManager:
    def __init__(self):
        self.agents = {}

    def add_agent(self, name):
        self.agents[name] = Agent(name)

    def assign_task(self, agent_name, task):
        if agent_name in self.agents:
            self.agents[agent_name].perform_task(task)
        else:
            print("Agent not found.")

# Example usage
if __name__ == "__main__":
    manager = AgentManager()
    manager.add_agent("MusicAgent")
    manager.add_agent("ReminderAgent")
    manager.assign_task("MusicAgent", "Play some jazz music")
    manager.assign_task("ReminderAgent", "Set a reminder for tomorrow")

