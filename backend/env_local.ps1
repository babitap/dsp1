$Env:DJANGO_DEBUG = 'True'
$Env:DJANGO_ALLOWED_HOST = 'localhost'
$Env:B2C_TENANT_NAME = 'findexdatascience'
$Env:B2C_POLICY_NAME = 'B2C_1_signup_findex_datascience'
$Env:B2C_APP_ID = '763e9334-9fdc-489b-824d-f58bedaa22f2'
$Env:B2C_REPLY_URL = 'http://localhost:8080'

$Env:PBI_AUTHENTICATION_MODE = 'ServicePrincipal'
$Env:PBI_CLIENT_ID = '85fc0dc8-72f7-41a7-b55b-5c8a34439b5d'
$Env:PBI_CLIENT_SECRET = 'Cu98Q~uY9XLd~IY1VjziRy86sW548nx4Oq0wxago'
$Env:PBI_TENANT_ID = 'b48a9eab-75aa-4a5b-9fd7-f39223245c1a'

$Env:PBI_EXPORT_TO_FILE_HTTP_ENDPOINT = "https://prod-14.australiaeast.logic.azure.com:443/workflows/10fd65b9c078405abb094d8abba25570/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=mFS0l4Ff4pRc1Nf9JYsKppFttbvgFd3c1NM5ztZ-95o"
$Env:PBI_EXPORT_TO_FILE_WITH_RLS_HTTP_ENDPOINT = "https://prod-23.australiaeast.logic.azure.com:443/workflows/d1f05b6c178b420f8ea3bdcc156f5b1e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=i9Tq6k5DcIadgLRU-RtsseDt0YLoq7Wem_rs0w3hQJE"
$Env:PBI_EXPORT_TO_ZIP_WITH_RLS_HTTP_ENDPOINT = 'https://prod-26.australiaeast.logic.azure.com:443/workflows/bc9599b63a114ab69a2383c19187e54b/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=qr7gfqACi59zBKzV5qSipfltWE4lpzIwsogosO_uKhE'
$Env:PBI_EXPORT_TO_FILE_HTTP_APIKEY = "TYyZC1iZjg4LTQ2NWUtOGU1Zi04ZWFjN2I1OTgwNDVjUnJWWWZKY1g"

$Env:PBI_AUTHORITY_URL = 'https://login.microsoftonline.com/'
$Env:PBI_SCOPE = 'https://analysis.windows.net/powerbi/api/.default'

$Env:PBI_EXPORT_TO_FILE_HTTP_ENDPOINT = "https://prod-05.australiaeast.logic.azure.com:443/workflows/2c4e1afe3f0245fb82a713c4382f8207/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=1SGSK3Wsrobr7-i0INzKpm6ZxuGRJ9Mlq2k8XW9idXM"
$Env:PBI_EXPORT_TO_FILE_WITH_RLS_HTTP_ENDPOINT = "https://prod-10.australiaeast.logic.azure.com:443/workflows/ff5738c4807649ff93ce13719aa6fb9a/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=loEGCoPbdktqPpy585w3VesS1RlZin-zwZ2g0427k3k"
$Env:PBI_EXPORT_TO_ZIP_WITH_RLS_HTTP_ENDPOINT = 'https://prod-23.australiaeast.logic.azure.com:443/workflows/780b6c71d93b4672823254c09821ce80/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=88WoY05tURO50NpVUjE9av50MzWYn2o6OvYGdeMNSHs'

$Env:PBI_EXPORT_TO_FILE_HTTP_APIKEY = "TYyZC1iZjg4LTQ2NWUtOGU1Zi04ZWFjN2I1OTgwNDVjUnJWWWZKY1g"

$Env:DEFAULT_DBENGINE = "mssql"
$Env:DEFAULT_DBHOST = "sql01-datascience-dev-sqldb.database.windows.net"
$Env:DEFAULT_DBUSER = "DSAccessWrite"
$Env:DEFAULT_DBNAME = "access_level"
$Env:DEFAULT_DBPASS = "D6QRh%gdJX3Zd4&r!kVx"
$Env:DEFAULT_DBPORT = "1433"
$Env:DEFAULT_DRIVER = "SQL Server Native Client 11.0"

$Env:EXTERNAL_DBENGINE = "mssql"
$Env:EXTERNAL_DBHOST = "sql01-datascience-dev-sqldb.database.windows.net"
$Env:EXTERNAL_DBUSER = "DSPublicRead"
$Env:EXTERNAL_DBNAME = "public_data"
$Env:EXTERNAL_DBPASS = "RKmWLCwrBi&W*aLIt*uK"
$Env:EXTERNAL_DBPORT = "1433"
$Env:EXTERNAL_DRIVER = "SQL Server Native Client 11.0"

$Env:STUDENT_DBENGINE = "mssql"
$Env:STUDENT_DBHOST = "sql01-datascience-dev-sqldb.database.windows.net"
$Env:STUDENT_DBUSER = "DSStudentRead"
$Env:STUDENT_DBNAME = "student_profile"
$Env:STUDENT_DBPASS = "ZSnLG0FV%iUoW0k3O7hY"
$Env:STUDENT_DBPORT = "1433"
$Env:STUDENT_DRIVER = "SQL Server Native Client 11.0"

$Env:PRESENT_DBENGINE = "mssql"
$Env:PRESENT_DBHOST = "sql01-datascience-dev-sqldb.database.windows.net"
$Env:PRESENT_DBUSER = "DSPresentPowerBIRead"
$Env:PRESENT_DBNAME = "present"
$Env:PRESENT_DBPASS = "DEVmWLPwrBi&W*aPIt*uK"
$Env:PRESENT_DBPORT = "1433"
$Env:PRESENT_DRIVER = "SQL Server Native Client 11.0"

$Env:DOWNLOAD_ENVIRONMENT = "local"
$Env:DOWNLOAD_STORAGE_ACCOUNT = "batchdatasciencedev"
$Env:DOWNLOAD_STORAGE_KEY = "G6VcEwo2mFVPhBNIE0domk6Kwm5KyTW496t+dTLawwZYHVrflvegNI3TFL9u14OpBVUkJ6TBAf7yWMEW+KMC/g=="
$Env:DOWNLOAD_LOG_TABLE = "batchtaskslogsdev"
$Env:INVITE_USERMAIL_TABLE = "usermailtabledev"
$Env:DOWNLOAD_CONTAINER_NAME = "batchtasksoutput"
$Env:STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=batchdatasciencedev;AccountKey=G6VcEwo2mFVPhBNIE0domk6Kwm5KyTW496t+dTLawwZYHVrflvegNI3TFL9u14OpBVUkJ6TBAf7yWMEW+KMC/g==;EndpointSuffix=core.windows.net"


$Env:SECRET_KEY = "^sj6_uyj%3#hzh*vc09+es=jb(^$%)*wh)qq=32#-$kgg_*v$u"
