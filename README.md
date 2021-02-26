[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/uwidcit/info2602a2) 

[![Run in Postman](https://run.pstmn.io/button.svg)](https://documenter.getpostman.com/view/583570/SzRuZCp8?version=latest)

# Running
When opened in gitpod the server should be running already if it isn't
you can start it with the following command;

```bash
npm run start
```

# Testing
1. Update environment.json with your server's url

```json
{
	"id": "af99e18d-e0b6-47aa-b586-2cec222c581a",
	"name": "A2 Gitpod",
	"values": [
		{
			"key": "host",
			"value": "[your server url]",
			"enabled": true
		}
	],
	"_postman_variable_scope": "environment",
	"_postman_exported_at": "2021-02-25T23:09:00.839Z",
	"_postman_exported_using": "Postman/8.0.6"
}
```

2. Execute the following command to test Pokelisting page

```
npm run app-test
```

3. Execute the following comand to test the api

```
npm run api-test
```
