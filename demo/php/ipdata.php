<?php
header("Content-type: text/html; charset=utf-8");

class ipdata{

	var $ipdatafile = './tinyipdata.dat';
	
	function setipdatafile($path){
		$this->ipdatafile = $path;
	}
	
	function convertip($ip) {
		$return = '';
		static $fp = NULL, $offset = array(), $index = NULL;
	
		if(preg_match("/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/", $ip)) {
	
			$ipdot = explode('.', $ip);
	
			if($ipdot[0] == 10 || $ipdot[0] == 127 || ($ipdot[0] == 192 && $ipdot[1] == 168) || ($ipdot[0] == 172 && ($ipdot[1] >= 16 && $ipdot[1] <= 31))) {
				$return = '- LAN';
			} elseif($ipdot[0] > 255 || $ipdot[1] > 255 || $ipdot[2] > 255 || $ipdot[3] > 255) {
				$return = '- Invalid IP Address';
			} else {
				$ip = pack('N', ip2long($ip));
				$ipdot[0] = (int)$ipdot[0];
				$ipdot[1] = (int)$ipdot[1];
			
				if($fp === NULL && $fp = @fopen($this->ipdatafile, 'rb')) {
					$offset = @unpack('Nlen', @fread($fp, 4));
					$index  = @fread($fp, $offset['len'] - 4);
				} elseif($fp == FALSE) {
					return  '- Invalid IP data file';
				}
			
				$length = $offset['len'] - 1028;
				$start  = @unpack('Vlen', $index[$ipdot[0] * 4] . $index[$ipdot[0] * 4 + 1] . $index[$ipdot[0] * 4 + 2] . $index[$ipdot[0] * 4 + 3]);
					
				for ($start = $start['len'] * 8 + 1024; $start < $length; $start += 8) {
					if ($index{$start} . $index{$start + 1} . $index{$start + 2} . $index{$start + 3} >= $ip) {
						$index_offset = @unpack('Vlen', $index{$start + 4} . $index{$start + 5} . $index{$start + 6} . "\x0");
						$index_length = @unpack('Clen', $index{$start + 7});
						break;
					}
				}
			
				@fseek($fp, $offset['len'] + $index_offset['len'] - 1024);
				if($index_length['len']) {
					return '- '.@fread($fp, $index_length['len']);
				} else {
					return '- Unknown';
				}
			}
		}
		return $return;
	}
	
}

$file = substr(dirname(__FILE__), 0, -8)."tinyipdata.dat";
$ip = '56.10.0.0';
$ipdata = new ipdata();
$ipdata->setipdatafile($file);
printf("<p>ip : %s , area: %s </p>", $ip, $ipdata->convertip($ip));
?>