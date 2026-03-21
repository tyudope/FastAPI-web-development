from app.models import Goal, Routine, Task


def build_goal_analysis_prompt(goal: Goal, routine:Routine, tasks:list[Task]) -> str:

    task_lines = "\n".join(f"- {task.name} : {task.description}" for task in tasks)


    prompt = f"""

You are an expert study strategy assistan.

Analyze the following study plan.

Long-term goal.
Title : {goal.title}
Description: {goal.description}

Routine:
Title:{routine.title}


Tasks:
{task_lines}



Give an analysis with the following sections:

1. Strengths
2. Weaknesses
3. Risks
4. Improvements
5. Recommended adjustments.


Be practical, concise, and specific.

""".strip()
    
    return prompt


