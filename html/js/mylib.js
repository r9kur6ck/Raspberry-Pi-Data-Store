/*
データサーバAPIを呼び出すスクリプト
*/

/*
チャネル操作
*/

function get_channel_list(cb) {
    let req = new XMLHttpRequest();
    req.onreadystatechange = function(){
	if (this.readyState == 4 && this.status == 200) {
	    let ml = JSON.parse(this.response, 'utf8');
	    cb(ml.channel);
	}
    }
    req.open('GET', '/channel/');
    req.send();
}

function add_channel(channel_id, channel_name, channel_owner, cb) {
    let req = new XMLHttpRequest();
    req.onreadystatechange = function(){
	if (this.readyState == 4 && this.status == 200) {
	    let ml = JSON.parse(this.response, 'utf8');
	    cb(ml);
	}
    }
    let channel = {"id":channel_id, "name":channel_name, "owner":channel_owner};
    let json = JSON.stringify(channel);
    req.open('POST', '/channel');
    req.setRequestHeader('Content-Type', 'application/json');
    req.send(json);
    
}

function delete_channel(channel_id, cb) {
    let req = new XMLHttpRequest();
    req.onreadystatechange = function(){
	if (this.readyState == 4 && this.status == 200) {
	    let ml = JSON.parse(this.response, 'utf8');
	    cb(ml);
	}
    }
    req.open('DELETE', '/channel/' + channel_id);
    req.send();
    
}


/*
データ操作
*/
function get_influxdb_data(channel_id, measurement, from, to, cb) {
    let req = new XMLHttpRequest();
    req.onreadystatechange = function(){
	if (this.readyState == 4 && this.status == 200) {
	    let ml = JSON.parse(this.response, 'utf8');
	    cb(ml.data);
	}
    }
    /*
      検索条件設定
    */
    let param = "";
    if (measurement) {
	param = '&measurement='+measurement;
    }
    let url = '/data/?channel_id=' + channel_id + param
    req.open('GET', url);
    req.send();
}



