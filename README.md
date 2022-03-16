# Archive projects API
### REST API built using Pyhton, Flask and MySQL
###### not public published (works in localhost) <br />


## Features
- Get all projects in database
- create new project and insert in database
- retreive a project by id


## available requests examples
 **1. input : project as json object
     output: view object**
     
> '^/archives/create/' -->  **[POST]**
```sh
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
```

 **2. input : none
     output: retrieve all projects**

> '^/archives/replicate/'     --> **[GET]**
> this is how output will look like as json object

```sh
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
	  }
```
