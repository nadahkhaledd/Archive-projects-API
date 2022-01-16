to send json input you should use this template:

{
  "id": 1,
  "name": "projectY",
  "departmentID": 1,
  "department": {
    "id": 1,
    "name": "departmentY",
    "assetID": 1,
    "asset": {
		"id": 1,
		"name": "assetX"
    }
  }
}


and response to get all records is shown like below:

{
    "department": {
      "asset": {
        "id": 1,
        "name": "assetX"
      },
      "id": 1,
      "name": "departmentX"
    },
    "id": 1,
    "name": "projectX"
  },