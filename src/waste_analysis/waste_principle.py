class WastePrinciple:
    def __init__(self, name, description, examples):
        self.name = name
        self.description = description
        self.examples = examples

    def __str__(self):
        return f"{self.name}: {self.description}"

    def get_examples(self):
        return f"Examples of {self.name}:\n" + "\n".join(f"- {example}" for example in self.examples)

# Creating instances for each waste principle
overproduction = WastePrinciple(
    "Overproduction",
    "Producing more than is required or before it is needed.",
    ["Manufacturing products in large batches", "Creating reports that no one reads", "Printing documents before they are needed"]
)

waiting = WastePrinciple(
    "Waiting",
    "Time spent waiting for the next step in a process.",
    ["Employees waiting for equipment to be fixed", "Customers waiting in line", "Waiting for approvals or decisions"]
)

transportation = WastePrinciple(
    "Transportation",
    "Unnecessary movement of materials or information.",
    ["Moving work in progress between departments", "Transferring data between incompatible systems", "Excessive email forwarding"]
)

over_processing = WastePrinciple(
    "Over-processing",
    "Doing more work than necessary to produce a product or service.",
    ["Adding features that customers don't need", "Multiple layers of approval for simple decisions", "Excessive quality checks beyond what's necessary"]
)

inventory = WastePrinciple(
    "Inventory",
    "Excess products or materials not being processed.",
    ["Stockpiling raw materials", "Unfinished work accumulating between steps", "Storing obsolete information or data"]
)

motion = WastePrinciple(
    "Motion",
    "Unnecessary movement of people.",
    ["Poor workspace layout causing extra movement", "Searching for misplaced tools or information", "Excessive meetings requiring physical presence"]
)

defects = WastePrinciple(
    "Defects",
    "Errors or problems that require correction.",
    ["Manufacturing errors requiring rework", "Data entry mistakes", "Unclear communication leading to misunderstandings"]
)

unused_creativity = WastePrinciple(
    "Unused Employee Creativity",
    "Failing to leverage employees' skills, ideas, and improvement suggestions.",
    ["Not involving frontline staff in problem-solving", "Ignoring employee suggestions", "Underutilizing employee skills and talents"]
)

waste_principles = [overproduction, waiting, transportation, over_processing, inventory, motion, defects, unused_creativity]