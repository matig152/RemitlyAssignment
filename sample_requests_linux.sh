# ENDPOINT 1: 
echo "*** ENDPOINT 1: Retrieve information about provided swift code. ***"
curl http://localhost:8080/v1/swift-codes/AFAAUYM1XXX


# ENDPOINT 2:
echo "*** ENDPOINT 2: Retrieve information about swift codes by country ***"
curl http://localhost:8080/v1/swift-codes/country/BG

# ENDPOINT 3:
echo "*** ENDPOINT 3: Add new swift code"
echo 'Adding Swift Code: { "address": "SampleAdress","bankName": "SampleBankName","countryISO2": "POLAND","countryName": "PL","isHeadquarter": true,"swiftCode": "ABCDEFGXXX"}'
curl -X POST http://localhost:8080/v1/swift-codes -H "Content-Type: application/json" -d '{ "address": "SampleAdress","bankName": "SampleBankName","countryISO2": "POLAND","countryName": "PL","isHeadquarter": true,"swiftCode": "ABCDEFGXXX"}'


# ENDPOINT 4
echo "*** ENDPOINT 4: Delete selected swift code":
echo "Deleting SWIFT code: ABCDEFGXXX"
curl -X DELETE http://localhost:8080/v1/swift-codes/ABCDEFGXXX
