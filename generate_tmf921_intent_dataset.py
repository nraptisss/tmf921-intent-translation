#!/usr/bin/env python3
"""
TMF921 Intent Management Dataset Generator
Generates 1000 NL Intent examples mapped to TMF921 Intent types
"""

import json
import random
from datetime import datetime, timedelta
import uuid

# TMF921 Intent Types
INTENT_TYPES = [
    "Intent",
    "ProbeIntent",
    "IntentSpecification",
    "IntentReport"
]

# Lifecycle States
LIFECYCLE_STATES = ["Created", "Active"]

# Reporting Events
REPORTING_EVENTS = [
    "StateComplies",
    "StateDegrades",
    "ReportingIntervalExpired",
    "IntentRejected",
    "HandlingEnded",
    "UpdateRejected",
    "UpdateFinished"
]

# Expectation Types
EXPECTATION_TYPES = [
    "DeliveryExpectation",
    "PropertyExpectation",
    "ReportingExpectation"
]

# Service Types
SERVICE_TYPES = [
    "EventWirelessAccess",
    "StreamingApplication",
    "NetworkSlice",
    "BroadbandService",
    "CloudService",
    "EdgeComputing",
    "IoTService",
    "VideoStreaming",
    "VoiceService",
    "DataAnalytics"
]

# Application Types
APP_TYPES = [
    "AWS MediaLive",
    "Facebook Live",
    "YouTube",
    "Zoom",
    "Microsoft Teams",
    "Webex",
    "Google Meet",
    "Twitch",
    "Custom Application"
]

# Service Quality Levels
SERVICE_QUALITIES = [
    "4KUHD",
    "1080pHD",
    "720p",
    "480p",
    "Standard",
    "Premium",
    "Basic"
]

# Context Domains
CONTEXT_DOMAINS = [
    "Broadband services",
    "Autonomous services",
    "intent-based networks",
    "5G networks",
    "IoT networks",
    "Cloud services",
    "Edge computing",
    "Video streaming",
    "Enterprise networks",
    "Smart city"
]

# Priority Levels
PRIORITY_LEVELS = ["1", "2", "3", "4", "5"]

# Reporting Intervals
REPORTING_INTERVALS = [5, 10, 15, 30, 60]  # minutes

# Property Parameters
LATENCY_VALUES = ["5 ms", "10 ms", "12 ms", "20 ms", "50 ms", "100 ms"]
PARTICIPANT_COUNTS = [50, 100, 200, 500, 1000, 5000]
THROUGHPUT_VALUES = ["100 Mbps", "500 Mbps", "1 Gbps", "10 Gbps"]
AVAILABILITY_VALUES = ["99.9%", "99.95%", "99.99%", "99.999%"]

# Network Slice Parameters
NSSI_IDS = [
    "NEST-EMBB_VIDEOSTREAMING_INSIDE_VENUE_5G",
    "NEST-URLLC_AUTOMATION_FACTORY",
    "NEST-MMTC_SENSOR_NETWORK",
    "NEST-EMBB_STADIUM_ULTRA_DENSE"
]
NSI_IDS = [
    "NSI-001",
    "NSI-002",
    "NSI-003",
    "NSI-VENUE-5G",
    "NSI-FACTORY-AUTO"
]

# Geographic Areas
AREAS = [
    "Stadium arena",
    "Convention center",
    "Factory floor",
    "Hospital campus",
    "University campus",
    "Airport terminal",
    "Shopping mall",
    "Smart city district",
    "Industrial zone",
    "Residential area"
]

# NL Intent Templates for different actions

# CREATE Intent templates
CREATE_INTENT_TEMPLATES = [
    "Create an intent to {service_description}",
    "I want to {service_description} with {quality_requirement}",
    "Set up a new intent for {service_description}",
    "Request a {service_type} with {property_requirement}",
    "Define an intent to deliver {service_description}",
    "Establish intent for {service_description}",
    "I need an intent configured for {service_description}",
    "Configure a new {service_type} intent",
    "Set up {service_description} with priority {priority}",
    "Create intent to provision {service_description}",
    "Add a new intent for {service_description}",
    "Initiate {service_description} service intent",
    "Register a service intent for {service_description}",
    "Deploy intent for {service_description}",
    "Start a new {service_type} with {quality_requirement}",
    "Place an intent for {service_description}",
    "Order a {service_type} service with {property_requirement}",
    "Submit intent for {service_description}",
    "Request deployment of {service_description}",
    "Generate intent for {service_description}"
]

# QUERY/READ Intent templates
QUERY_INTENT_TEMPLATES = [
    "Show me the intent with ID {intent_id}",
    "Get details of intent {intent_id}",
    "What is the status of intent {intent_id}?",
    "Find intent named {intent_name}",
    "Retrieve intent {intent_id} information",
    "List all intents in the system",
    "Show all active intents",
    "Get all intents with priority {priority}",
    "Find intents related to {service_type}",
    "What intents exist for {context_domain}?",
    "Search for intent {intent_id}",
    "Display intent {intent_id} details",
    "Check status of {intent_name}",
    "View the {intent_name} intent",
    "Show information about intent {intent_id}",
    "Look up intent {intent_id}",
    "Fetch the intent {intent_id}",
    "Report on intent {intent_id}",
    "What is the state of {intent_name}?",
    "Get the current status of {intent_name}"
]

# UPDATE/PATCH Intent templates
UPDATE_INTENT_TEMPLATES = [
    "Update intent {intent_id} to {new_requirement}",
    "Change the priority of intent {intent_id} to {priority}",
    "Modify {intent_name} quality to {quality_requirement}",
    "Update the deadline for intent {intent_id} to {deadline}",
    "Extend intent {intent_id} validity period",
    "Change the target of intent {intent_id}",
    "Adjust {intent_name} parameters",
    "Set new property value for {intent_name}",
    "Modify intent {intent_id} description",
    "Update the context of {intent_name} to {context_domain}",
    "Change {intent_name} priority level to {priority}",
    "Edit intent {intent_id} specifications",
    "Revise {intent_name} requirements",
    "Update intent {intent_id} with new values",
    "Patch intent {intent_name} configuration",
    "Amend intent {intent_id} parameters",
    "Alter the properties of {intent_name}",
    "Replace values in intent {intent_id}",
    "Refresh intent {intent_id} settings",
    "Modify the expression of intent {intent_name}"
]

# DELETE Intent templates
DELETE_INTENT_TEMPLATES = [
    "Delete intent {intent_id}",
    "Remove intent {intent_name}",
    "Cancel intent {intent_id}",
    "Terminate intent {intent_name}",
    "Delete the intent for {service_description}",
    "Remove the {service_type} intent",
    "Destroy intent {intent_id}",
    "Eliminate intent {intent_name}",
    "Withdraw intent {intent_id}",
    "Erase intent {intent_name}",
    "Purge intent {intent_id}",
    "Cancel all {service_type} intents",
    "Delete expired intents",
    "Remove completed intents",
    "Clean up intent {intent_name}",
    "Take down intent {intent_id}",
    "Unregister intent {intent_name}",
    "Discontinue intent {intent_id}",
    "Abort intent {intent_name}",
    "Drop intent {intent_id}"
]

# PROBE Intent templates
PROBE_INTENT_TEMPLATES = [
    "Probe intent {intent_id} to check feasibility",
    "Test if we can {service_description}",
    "Check availability for {service_type}",
    "Probe the system for {service_description} capability",
    "What would happen if we {service_description}?",
    "Simulate intent for {service_description}",
    "Preview the {service_type} intent outcome",
    "Evaluate feasibility of {service_description}",
    "Check compliance for {service_description}",
    "Probe reporting status of intent {intent_id}",
    "Test intent expression for {service_description}",
    "Verify if {service_description} is achievable",
    "Check system capability for {service_description}",
    "Probe {service_type} service configuration",
    "Assess intent {intent_id} viability",
    "Evaluate {service_description} parameters",
    "Test {quality_requirement} capability",
    "Check latency requirements for {service_description}",
    "Probe network slice {nssi_id} status",
    "Verify {context_domain} readiness"
]

# REPORT Intent templates
REPORT_INTENT_TEMPLATES = [
    "Generate report for intent {intent_id}",
    "Get compliance report for {intent_name}",
    "Show status report of intent {intent_id}",
    "What is the reporting status of {intent_name}?",
    "Get intent report for {service_description}",
    "Display report for {service_type}",
    "Generate compliance status report",
    "Get degradation report for intent {intent_id}",
    "Show all reporting events for {intent_name}",
    "What is the current state compliance?",
    "Get intent health report",
    "Generate monitoring report for {service_description}",
    "Show intent evaluation report",
    "What are the reporting metrics?",
    "Get intent state report",
    "Generate performance report for intent {intent_id}",
    "Show intent validation results",
    "What is the compliance status report?",
    "Get monitoring data for {intent_name}",
    "Generate intent assessment report"
]

# SPECIFICATION Intent templates
SPECIFICATION_INTENT_TEMPLATES = [
    "Create intent specification for {service_description}",
    "Define template for {service_type} intent",
    "Set up intent specification for {quality_requirement}",
    "Create intent schema for {service_description}",
    "Define new intent type for {service_type}",
    "Create specification template for {service_description}",
    "Register intent specification for {service_type}",
    "Set up intent blueprint for {service_description}",
    "Define intent model for {service_type}",
    "Create intent specification with parameters {property_requirement}",
    "Establish intent template for {service_description}",
    "Configure intent specification for {context_domain}",
    "Design intent specification for {service_type}",
    "Create intent class for {service_description}",
    "Register new intent specification",
    "Add intent specification template",
    "Create specification for {service_type} intent",
    "Define intent specification parameters",
    "Set up intent model for {service_description}",
    "Create intent type definition for {service_type}"
]

# Service descriptions for variety
SERVICE_DESCRIPTIONS = [
    "deliver 4K ultra HD video streaming to 200 participants in the stadium",
    "provide low latency connectivity for factory automation with 5ms latency",
    "enable high bandwidth connectivity for the convention center",
    "deploy network slice with 99.999% availability",
    "provide video streaming service for the event venue",
    "enable edge computing capabilities for autonomous vehicles",
    "deliver IoT connectivity for sensor networks with 10000 devices",
    "provide broadband service for residential area with 1Gbps throughput",
    "enable video conferencing with 500 concurrent participants",
    "deploy private 5G network for industrial automation",
    "provide smart city connectivity for urban infrastructure",
    "enable telehealth services with guaranteed bandwidth",
    "deploy augmented reality service for retail stores",
    "provide mission critical communications for emergency services",
    "enable connected car services with ultra reliable low latency",
    "deploy smart grid connectivity for utility management",
    "provide immersive gaming services with minimal latency",
    "enable remote surgery capabilities with 1ms latency",
    "deploy connected logistics for supply chain management",
    "provide holographic communication services"
]

# Quality requirements
QUALITY_REQUIREMENTS = [
    "4K UHD quality",
    "1080p HD quality",
    "low latency under 10ms",
    "ultra low latency under 5ms",
    "high availability of 99.99%",
    "premium service quality",
    "standard quality",
    "high bandwidth 10Gbps",
    "medium bandwidth 1Gbps",
    "low bandwidth 100Mbps",
    "real-time performance",
    "near real-time performance",
    "asynchronous processing",
    "synchronous processing",
    "mission critical reliability"
]

# Property requirements
PROPERTY_REQUIREMENTS = [
    "minimum 99.99% availability",
    "latency under 12ms",
    "200 concurrent users",
    "1000 device capacity",
    "10Gbps throughput",
    "coverage in stadium arena",
    "enterprise grade security",
    "multi-region deployment",
    "edge computing support",
    "5G connectivity",
    "network slicing capability",
    "QoS guarantee",
    "SLA compliance",
    "24/7 availability",
    "geographic redundancy"
]


def generate_uuid():
    """Generate a unique identifier"""
    return str(uuid.uuid4())


def generate_intent_id():
    """Generate an intent ID like in the spec examples"""
    return str(random.randint(20000, 99999))


def generate_intent_name():
    """Generate a descriptive intent name"""
    prefixes = [
        "EventLive", "NetworkSlice", "Broadband", "CloudService", "EdgeCompute",
        "VideoStream", "IoTConnect", "SmartCity", "FactoryAuto", "Telehealth",
        "Gaming", "MissionCritical", "Autonomous", "ConnectedCar", "SmartGrid"
    ]
    suffixes = ["Intent", "Service", "Deployment", "Provision", "Setup"]
    numbers = ["001", "002", "A", "B", "C", "v1", "v2"]
    return f"{random.choice(prefixes)}{random.choice(suffixes)}{random.choice(numbers)}"


def generate_valid_for():
    """Generate a validity period"""
    start = datetime.now() + timedelta(days=random.randint(0, 30))
    end = start + timedelta(days=random.randint(30, 365))
    return {
        "startDateTime": start.isoformat() + "Z",
        "endDateTime": end.isoformat() + "Z"
    }


def generate_related_party():
    """Generate related party information"""
    roles = ["Owner", "Provider", "User", "Administrator", "Operator"]
    party_types = ["Organization", "Individual"]
    return {
        "role": random.choice(roles),
        "partyOrPartyRole": {
            "@type": random.choice(party_types),
            "name": f"Party_{generate_uuid()[:8]}"
        }
    }


def generate_expression():
    """Generate a simplified intent expression"""
    expression_types = ["JsonLdExpression"]
    iri_base = "https://mycsp.com:8080/tmf-api/rdfs/"
    return {
        "@type": random.choice(expression_types),
        "iri": f"{iri_base}expression-{generate_uuid()[:8]}",
        "expressionValue": {
            "@context": {
                "icm": "http://tio.models.tmforum.org/tio/v1.0.0/IntentCommonModel#",
                "ido": "http://www.idan-tmforum-catalyst.org/IntentDrivenAutonomousNetworks#"
            },
            "@graph": [
                {
                    "@id": f"ido:Intent_{generate_uuid()[:8]}",
                    "@type": "icm:Intent",
                    "icm:intentOwner": f"ido:IntentManager_{generate_uuid()[:8]}",
                    "icm:layer": random.choice(["resource", "service", "application"]),
                    "icm:hasExpectation": [
                        {
                            "@id": f"ido:Expectation_{generate_uuid()[:8]}",
                            "@type": f"icm:{random.choice(EXPECTATION_TYPES)}"
                        }
                    ]
                }
            ]
        }
    }


def generate_characteristics():
    """Generate intent characteristics"""
    chars = []
    num_chars = random.randint(1, 4)

    char_templates = [
        {"name": "isTimeConstrained", "valueType": "boolean", "value": random.choice([True, False])},
        {"name": "requiresSLA", "valueType": "boolean", "value": True},
        {"name": "geographicScope", "valueType": "string", "value": random.choice(AREAS)},
        {"name": "deploymentModel", "valueType": "string", "value": random.choice(["Centralized", "Distributed", "Hybrid"])},
        {"name": "securityLevel", "valueType": "string", "value": random.choice(["High", "Medium", "Low"])},
        {"name": "dataRetention", "valueType": "number", "value": random.randint(30, 365)},
        {"name": "maxConcurrentUsers", "valueType": "number", "value": random.choice(PARTICIPANT_COUNTS)},
        {"name": "serviceLevel", "valueType": "string", "value": random.choice(SERVICE_QUALITIES)}
    ]

    selected_chars = random.sample(char_templates, min(num_chars, len(char_templates)))
    for i, char in enumerate(selected_chars):
        chars.append({
            "id": f"char_{generate_uuid()[:8]}",
            **char
        })

    return chars


def generate_nl_intent_entry(intent_type, action, template_type):
    """Generate a single NL Intent entry with TMF921 mapping"""

    # Fill template variables
    template_vars = {
        "intent_id": generate_intent_id(),
        "intent_name": generate_intent_name(),
        "service_description": random.choice(SERVICE_DESCRIPTIONS),
        "service_type": random.choice(SERVICE_TYPES),
        "quality_requirement": random.choice(QUALITY_REQUIREMENTS),
        "property_requirement": random.choice(PROPERTY_REQUIREMENTS),
        "priority": random.choice(PRIORITY_LEVELS),
        "context_domain": random.choice(CONTEXT_DOMAINS),
        "nssi_id": random.choice(NSSI_IDS),
        "deadline": (datetime.now() + timedelta(days=random.randint(7, 90))).strftime("%Y-%m-%d"),
        "new_requirement": random.choice(SERVICE_DESCRIPTIONS)
    }

    # Select appropriate template
    if template_type == "CREATE":
        template = random.choice(CREATE_INTENT_TEMPLATES)
    elif template_type == "QUERY":
        template = random.choice(QUERY_INTENT_TEMPLATES)
    elif template_type == "UPDATE":
        template = random.choice(UPDATE_INTENT_TEMPLATES)
    elif template_type == "DELETE":
        template = random.choice(DELETE_INTENT_TEMPLATES)
    elif template_type == "PROBE":
        template = random.choice(PROBE_INTENT_TEMPLATES)
    elif template_type == "REPORT":
        template = random.choice(REPORT_INTENT_TEMPLATES)
    elif template_type == "SPECIFICATION":
        template = random.choice(SPECIFICATION_INTENT_TEMPLATES)
    else:
        template = random.choice(CREATE_INTENT_TEMPLATES)

    # Generate natural language intent
    nl_intent = template.format(**template_vars)

    # Map to TMF921 action type
    tmf921_action_map = {
        "CREATE": "POST",
        "QUERY": "GET",
        "UPDATE": "PATCH",
        "DELETE": "DELETE",
        "PROBE": "POST (ProbeIntent)",
        "REPORT": "GET (IntentReport)",
        "SPECIFICATION": "POST (IntentSpecification)"
    }

    # Generate TMF921 mapping
    entry = {
        "id": generate_uuid(),
        "nl_intent": nl_intent,
        "nl_intent_normalized": nl_intent.lower().strip(),
        "tmf921_mapping": {
            "intent_type": intent_type,
            "action": tmf921_action_map.get(action, action),
            "expectation_type": random.choice(EXPECTATION_TYPES) if intent_type in ["Intent", "ProbeIntent"] else None,
            "endpoint": f"/intent" if intent_type in ["Intent", "ProbeIntent"] else f"/{intent_type.lower()}",
            "lifecycle_status": random.choice(LIFECYCLE_STATES),
            "reporting_events": random.sample(REPORTING_EVENTS, random.randint(1, 3)) if action == "REPORT" or random.random() > 0.7 else None
        },
        "tmf921_resource": {
            "id": template_vars["intent_id"],
            "name": template_vars["intent_name"],
            "description": nl_intent,
            "version": f"{random.randint(1, 5)}.{random.randint(0, 9)}",
            "priority": template_vars["priority"],
            "context": template_vars["context_domain"],
            "isBundle": random.choice([True, False]),
            "lifestyleStatus": random.choice(LIFECYCLE_STATES),
            "validFor": generate_valid_for(),
            "expression": generate_expression(),
            "characteristic": generate_characteristics(),
            "relatedParty": [generate_related_party()]
        },
        "intent_parameters": {
            "service_type": template_vars["service_type"],
            "quality_level": random.choice(SERVICE_QUALITIES),
            "latency": random.choice(LATENCY_VALUES),
            "throughput": random.choice(THROUGHPUT_VALUES),
            "availability": random.choice(AVAILABILITY_VALUES),
            "max_participants": random.choice(PARTICIPANT_COUNTS),
            "network_slice_id": random.choice(NSSI_IDS) if "slice" in template_vars["service_description"].lower() else None,
            "area_of_service": random.choice(AREAS),
            "reporting_interval": random.choice(REPORTING_INTERVALS),
            "app_types": random.sample(APP_TYPES, random.randint(1, 3))
        },
        "metadata": {
            "generated_at": datetime.now().isoformat() + "Z",
            "tmf921_version": "5.0.0",
            "intent_model_version": "v3.4.0"
        }
    }

    return entry


def generate_dataset(num_entries=1000):
    """Generate the complete dataset"""
    dataset = []

    # Distribution of intent types and actions
    intent_actions = [
        ("Intent", "CREATE"),
        ("Intent", "QUERY"),
        ("Intent", "UPDATE"),
        ("Intent", "DELETE"),
        ("Intent", "REPORT"),
        ("ProbeIntent", "PROBE"),
        ("ProbeIntent", "QUERY"),
        ("ProbeIntent", "REPORT"),
        ("IntentSpecification", "CREATE"),
        ("IntentSpecification", "QUERY"),
        ("IntentSpecification", "UPDATE"),
        ("IntentSpecification", "DELETE"),
        ("IntentReport", "QUERY"),
        ("IntentReport", "REPORT")
    ]

    # Generate entries with balanced distribution
    entries_per_combination = num_entries // len(intent_actions)

    for intent_type, action in intent_actions:
        for _ in range(entries_per_combination):
            entry = generate_nl_intent_entry(intent_type, action, action)
            dataset.append(entry)

    # Fill remaining entries
    while len(dataset) < num_entries:
        intent_type, action = random.choice(intent_actions)
        entry = generate_nl_intent_entry(intent_type, action, action)
        dataset.append(entry)

    # Shuffle the dataset for variety
    random.shuffle(dataset)

    # Add index to each entry
    for i, entry in enumerate(dataset):
        entry["index"] = i + 1

    return dataset


def save_dataset(dataset, filename="tmf921_nl_intent_dataset.json"):
    """Save dataset to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Dataset saved to {filename}")
    print(f"Total entries: {len(dataset)}")


def save_csv(dataset, filename="tmf921_nl_intent_dataset.csv"):
    """Save dataset to CSV for easier viewing"""
    import csv

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        # Flatten the structure for CSV
        fieldnames = [
            'index', 'nl_intent', 'nl_intent_normalized',
            'intent_type', 'action', 'expectation_type',
            'endpoint', 'lifecycle_status', 'resource_id',
            'resource_name', 'resource_version', 'priority',
            'context', 'is_bundle', 'service_type',
            'quality_level', 'latency', 'throughput',
            'availability', 'max_participants', 'reporting_interval'
        ]

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for entry in dataset:
            mapping = entry['tmf921_mapping']
            resource = entry['tmf921_resource']
            params = entry['intent_parameters']

            row = {
                'index': entry['index'],
                'nl_intent': entry['nl_intent'],
                'nl_intent_normalized': entry['nl_intent_normalized'],
                'intent_type': mapping['intent_type'],
                'action': mapping['action'],
                'expectation_type': mapping['expectation_type'],
                'endpoint': mapping['endpoint'],
                'lifecycle_status': mapping['lifecycle_status'],
                'resource_id': resource['id'],
                'resource_name': resource['name'],
                'resource_version': resource['version'],
                'priority': resource['priority'],
                'context': resource['context'],
                'is_bundle': resource['isBundle'],
                'service_type': params['service_type'],
                'quality_level': params['quality_level'],
                'latency': params['latency'],
                'throughput': params['throughput'],
                'availability': params['availability'],
                'max_participants': params['max_participants'],
                'reporting_interval': params['reporting_interval']
            }
            writer.writerow(row)

    print(f"CSV dataset saved to {filename}")


def generate_statistics(dataset):
    """Generate statistics about the dataset"""
    stats = {
        "total_entries": len(dataset),
        "by_intent_type": {},
        "by_action": {},
        "by_lifecycle_status": {},
        "by_service_type": {},
        "by_priority": {},
        "by_context": {}
    }

    for entry in dataset:
        mapping = entry['tmf921_mapping']
        resource = entry['tmf921_resource']
        params = entry['intent_parameters']

        # Count by intent type
        intent_type = mapping['intent_type']
        stats["by_intent_type"][intent_type] = stats["by_intent_type"].get(intent_type, 0) + 1

        # Count by action
        action = mapping['action']
        stats["by_action"][action] = stats["by_action"].get(action, 0) + 1

        # Count by lifecycle status
        status = mapping['lifecycle_status']
        stats["by_lifecycle_status"][status] = stats["by_lifecycle_status"].get(status, 0) + 1

        # Count by service type
        service_type = params['service_type']
        stats["by_service_type"][service_type] = stats["by_service_type"].get(service_type, 0) + 1

        # Count by priority
        priority = resource['priority']
        stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1

        # Count by context
        context = resource['context']
        stats["by_context"][context] = stats["by_context"].get(context, 0) + 1

    return stats


def main():
    """Main function to generate the dataset"""
    print("=" * 60)
    print("TMF921 Intent Management - NL Intent Dataset Generator")
    print("=" * 60)
    print()

    # Set seed for reproducibility
    random.seed(42)

    print("Generating 1000 NL Intent entries mapped to TMF921...")
    dataset = generate_dataset(1000)

    print(f"Generated {len(dataset)} entries")
    print()

    # Generate and display statistics
    stats = generate_statistics(dataset)
    print("Dataset Statistics:")
    print("-" * 40)
    print(f"Total Entries: {stats['total_entries']}")
    print()
    print("By Intent Type:")
    for intent_type, count in sorted(stats['by_intent_type'].items()):
        print(f"  {intent_type}: {count}")
    print()
    print("By Action:")
    for action, count in sorted(stats['by_action'].items()):
        print(f"  {action}: {count}")
    print()
    print("By Lifecycle Status:")
    for status, count in sorted(stats['by_lifecycle_status'].items()):
        print(f"  {status}: {count}")
    print()
    print("By Service Type:")
    for service_type, count in sorted(stats['by_service_type'].items()):
        print(f"  {service_type}: {count}")
    print()

    # Save datasets
    print("Saving datasets...")
    save_dataset(dataset)
    save_csv(dataset)

    # Save statistics
    with open("dataset_statistics.json", 'w') as f:
        json.dump(stats, f, indent=2)
    print("Statistics saved to dataset_statistics.json")

    print()
    print("=" * 60)
    print("Dataset generation complete!")
    print("=" * 60)

    # Show sample entries
    print()
    print("Sample Entries:")
    print("-" * 60)
    for i in range(min(5, len(dataset))):
        entry = dataset[i]
        print(f"\n[{i+1}] NL Intent: {entry['nl_intent']}")
        print(f"    TMF921 Type: {entry['tmf921_mapping']['intent_type']}")
        print(f"    Action: {entry['tmf921_mapping']['action']}")
        print(f"    Status: {entry['tmf921_mapping']['lifecycle_status']}")


if __name__ == "__main__":
    main()
