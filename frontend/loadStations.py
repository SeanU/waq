# Load station data

import pandas as pd
import mysqli

fileLoc = '/data/waq/exploration/station.csv'

df = pd.DataFrame.from_csv(fileLoc)

$servername = "localhost";
$username = "webuser";
$password = "JZdZ82hh7W2cyUrJ";
$dbname = "capstone";

# Create connection

$conn = new mysqli($servername, $username, $password, $dbname);

# Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

# $sql = "SELECT id, firstName, lastName, badgeName, email, student, speaker FROM registration WHERE id=$lastId";
# //echo $sql;
# $result = $conn->query($sql);>



pd.DataFrame.to_sql(df, conn, flavor='mysql', schema=capstone, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)¶
df.to_sql()






