var prefs = {};
var pedometer_state = 0;
prefs['email'] = "ozkolonur@gmail.com";
prefs['device_id'] = "fffffffe-a0e0-17d4-4349-5aae2fce6653";
prefs['gender'] = "male";
prefs['age'] = "28";
prefs['height'] = "178";
prefs['weight'] = "80";
prefs['login_type'] = "email";
prefs['manufacturer'] = "HUAWEI";
prefs['model'] = "Turkcell T20";
prefs['product'] = "U8650-1";
prefs['swversion'] = "2.0";
prefs['username'] = "ozkolonur";
prefs['lifestyle'] = "1";
prefs['password'] = "123123";
prefs['sensivity'] = "40";
prefs['default_sensivity'] = "30";
prefs['mode'] = "auto";
prefs['platform'] = "sim";
prefs['signup_emails'] = "ozkolonur@gmail.com;ozkolonur@hotmail.com;onuro@airties.com";
prefs['first_use'] = "yes";
prefs['wizard_completed'] = "no";
prefs['rating_completed'] = "no";
prefs['swversion'] = "1.1.0";
prefs['app_state'] = "running";
prefs['pedometer_state'] = "started";
prefs['software_update'] = "advised";
prefs['config_changed'] = "yes";
prefs['token'] = "43475f7219c43a56c3b3288dbb2a720e";

var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-33463369-1']);
_gaq.push(['_setCustomVar', 1, 'platform', prefs['platform'],1]);
_gaq.push(['_setCustomVar', 2, 'swversion', prefs['swversion'],1]);
_gaq.push(['_setCustomVar', 3, 'firstuse', 'yes',1]);
//_gaq.push(['_trackPageview']);

(function() {
  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();

function test_callback(resp){
    logit("test_callback:" + resp);
}


function sim_sync(){
    logit("sim_sync:");
    $.ajax({
        url: server_addr + "/mobsync/config/",
        type: "post",
        data: prefs,
        // callback handler that will be called on success
        success: function(response, textStatus, jqXHR){
            // log a message to the console
            logit("SYNC Complete!");
			logit(response);
            update_vars = response['update'];
			for (var key in update_vars) {
			  if (update_vars.hasOwnProperty(key)) {
                 logit("UPDATE "+key+"="+update_vars[key]);
                 prefs[key] = update_vars[key]
			  }
			}
            //logit(update_vars);
        },
        // callback handler that will be called on error
        error: function(jqXHR, textStatus, errorThrown){
            // log the error to the console
            logit(
                "The following error occured: "+
                textStatus, errorThrown
            );
        },
        // callback handler that will be called on completion
        // which means, either on success or error
        complete: function(){
            // enable the inputs
            logit("AJAX Complete");
        }
    });
}


function sim_app_request(callback, operation, param1, param2){
    if (operation == 'get')
    {
        result = prefs[param1];
	}
	else if (operation == 'set'){
		//For some variables like sensivity extra operation might need
		prefs[param1] = param2;
        result = param2;
	}
	else if (operation == 'pedometer_start'){
		pedometer_state = 1;
        result = "OK";
	}
	else if (operation == 'set_app_state'){
		logit("redirecting");
		window.location = "/mobindex/index.html";
		pedometer_state = 1;
        result = "OK";
	}
	else if (operation == 'pedometer_stop'){
		pedometer_state = 0;
        result = "OK";
	}
	else if (operation == 'hide_splash'){
        result = "OK";
	}
	else if (operation == 'step_update'){
		step_update(100, 200);
		pedometer_state = 0;
        result = "OK";
	}
	else if (operation == 'pedometer_reset'){
        result = "OK";
	}
	else if (operation == 'sync'){
        sim_sync();
	}
	else if (operation == 'load_activity_data'){
        result = "OK";
        addActivityData('st30082012','[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,24,1,0,12,153,213,343,284,198,0,0,0,0,0,0,3,0,0,0,279,33,0,21,18,24,10,0,0,124,54,4,1,4,85,2,1,2,3,0,2,3,2,1,0,1,2,0,9,17,1,9,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]');
        addActivityData('st02092012','[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,25,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]');
	}
	else if (operation == 'trackpage'){
		_gaq.push(['_trackPageview', param1]);
        result = "OK";
	}
	else if (operation == 'trackevent'){
		_gaq.push(['_trackEvent', param1, param2]);
		result = "OK";
	}

    logit(operation+":"+param1+":"+param2+" result="+result);

    logit("callback_length:"+callback.length);
    if (callback.length > 0){
        window[callback](result);
    }
    return;
}

