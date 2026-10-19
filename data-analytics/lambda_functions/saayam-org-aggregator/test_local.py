# test_local.py

from lambda_function import lambda_handler

if __name__ == "__main__":
    event = {
        "request_id": 1,      # will use mock req_loc
        "beneficiary_id": 123,  # will use mock profile address if needed
        "sort_by": "distance",
    }

    result = lambda_handler(event, None)

    for org in result["organizations"]:
        print(
            org["Name"],
            "| distance:", org["distance"],
            org["distance_unit"],
            "| status:", org["distance_status"],
        )
