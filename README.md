# Remitly Assignment - SWIFT code API
This application was created in Python using Flask and MongoDB.

# Prerequisites
The following dependencies are needed for this project to run:
 - MongoDB community server ([download here](https://www.mongodb.com/try/download/community))
 - Flask, PyMongo and other python packages, specified in requirements.txt

# Installation
1. Clone this repository
2. Run MongoDB Comunity Server ```sudo systemctl start mongod```
3. Run app.py file ```python3 app.py ```
4. Execute requests, as shown in section below.





# Endpoint examples
### Endpoint 1: Retrieve information about provided SWIFT code
```
curl http://localhost:8080/v1/swift-codes/AFAAUYM1XXX
```

### Endpoint 2: Retrieve information about SWIFT codes by country
```
curl http://localhost:8080/v1/swift-codes/country/BG
```

### Endpoint 3: Add new SWIFT code
```
curl -X POST http://localhost:8080/v1/swift-codes -H "Content-Type: application/json" -d '{
 "address": "SampleAdress",
 "bankName": "SampleBankName",
 "countryISO2": "POLAND",
 "countryName": "PL",
 "isHeadquarter": true,
 "swiftCode": "ABCDEFGXXX"}'
```

### Endpoint 4: Delete selected SWIFT code
```
curl -X DELETE http://localhost:8080/v1/swift-codes/ABCDEFGXXX
```
