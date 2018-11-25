<?php
// Connecting, selecting database

function hello(){
	echo "Hello World!";
}

function get_transaction($txnid){
	return $txnid;
}

function get_public_key($identifier){
	return $identifier;
}

function decrypt($enc, $key){
	$dec = $enc;
	return $dec;
}


$client = MultichainClient("http://<chainurl>:8000", 'multichainrpc', '79pgKQusiH3VDVpyzsM6e3kRz6gWNctAwgJvymG3iiuz', 3);
$address = $client->setDebug(true)->getNewAddress();


$dbconn = pg_connect("host=localhost port=5100 dbname=postgres")
    or die('Could not connect: ' . pg_last_error());

// Performing SQL query
$query = 'SELECT * FROM dummy';
$result = pg_query($query) or die('Query failed: ' . pg_last_error());


while($line = pg_fetch_array($result, null, PGSQL_NUM)) {
	$tobehashed =  $line[0].$line[1].$line[2].$line[3];
	$hash_db = hash('sha256', $tobehashed);
	echo $hash_db."\n";
	$txnid = $line[4]; 
	$identifier = $line[5];

	$encrypted_hash = get_transaction($txnid);
	echo $encrypted_hash."\n";
	$key = get_public_key($identifier);

	$hash_bc = decrypt($encrypted_hash, $key);

	if ($hash_db != $hash_bc) {
		//echo "Error!";
		exit("Error!");
	}
}


// Printing results in HTML
// echo "<table>\n";
// while ($line = pg_fetch_array($result, null, PGSQL_ASSOC)) {
//     echo "\t<tr>\n";
//     foreach ($line as $col_value) {
//         echo "\t\t<td>$col_value</td>\n";
//     }
//     echo "\t</tr>\n";
// }
// echo "</table>\n";

// Free resultset
//pg_free_result($result);

// Closing connection
pg_free_result($result);
pg_close($dbconn);
hello();
//echo hash('sha256', 'The quick brown fox jumped over the lazy dog.');
?>