<?php

#The sensor will tell us its ID, the type of value it wants recorded, the value and its units
$sensorid = $_GET['sensorid'];
$valuetype = $_GET['valuetype'];
$value = $_GET['value'];
$units = $_GET['units'];
echo "<h1>$sensorid says: $valuetype is $value$units</h1>";

#make the connection to the database
include 'db_conn.php';

$sql = "INSERT INTO `generic_sensor_data` (`sensor_id`, `value_type`, `value`, `units`) VALUES ('$sensorid', '$valuetype', $value, '$units')";

$result = $conn->query($sql);

if(!result){
	die('Invalid query: ' . mysql_error());
}
$conn->close();

?>
 