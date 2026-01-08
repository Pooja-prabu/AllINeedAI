def plan_project(query: str, tools: list):
    """
    Takes a project query + ranked tools
    Returns tools grouped by system architecture layers
    """

    plan = {
        "frontend": {
            "tech_stack": [],
            "tools": []
        },
        "backend": {
            "tech_stack": [],
            "tools": []
        },
        "agent": {
            "tools": []
        },
        "integrations": {
            "tools": []
        },
        "deployment": {
            "tools": []
        }
    }

    for tool in tools:
        name = tool.get("name", "")
        category = (tool.get("category") or "").lower()
        tags = [t.lower() for t in (tool.get("tags") or [])]

        # Frontend
        if category in ["frontend", "ui"] or "frontend" in tags:
            plan["frontend"]["tools"].append(tool)

        # Backend
        elif category in ["backend", "api", "database"] or "backend" in tags:
            plan["backend"]["tools"].append(tool)

        # Agent / AI
        elif "agent" in tags or "llm" in tags or "ai" in tags:
            plan["agent"]["tools"].append(tool)

        # Integrations
        elif "integration" in tags or "sms" in tags or "email" in tags:
            plan["integrations"]["tools"].append(tool)

        # Deployment
        elif category in ["cloud", "deployment"] or "deploy" in tags:
            plan["deployment"]["tools"].append(tool)

    return plan
