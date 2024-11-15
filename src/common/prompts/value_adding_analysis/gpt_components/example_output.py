# File: example_output_variations.py

EXAMPLE_OUTPUTS = {
    "simple_process": """
    Here's an example of the expected output for a simple process:

    classify("VA", "Submit Order", "Fill out order form", "Directly contributes to customer's goal of placing an order.")
    classify("BVA", "Submit Order", "Verify customer information", "Necessary for business operations but not directly valuable to customer.")
    classify("VA", "Submit Order", "Confirm order details", "Ensures accuracy of the order, directly benefiting the customer.")
    classify("NVA", "Submit Order", "Wait for system update", "Waiting time does not add value to the customer or the business.")
    classify("VA", "Process Payment", "Accept payment", "Directly fulfills customer's need to complete the transaction.")
    classify("BVA", "Process Payment", "Generate invoice", "Required for business record-keeping but not directly valuable to customer.")
    """,

    "complex_process": """
    Here's an example of the expected output for a more complex process:

    # Customer Onboarding
    classify("VA", "Customer Onboarding", "Collect customer requirements", "Directly addresses customer needs and initiates value creation.")
    classify("BVA", "Customer Onboarding", "Verify customer identity", "Necessary for regulatory compliance but not directly valuable to customer.")
    classify("VA", "Customer Onboarding", "Set up customer account", "Enables customer to access services, directly adding value.")
    classify("NVA", "Customer Onboarding", "Internal system synchronization", "Technical delay that doesn't add value to customer or business processes.")

    # Service Provisioning
    classify("VA", "Service Provisioning", "Configure service parameters", "Directly tailors the service to customer specifications.")
    classify("BVA", "Service Provisioning", "Conduct internal quality check", "Ensures service quality but is not directly perceived by customer.")
    classify("VA", "Service Provisioning", "Activate customer service", "Directly delivers the core value proposition to the customer.")
    classify("NVA", "Service Provisioning", "Wait for third-party integration", "Delay in process that doesn't contribute value.")

    # Follow-up
    classify("VA", "Follow-up", "Collect customer feedback", "Directly engages with customer to improve their experience.")
    classify("BVA", "Follow-up", "Update customer records", "Maintains accurate information for future interactions but not directly valuable to customer.")
    classify("NVA", "Follow-up", "Rework incorrect service configuration", "Correcting errors doesn't add new value, indicates process inefficiency.")
    """,
    
"varied_process": """
Here's an example of the expected output for a simple process:
classify("BVA", "Restaurant Operation", "Record daily sales figures", "Essential for financial tracking but doesn't directly enhance the customer's meal.")
classify("VA", "Manufacturing Process", "Assemble product components", "Directly contributes to creating the product that customers will purchase.")
classify("NVA", "Office Management", "Manually sort incoming mail by department", "Time-consuming task that could be eliminated with digital communication.")
classify("VA", "Customer Service", "Resolve customer complaint", "Directly addresses and solves a customer's issue, improving their experience.")
classify("BVA", "Human Resources", "Conduct annual employee review", "Necessary for employee development but doesn't directly impact customer value.")
classify("VA", "Product Development", "Test new product features", "Directly contributes to improving the product for customers.")
classify("BVA", "Retail Store Operation", "Restock inventory shelves", "Necessary for business operations but doesn't directly add value to the product.")
classify("NVA", "Data Management", "Maintain duplicate paper and digital records", "Redundant process that consumes resources without adding value.")
classify("VA", "Healthcare Service", "Perform medical diagnosis", "Directly contributes to addressing the patient's health concerns.")
classify("BVA", "Software Development", "Document code changes", "Supports long-term maintenance but doesn't immediately impact software functionality.")
""",

"custom_process": """
Here are examples of the expected output for various steps:

classify("VA", "Review Application", "Analyze credit score", "Directly impacts the decision-making process for loan approval.")
classify("BVA", "Document Processing", "Scan physical documents", "Necessary for digital record-keeping, though not directly impacting the decision.")
classify("NVA", "Data Entry", "Manually input data from paper forms", "Could be eliminated through digital application process, reducing errors and time.")
classify("VA", "Customer Interview", "Discuss financial goals", "Provides crucial information for tailoring the product offering to the customer's needs.")
classify("BVA", "Compliance Check", "Verify customer identity", "Essential for legal requirements, but doesn't directly influence the application decision.")
classify("NVA", "Internal Communication", "Update team on application status via email", "Could be replaced with an automated system notification, reducing time and potential miscommunication.")
classify("VA", "Risk Assessment", "Evaluate collateral value", "Directly impacts the terms and approval of the loan application.")
classify("BVA", "Customer Support", "Answer applicant's process-related questions", "Facilitates smooth application process but doesn't directly affect the decision.")
classify("NVA", "File Management", "Print and file physical copies of digital documents", "Redundant step in a digital age, consuming resources without adding value.")
classify("VA", "Offer Customization", "Adjust interest rate based on risk profile", "Directly impacts the value proposition to the customer and the application outcome.")
"""
}