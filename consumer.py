import requests
from robocorp import workitems
from robocorp.tasks import task
import json

@task
def consume_traffic_data():
    """
    Inhuman Insurance, Inc. Artificial Intelligence System robot.
    Consumes traffic data work items.
    """
    process_traffic_data()

def process_traffic_data():
    # Load JSON data as file
    with open(r'output\work-items-out\workitems.json', 'r') as file:
        workitems_data = json.load(file)

    # Iterate over work items
    for item in enumerate(workitems_data):
        if 'payload' in item:
            traffic_data = item.payload["traffic_data"]
            if len(traffic_data["country"]) == 3:
                status, return_json = post_traffic_data_to_sales_system(traffic_data)
                if status == 200:
                    item.done()
                else:
                    item.fail(
                        exception_type="APPLICATION",
                        code = "TRAFFIC_DATA_POST_FAILED",
                        message = return_json["message"],
                    )
            else:
                item.fail(
                    exception_type = "BUSINESS",
                    code = "INVALID_TRAFFIC_DATA",
                    message = item.payload,
                )


def post_traffic_data_to_sales_system(traffic_data):
    url = "https://robocorp.com/inhuman-insurance-inc/sales-system-api"
    response = requests.post(url, json=traffic_data)
    # response.raise_for_status
    return response.status_code, response.json()