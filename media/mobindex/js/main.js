//asla vazgecme
var cfg_nickname;
var cfg_email;
var cfg_gender;
var cfg_age;
var cfg_height;
var cfg_weight;
var cfg_lifestyle;
var cfg_mode;
var cfg_sensivity;
var cfg_default_sensivity;
var cfg_device_id;
var cfg_password;
var cfg_platform;
var cfg_swversion;
var cfg_app_state;
var cfg_pedometer_state;
var diets = null;
var ranks = null;
var venues = null; 
var diets_updated = null;
var venues_updated = null;
var ranks_updated = null;
var start_button_state = 0;
var currentUrl = null;
var settingsInputChangedTimer = null;
var cfg_first_use = null;
var cfg_wizard_completed = null;
var cfg_rating_completed = null;
var cfg_config_changed = null;
var cfg_software_update = "uptodate";
var server_addr = "http://www.adimsayar.com"
var activity_data = [];
var logging_enabled = false;
var cfg_signup_emails = null;

var suggestions = ["Beyaz ekmekten kaçının. Çavdar ekmeği veya tam buğday ekmeği tüketin.",
"Mutlaka günde 2.5 litre su için.",
"Günde 10 bin adım atmayı alışkanlık haline getirin.",
"Akşam 6 dan sonra yemek yemeyin. 1 saat sonra meyve tüketebilirsiniz.",
"Akşam yemeklerinizi hafif tutun.",
"Kahvaltı yapmayı ihmal etmeyin. Her gün aynı saatte yapmaya özen gösterin.",
"Kesinlikle ögün atlamayın. Ara öğünleri ihmal etmeyin.",
"Yatmadan önce bir kase yağsız yoğurt yiyin. Böylece sindirim sisteminiz güçlenir.",
"Hazır yiyecek ve içeceklerden uzak durun.",
"Sabah kahvaltısında iki dilim ekmek yiyin. Metabolizmanız hızlanır.",
"Kahvaltı-öğle yemeği arasıda ara öğün yapın. Ara öğünlerde kuru-taze meyve tüketin.",
"Taze meyve ve sebzelerden uzak durmayın. ",
"Beyaz et tüketmeğe özen gösterin. Haftada bir kez balık tüketin",
"Acıktığınızda domates, salatalık gibi su oranı yüksek besinlerden faydalanın.",
"Yemegi hızlı yemeyin. Lokmalarınızı küçültün ve çok çiğneyin.",
"Bol bol egzersiz yapın, egzersizleri çeşitlendirin.",
"Başka şeylerle oyalanarak (televizyon, sohbet, kitap vb.) yemek yemeyin.",
"Bırakın yemekler arkanızdan ağlasın. Hepsini bitirmek zorunda değilsiniz.",
"Karnınız tok iken tatlı yemeyin.",
"Şekerden uzak durun. İçeceklerinizi şekersiz tüketmeye alışın.",
"Zeytinyağı sağlık kaynağıdır, tercih edin. Katı yağlardan uzak durun.",
"Az yağlı peynirleri tercih edin.",
"Şeker oranı yüksek meyvelerden fazla tüketmeyin. (Şeftali, Üzüm vb.)",
"Yemeklerde beyaz eti daha çok kullanın.",
"Kırmızı et yiyecekseniz yağsız ve ızgara olmasına dikkat edin.",
"Bol sebze, bakliyat ve lifli gıdalar tüketin.",
"Ağır şerbetli tatlılardan kaçının.",
"Her zaman yürümeyi tercih edin. Yürüyüş en faydalı spordur.",
"Her türlü yağlı soslardan uzak durun. (Mayonez vb.)",
"Büyük tabaklarda, küçük porsiyonlarla yiyin.",
"Bol bol sebze tüketin."];

function logit(msg){
    if (logging_enabled)
        console.log(msg);
}

(function($) {
    /*
     * Changes the displayed text for a jquery mobile button.
     * Encapsulates the idiosyncracies of how jquery re-arranges the DOM
     * to display a button for either an <a> link or <input type="button">
     */
    $.fn.changeButtonText = function(newText) {
        return this.each(function() {
            $this = $(this);
            if( $this.is('a') ) {
                $('span.ui-btn-text',$this).text(newText);
                return;
            }
            if( $this.is('input') ) {
                $this.val(newText);
                // go up the tree
                var ctx = $this.closest('.ui-btn');
                $('span.ui-btn-text',ctx).text(newText);
                return;
            }
        });
    };
})(jQuery);

function isValidEmailAddress(emailAddress) {
    var pattern = new RegExp(/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i);
    return pattern.test(emailAddress);
};


function getDailyAverageSteps(){
    total_steps = 0;
    day_count = 0;
    tmp_date = new Date();
    if (activity_data.length > 1)
    {
        for(i=0;i<activity_data.length;i++){
            if ((activity_data[i].date.getDate() == tmp_date.getDate())
                  && (activity_data[i].date.getMonth() == tmp_date.getMonth())
                    && (activity_data[i].date.getYear() == tmp_date.getYear()))
            {
                //logit("skip today");
                continue;
            }
            //logit("dat1="+activity_data[i].date.getDate());
            total_steps += activity_data[i].total_steps
            day_count++;
            //logit(day_count) 
        }
        return ''+parseInt(total_steps / day_count);
    }
    else
    {
        return '-';
    }
}

function addActivityData(key, value){
    function getStepList(steps_str){
        steps_list = steps_str.replace(/[\[\]']+/g,'').split(',');
        steps_list_int = [];
        for (i=0;i<steps_list.length;i++){
            steps_list_int[i] = parseInt(steps_list[i]);
        }
        return steps_list_int;
    }
    function getTotalStepsFromList(steps_list_int){
        steps_total = 0
        for (i=0;i<steps_list_int.length;i++){
            steps_total += steps_list[i];
        }
        return steps_total;
    }
   //currently only sm10032013 like variables will be sent from device
   //data format: key
   //stDDMMYYYY = 0,0,0,0,0... (288 units of steps for every 5min)
   tmp_day = Number(key.substring(2,4));
   tmp_month = Number(key.substring(4,6));
   tmp_year = Number(key.substring(6,10));
   logit("day="+tmp_day);
   logit("month="+tmp_month);
   logit("substring="+key.substring(4,6));
   logit("year="+tmp_year);
   tmp_date = new Date();
   tmp_date.setFullYear(tmp_year,tmp_month,tmp_day);
   logit(tmp_date);
   steps_list = getStepList(value);
   total_steps = getTotalStepsFromList(steps_list)
   activity_data.push({
    date:   tmp_date,
    steps: steps_list,
    total_steps: total_steps,
    activity: null
   });
   logit(activity_data.steps);
}




$(document).delegate('#login-button-forgotpass', 'click', function() {
  $(this).simpledialog({
    'mode' : 'string',
    'prompt' : 'Şifrenizin gönderileceği eposta adresini girin',
    'buttons' : {
      'Tamam': {
        click: btnForgotPassOnClick,
        icon: null
      },
      'Vazgeç': {
        click: function () { },
        icon: null,
        theme: "c"
      }
    }
  })
})

function btnForgotPassOnClick(){
    logit("btnForgotPassOnClick");
    $.mobile.loadingMessage ='Lutfen Bekleyiniz';
    $.mobile.loadingMessageTextVisible=true;
    $.mobile.showPageLoadingMsg();
    email_address = $('#login-button-forgotpass').attr('data-string');
    key = 33900+email_address.length
    logit(email_address);
    if( !isValidEmailAddress( email_address ) ){
        logit("email address is not valid");
        native_alert("email address is not valid");
        //$("#input-email").focus();
    }else {
        logit("email address is OK");
		$.ajax({
		    url: server_addr + "/profile/reset_password_email/",
		    type: "post",
		    data: {'email':email_address, 'key':key},
		    // callback handler that will be called on success
		    success: function(response, textStatus, jqXHR){
		        // log a message to the console
		        logit("Hooray, it worked!");
		        logit(response.status);
		        if (response.status.indexOf("OK") >= 0){
		            logit("reset password OK");
		            $.mobile.hidePageLoadingMsg();
                    native_alert("Sifreniz e-posta adresine gonderildi. Sifrenizi kullanarak giris yapabilirsiniz");
				} else if(response.status.indexOf("FAIL") >= 0){
		            logit("reset password FAIL");
		            $.mobile.hidePageLoadingMsg();
		            native_alert("Kullanici kaydi basarisiz, lutfen daha sonra tekrar deneyin");
		        }
		    },
		    // callback handler that will be called on error
		    error: function(jqXHR, textStatus, errorThrown){
		        // log the error to the console
		        logit(
		            "The following error occured: "+
		            textStatus, errorThrown
		        );
		        $.mobile.hidePageLoadingMsg();
		        native_alert("Sunucuya erisilemedi. Internet baglantinizi kontrol edin.");
		    },
		    // callback handler that will be called on completion
		    // which means, either on success or error
		    complete: function(){
		        // enable the inputs
		        logit("AJAX Complete");
		    }
		});
    }
}


function btnSettingsReset(){
    logit("btnSettingsReset()");
    app_request('set_cfg_mode','set','mode','auto');
    //app_request('set_cfg_default_sensivity','get','default_sensivity','');
    app_request('set_cfg_sensivity','set','sensivity',cfg_default_sensivity);
    $('#input-mode').val(cfg_mode);
    $('#input-mode').selectmenu('refresh', true);
    $('#input-sensivity').val(cfg_sensivity);
}

function btnLogOut(){
    //#show confirmation dialog
    logit("btnLogOut()");
    app_request('', 'pedometer_stop', '', '');
    //app_request('set_cfg_pedometer_state', 'set', 'pedometer_state', 'stopped');
    app_request('','trackevent', 'click', 'logout');
    app_request('', 'set_app_state', 'logged_out', '');
}

function btnSignUpFbOnClick(){
    logit("btnSignUpFbOnClick");
    $.mobile.loadingMessage ='Giris Yapiliyor, Lutfen Bekleyiniz';
    $.mobile.loadingMessageTextVisible=true;
    $.mobile.showPageLoadingMsg();
    app_request('','signup_facebook', '', '');
}

function rateApplication(){
    logit("rateApplication");
    app_request('','trackevent', 'click', 'rate_application');
    app_request('set_cfg_rating_completed', 'set', 'rating_completed', 'yes');
    setTimeout(updateView,500);
    app_request('','rate_application', '', '');
}

function updateSoftware(){
    logit("softwareUpdate");
    app_request('','trackevent', 'click', 'update_software');
    app_request('','software_update', '', '');
    setTimeout(updateView,500);
}


function native_alert(msg){
        $("#popupmsg").text(msg);
        $("#popup").popup();
        $("#popup").popup("open");
}


function logout_question(){
        //$("#questionmsg").text("question");
        $("#popupDialog2").popup();
        $("#popupDialog2").popup("open");
}

//question,option1_text, option1_callback, option2_text, option2_callback
function native_question(){
        //$("#questionmsg").text("question");
        $("#popupDialog").popup();
        $("#popupDialog").popup("open");
}

function say_facebook_fail(){
    $.mobile.hidePageLoadingMsg();
	native_alert("Facebook ile giriş yaparken bir hata oluştu. İnternet bağlantınızı kontrol edin, yada bir başka seçenekle giriş yapmayı deneyin.");
}


function btnSignUpEmailDirectOnClick(){
    logit("btnSignUpEmailDirectOnClick");
    tmp_email = $('#signup-select-email').val()
    if (!isValidEmailAddress(tmp_email)){
        native_alert("Gecersiz e-posta adresi");
    } else {
        app_request('set_cfg_email','set','email',tmp_email);
        app_request('', 'set_app_state', 'running', '');
	}
}

function btnSignUpEmailOnClick(){
    logit("btnSignUpEmailOnClick");
    email_address = $("#signup-input-email").val();
    key = 33900+email_address.length
    logit(email_address);
    if( !isValidEmailAddress( email_address ) ){
        logit("email address is not valid");
        native_alert("Gecersiz e-posta adresi");
        //$("#signup-input-email").focus();
    }else {
        $.mobile.loadingMessage ='Giris Yapiliyor, Lutfen Bekleyiniz';
        $.mobile.loadingMessageTextVisible=true;
        $.mobile.showPageLoadingMsg();
        logit("email address is OK");
		$.ajax({
		    url: server_addr + "/profile/register_email_user/",
		    type: "post",
		    data: {'email':email_address, 'key':key},
		    // callback handler that will be called on success
		    success: function(response, textStatus, jqXHR){
		        // log a message to the console
		        logit("Requesting new password...");
		        logit(response.status);
		        if (response.status.indexOf("OK") >= 0){
		            logit("registration OK");
		            $.mobile.hidePageLoadingMsg();
                    native_alert("Sifreniz e-posta adresine gonderildi. Sifrenizi kullanarak giris yapabilirsiniz");
				} else if(response.status.indexOf("FAIL") >= 0){
		            logit("authorization FAIL");
		            logit(response);
		            $.mobile.hidePageLoadingMsg();
		            native_alert("Kullanici kaydi basarisiz, lutfen daha sonra tekrar deneyin");
		        }
		    },
		    // callback handler that will be called on error
		    error: function(jqXHR, textStatus, errorThrown){
		        // log the error to the console
		        logit(
		            "The following error occured: "+
		            textStatus, errorThrown
		        );
		        $.mobile.hidePageLoadingMsg();
		        native_alert("Sunucuya erisilemedi. Internet baglantinizi kontrol edin.");
		    },
		    // callback handler that will be called on completion
		    // which means, either on success or error
		    complete: function(){
		        // enable the inputs
		        logit("AJAX Complete");
		        $.mobile.hidePageLoadingMsg();
		    }
		});
    }

    //app_request('','signup_email', '', '');
}

function btnLoginOnClick(){
    logit("btnLoginOnClick");
    email_address = $("#login-input-email").val();
    pass = $("#login-input-password").val();
    if( !isValidEmailAddress( email_address ) ){
        logit("email address is not valid");
        native_alert("email address is not valid");
        //$("#input-email").focus();
    }
    $.mobile.loadingMessage ='Giris Yapiliyor, Lutfen Bekleyiniz';
    $.mobile.loadingMessageTextVisible=true;
    $.mobile.showPageLoadingMsg();
    $.ajax({
        url: server_addr + "/profile/authorize_user/",
        type: "post",
        data: {'email':email_address, 'key':pass},
        // callback handler that will be called on success
        success: function(response, textStatus, jqXHR){
            // log a message to the console
            logit("Logging in...");
            logit(response.status);
            if (response.status.indexOf("OK") >= 0){
                logit("authorization OK");
                $.mobile.hidePageLoadingMsg();
                app_request('set_cfg_email', 'set', 'email', email_address);
                app_request('', 'set_app_state', 'running', '');
			} else if(response.status.indexOf("FAIL") >= 0){
                logit("authorization FAIL");
                $.mobile.hidePageLoadingMsg();
                native_alert("Yanlis kullanici adi veya sifre");
            }
        },
        // callback handler that will be called on error
        error: function(jqXHR, textStatus, errorThrown){
            // log the error to the console
            logit(
                "The following error occured: "+
                textStatus, errorThrown
            );
            $.mobile.hidePageLoadingMsg();
            native_alert("Sunucuya erisilemedi. Internet baglantinizi kontrol edin.");
        },
        // callback handler that will be called on completion
        // which means, either on success or error
        complete: function(){
            // enable the inputs
            $.mobile.hidePageLoadingMsg();
            logit("AJAX Complete");
        }
    });
}

function btnStartStopOnClick(){
    logit("btnStartStop2");
    if (start_button_state == 0)
    {
        start_button_state = 1;
        $("#btn-start-stop").changeButtonText("Stop");
        app_request('','trackevent', 'click', 'start_button');
        app_request('','pedometer_start', '', '');
        tmp = "<p>Adımsayar şu an çalışıyor, bu ekrandan günlük kaç adım attığınızı takip edebilirsiniz</p>"
        $("#suggestion-text").html(tmp);
        setTimeout(updateView,10000);
    }
    else if(start_button_state == 1)
    {
        start_button_state = 0;
        $("#btn-start-stop").changeButtonText("Start");
        app_request('','pedometer_stop', '', '');
        app_request('','trackevent', 'click', 'stop_button');
    }
    $("#btn-start-stop2 .ui-btn-text").text("");
}

function btnResetOnClick(){
    if ((cfg_weight == "227") && (cfg_height=="227")){
        logit("syncsync");
        app_request('', 'sync', '','');
    } else {
        app_request('', 'pedometer_reset', '','');
        app_request('','trackevent', 'click', 'reset_button');
    }
}


function step_update(curStep, totalStep){
    logit("curstep="+curStep+" totalStep="+totalStep);
    total_step_int = parseInt(totalStep);
    progress_change((total_step_int/10000)*100);
    if ((total_step_int >= 1) && (total_step_int < 20))
    {
        return;
    }
    if (total_step_int % 100 == 0){
       progress_change((total_step_int/10000)*100);
       if ((total_step_int >= 0) && (total_step_int <= 1000)){
           smile_change(1);
       }
       else if ((total_step_int > 1000) && (total_step_int <= 4000)) {
           smile_change(2);
       }
       else if ((total_step_int > 4000) && (total_step_int <= 7000)) {
           smile_change(3);
       }
       else if ((total_step_int > 7000) && (total_step_int <= 10000)) {
           smile_change(4);
       }
       else if (total_step_int > 10000) {
           smile_change(5);
       }
    }
    $("#step-text").text(curStep);
    $("#step-today").text(totalStep);
}

function app_request(callback, operation, param1, param2){
    userAgent = navigator.userAgent;
    if (userAgent.indexOf('Chrome') > 0)
	{
		sim_app_request(callback, operation, param1, param2);
	} else if(userAgent.indexOf('Android') > 0) {
        window.AndroidAPI.request(callback,operation, param1, param2);
    }
    else {
	    document.location = "app:" + operation + ":" + callback + ":" + param1 + ":" + param2;
    }
}

//config_init();
/*
function update_lists_data(){
    current_time = new Date();
    if ((ranks==null) || ((current_time - ranks_updated) > (3 * 60 * 1000 * 60))){
        ajax_load_ranking();
    }
    if ((venues==null) || ((current_time - venues_updated) > (5 * 1000 * 60))){
        //ajax_load_venues();
    }
    if ((diets==null) || ((current_time - diets_updated) > (3* 60 * 1000 * 60))){
        //ajax_load_diets();
    }
}
$(document).bind("mobileinit", function()
{
    logit("-------mobile-init");
    if (navigator.userAgent.indexOf("Android") != -1)
    {
        $.mobile.defaultPageTransition = 'none';
        $.mobile.defaultDialogTransition = 'none';
    }
});
$(document).bind("mobileinit", function(){
      $.mobile.defaultPageTransition = 'none';
      $.mobile.defaultDialogTransition = 'none';
      $.mobile.useFastClick = true;
});
*/

function hideSplash(){
    app_request('','hide_splash','','');
}

function updateLogin(){
      logit("updateLogin");
      logit("set_cfg_emails="+cfg_signup_emails);
    if (cfg_signup_emails == null){
      logit("updateLogin wait");
      setTimeout(updateLogin,100);
    } else {
    if (cfg_signup_emails.length > 0){
logit("option 1");
        $('#email-signup-box').hide();
        $('#login-box').hide();
        $('#select-default-email').attr('value',cfg_signup_emails[0]);
        $('#select-default-email').text(cfg_signup_emails[0]);
        $('#select-default-email').attr('selected', 'selected');
        $('#signup-select-email').selectmenu('refresh');
        for(i=1;i<cfg_signup_emails.length;i++){
            tmp_line = '<option value="'+cfg_signup_emails[i]+'" >'+cfg_signup_emails[i]+'</option>';
            $('#signup-select-email').append(tmp_line);    
        }
        setTimeout(hideSplash,100);
        app_request('','trackevent', 'login_dialog_state', 'combobox');
    } else {
logit("option 2");
        $('#email-signup-combobox').hide();
        setTimeout(hideSplash,100);
        app_request('','trackevent', 'login_dialog_state', 'textfield');
    }
    }
}

$(document).delegate("#login-page", "pageshow", function() {
    logit("login-page pageshow");
    logit("email="+cfg_signup_emails);
    updateLogin()
    app_request('','trackpage', '/login.html', '');
    logit("-------------------new version");
});

$(document).delegate("#login-page", "pageinit", function() {
    logit("login-page pageinit");
    config_init();
    //app_request('set_signup_input_email','get','signup_email','');
    app_request('set_login_input_email','get','email','');
});

$(document).delegate("#login-page", "pagebeforecreate", function() {
    logit("index-page pagebeforecreate");
    app_request('set_cfg_signup_emails', 'get', 'signup_emails', '');
});

$(document).delegate("#index-page", "pagebeforecreate", function() {
    logit("index-page pagebeforecreate");
});

$(document).delegate("#index-page", "pageinit", function() {
    logit("index-page pageinit");
    //app_request('set_cfg_pedometer_state', 'get', 'pedometer_state', '');
    dateObj = new Date();
    day = dateObj.getUTCDay();
    $("#suggestion-text").text(suggestions[day]);
    app_request('','step_update','','');
    app_request('','load_activity_data','','');
    config_init();
    //update_lists_data();
});


$(document).delegate("#index-page", "pageshow", function() {
    logit("index-page pageshow");
    app_request('','trackpage', '/index.html', '');
    //app_request('','trackevent', 'click', 'start_button');
    setTimeout(updateView,500);
    $("#navbar-0").navbar(); 
    setTimeout(hideSplash,600);
});

function updateView(){
    logit("updateView");
    tmp = getDailyAverageSteps();
    $("#step-this-week").text(tmp);
    logit("cfg_pedometer_state="+cfg_pedometer_state);
    logit("cfg_wizard_completed="+cfg_wizard_completed);
    logit("cfg_rating_completed="+cfg_rating_completed);
    logit("cfg_software_update="+cfg_software_update);
    if (cfg_pedometer_state == "started"){
        logit("pedometer was STARTED");
        var btn_element = $("#play-button");
        var span_element = $("span",btn_element);
        $(span_element).addClass('play-image-active');
        start_button_state = 1;
    }
    else if (cfg_pedometer_state == "stopped"){
        logit("pedometer was STOPPED");
        var btn_element = $("#play-button");
        var span_element = $("span",btn_element);
        $(span_element).removeClass('play-image-active');
        start_button_state = 0;
    }

    if (cfg_wizard_completed != "yes") {
        logit("This is first time use");
        tmp = "<p>Uygulamayı ilk defa kullanıyorsanız <a href='welcome2.html'> buraya tıklayın</a></p>"
        $("#suggestion-text").html(tmp);
        //$("#first_use-suggestion").show();
        //$("#index-suggestion").hide();
    } 
    else if (cfg_rating_completed != "yes"){
        tmp = "<p>Her zaman daha iyisini yapmaya çalışıyoruz. Adımsayar uygulamasına <a href='#' onclick='rateApplication();'>oy verin</a></p>"
        $("#suggestion-text").html(tmp);
        
        //$("#first_use-suggestion").hide();
        //$("#index-suggestion").show();
    } else if (cfg_software_update == "advised") {
        logit("This is first time use");
        tmp = "<p>Uygulamanın yeni sürümü yayınlandı<a href='#' onclick='updateSoftware();'> buradan yükleyebilirsiniz</a></p>";
        $("#suggestion-text").html(tmp);
        //$("#first_use-suggestion").show();
        //$("#index-suggestion").hide();
    } else if (cfg_software_update == "required") {
		native_question();
    } else {
		dateObj = new Date();
		day = dateObj.getUTCDay();
		$("#suggestion-text").text(suggestions[day]);
    }
}

/*
$(document).delegate("#ranking-page", "pagebeforecreate", function() {
    logit("ranking-page pagebeforecreate");
    app_request('','','pagebeforecreate','');
    //$("[data-localize]").localize("lang", { language: "tr" });
});

$(document).delegate("#ranking-page", "pageinit", function() {
  logit("ranking-page pageinit");
  //if ranking exits and timedelta < 1 day use it
  // if not ask to server again
    app_request('','','pageinit','');
  display_ranking(ranks);
  $('#ranking-list').listview('refresh');
});

$(document).delegate("#ranking-page", "pageshow", function() {
  logit("ranking-page pageshow");
  app_request('','trackpage', '/ranking.html', '');
  //$('#ranking-list').listview('refresh');
});


$(document).delegate("#diet-page", "pageinit", function() {
  logit("diet-page pageinit");
  //if ranking exits and timedelta < 1 day use it
  // if not ask to server again
  while(diets == null)
  {
      logit("diets is null");
      $.mobile.showPageLoadingMsg();
  }
  $.mobile.hidePageLoadingMsg();
  display_diets(diets);
  //$('#diet-list').listview('refresh');
});

$(document).delegate("#diet-page", "pageshow", function() {
  logit("diet-page pageshow");
  app_request('','trackpage', '/diet.html', '');
  //$('#diet-list').listview('refresh');
});

$(document).delegate("#checkin-page", "pageinit", function() {
  logit("checkin-page pageinit");
  //if ranking exits and timedelta < 1 day display it
  //meanwhile go on normal procedure
  ajax_load_venues();
  //$('#venues-list').listview('refresh');
});

$(document).delegate("#checkin-page", "pageshow", function() {
  logit("checkin-page pageshow");
  app_request('','trackpage', '/checkin.html', '');
});
*/
$(document).delegate("#settings-page", "pageshow", function() {
  logit("settings-page pageshow");
  app_request('','trackpage', '/settings.html', '');
});

$(document).delegate("#welcome3-page", "pageinit", function() {
    logit("welcome-page-3 pageinit");
    if (cfg_gender == "male"){ 
        $("input[id='gender-choice-male']").attr("checked",true).checkboxradio("refresh");
    }else if (cfg_gender == "female") {
        $("input[id='gender-choice-female']").attr("checked",true).checkboxradio("refresh");
    }
    $('#input-lifestyle').val(cfg_lifestyle);
    $('#input-lifestyle').selectmenu('refresh', true);
    app_request('','trackpage', '/welcome3.html', '');
});

$(document).delegate("#welcome4-page", "pageinit", function() {
    logit("welcome-page-4 pageinit");
    $('#input-age').val(cfg_age);
    $('#input-height').val(cfg_height);
    $('#input-weight').val(cfg_weight);
    app_request('','trackpage', '/welcome4.html', '');
});

$(document).delegate("#welcome2-page", "pageinit", function() {
    logit("welcome-page-2 pageinit");
    app_request('','trackpage', '/welcome2.html', '');
});

$(document).delegate("#welcome5-page", "pageinit", function() {
    logit("welcome-page-5 pageinit");
    app_request('','trackpage', '/welcome5.html', '');
});

$(document).delegate("#welcome6-page", "pageinit", function() {
    logit("welcome-page-6 pageinit");
    app_request('set_cfg_wizard_completed', 'set', 'wizard_completed', 'yes');
    app_request('','trackpage', '/welcome6.html', '');
});


function GetLocation(location) {
    logit("lat"+location.coords.latitude);
    logit("lat"+location.coords.longitude);
    logit("lat"+location.coords.accuracy);
}
/*
function wait_for_venues_list(){
  currentUrl = $.mobile.activePage.data('url');
  logit(currentUrl);
  while((venues == null) && (currentUrl == '/mobindex/checkin.html'))
  {
      logit("venues is null");
      setTimeout(wait_for_venues_list, 100);
      $.mobile.loadingMessage ='Konum listesi güncelleniyor';
      $.mobile.loadingMessageTextVisible=true;
      $.mobile.showPageLoadingMsg();
      return;
  }
  $.mobile.loadingMessageTextVisible=false;  
  $.mobile.hidePageLoadingMsg();
  if (venues != null){
      display_venues(venues);
  }
  //$('#venues-list').listview('refresh');
  navigator.geolocation.getCurrentPosition(GetLocation, function(errorCode) {
    if (errorCode == 1) {
       logit("geolocation response:"+errorCode);
    }
  });
}

$(document).delegate("#checkin-page", "pageshow", function() {
  logit("checkin-page pageshow");
  wait_for_venues_list();
});
*/
$(document).delegate("#settings-page", "pageinit", function() {
  logit("settings-page pageinit");
    $('#input-nickname').val(cfg_nickname);
    $('#input-email').val(cfg_email);
    //$('#input-gender').val(cfg_gender);
    //$('#gender-choice-male').attr('checked', true);
    //$('#gender-choice-female').attr('checked','checked');
    if (cfg_gender == "male"){ 
        $("input[id='gender-choice-male']").attr("checked",true).checkboxradio("refresh");
    }else if (cfg_gender == "female") {
        $("input[id='gender-choice-female']").attr("checked",true).checkboxradio("refresh");
    }
    $('#input-age').val(cfg_age);
    $('#input-height').val(cfg_height);
    $('#input-weight').val(cfg_weight);
    $('#input-lifestyle').val(cfg_lifestyle);
    $('#input-lifestyle').selectmenu('refresh', true);
    $('#input-mode').val(cfg_mode);
    $('#input-mode').selectmenu('refresh', true);
    $('#input-sensivity').val(cfg_sensivity);
    $('#input-device_id').val(cfg_device_id);
    $('#input-password').val(cfg_password);
});


function set_cfg_nickname(nickname){
    cfg_nickname = nickname;
}

function set_cfg_email(email){
    cfg_email = email;
}

function set_cfg_gender(gender){
    cfg_gender = gender;
}

function set_cfg_age(age){
    cfg_age = age;
}

function set_cfg_height(height){
    cfg_height = height;
}

function set_cfg_default_sensivity(param){
    cfg_default_sensivity = param;
}

function set_cfg_weight(weight){
    cfg_weight = weight;
}

function set_cfg_lifestyle(lifestyle){
    cfg_lifestyle = lifestyle;
}

function set_cfg_mode(mode){
    cfg_mode = mode;
}

function set_cfg_sensivity(sensivity){
    cfg_sensivity = sensivity;
}

function set_cfg_device_id(device_id){
    cfg_device_id = device_id;
}


function set_cfg_password(password){
    cfg_password = password;
}

function set_cfg_first_use(param){
    cfg_first_use = param;
}

function set_cfg_wizard_completed(param){
    cfg_wizard_completed = param;
}

function set_cfg_rating_completed(param){
    cfg_rating_completed = param;
}

function set_cfg_software_update(param){
    cfg_software_update = param;
}

function set_cfg_config_changed(param){
    cfg_config_changed = param;
}

function set_cfg_platform(param){
    cfg_platform = param;
}

function set_cfg_swversion(param){
    cfg_swversion = param;
}

function set_cfg_app_state(param){
    cfg_app_state = param;
}

function set_cfg_signup_emails(param){
logit("cfg_signup_emails="+param);
    if (param.length > 4) {
        cfg_signup_emails = param.split(';');
    } else {
        cfg_signup_emails = [];
    }
logit("signup_emails_list:"+cfg_signup_emails);
}



function set_cfg_pedometer_state(param){
    cfg_pedometer_state = param;
    logit("1cfg_pedometer_state="+cfg_pedometer_state);
}

function set_signup_input_email(email){
    $('#signup-input-email').val(email);
}

function set_login_input_email(email){
    $('#login-input-email').val(email);
}

function config_init(){
    logit("config_init");
    app_request('set_cfg_app_state', 'get', 'app_state', '');
//    app_request('set_cfg_signup_emails', 'get', 'signup_emails', '');
    app_request('set_cfg_default_sensivity','get','default_sensivity','');
    app_request('set_cfg_pedometer_state', 'get', 'pedometer_state', '');
    app_request('set_cfg_nickname', 'get', 'username', '');
    app_request('set_cfg_email', 'get', 'email', '');
    app_request('set_cfg_gender', 'get', 'gender', '');
    app_request('set_cfg_age', 'get', 'age', '');
    app_request('set_cfg_height', 'get', 'height', '');
    app_request('set_cfg_weight', 'get', 'weight', '');
    app_request('set_cfg_lifestyle', 'get', 'lifestyle', '');
    app_request('set_cfg_mode', 'get', 'mode', '');
    app_request('set_cfg_sensivity', 'get', 'sensivity', '');
    app_request('set_cfg_device_id', 'get', 'device_id', '');
    app_request('set_cfg_password', 'get', 'password', '');
    app_request('set_cfg_first_use', 'get', 'first_use', '');
    app_request('set_cfg_wizard_completed', 'get', 'wizard_completed', '');
    app_request('set_cfg_rating_completed', 'get', 'rating_completed', '');
    app_request('set_cfg_software_update', 'get', 'software_update', '');
    app_request('set_cfg_config_changed', 'get', 'config_changed', '');
    app_request('set_cfg_platform', 'get', 'platform', '');
    app_request('set_cfg_swversion', 'get', 'swversion', '');
//    cfg_nickname = "ozkolonur";
//    cfg_email = "ozkolonur@gmail.com";
//    cfg_gender = "male";
//    cfg_age = "28";
//    cfg_height = "178";
//    cfg_weight = "78";
//    cfg_lifestyle = "1";
//    cfg_mode = "auto";
//    cfg_sensivity = "38";
//    cfg_device_id = "fffffffe-e0e0-17d4-4349-5aae2fce6653";
//    cfg_password = "123123";
}

function inputChanged(object){
    app_request('set_cfg_config_changed','set', 'config_changed', 'yes');
    obj_config = object.getAttribute("config")
    logit("input_changed:" + object.getAttribute("config"));
    logit("value" + object.value);
    if (obj_config == "gender") {
        logit("gender config");
        if (object.value == "off"){
	        app_request("set_cfg_gender",'set', "gender", "male");
		} else if (object.value == "on") {
	        app_request("set_cfg_gender",'set', "gender", "female");
        }
	} 
	else {
        callback = "set_cfg_"+obj_config
	    app_request(callback,'set', obj_config, object.value);
	}
}

function sensivityChanged(){
	tmp_sensivity = $("#input-sensivity").val();
	logit("sensivityChanged:"+tmp_sensivity);
	app_request('','set','sensivity',tmp_sensivity);
	settingsInputChanged();
}

function wizardCompleted(){
	logit("wizardCompleted");
	app_request('set_cfg_wizard_completed','set', 'wizard_completed', 'yes');
    setTimeout(updateView,1000);
}

function settingsInputChanged(){
	logit('settingInputChanged');
	app_request('set_cfg_config_changed','set', 'config_changed', 'yes');
	clearTimeout(settingsInputChangedTimer);
	settingsInputChangedTimer = setTimeout(startSync,10000);
}

function startSync(){
	logit('startSync');
    app_request('', 'sync', '','');
}
/*
function btnSave(){
    logit('btnSave');
    items = $('#settings').serializeArray();
    for(i=0; i<items.length; i++){
        logit(items[i].name);
    }
    $.ajax({
        url: server_addr + "/mobsync/config/",
        type: "post",
        data: items,
        // callback handler that will be called on success
        success: function(response, textStatus, jqXHR){
            // log a message to the console
            logit("Hooray, it worked!");
            logit(response);
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

function check_new_version(){
    logit('check_new_version');
    
    $.ajax({
        url: server_addr + "/mobsync/latest_version/",
        type: "post",
        data: {'platform':cfg_platform},
        // callback handler that will be called on success
        success: function(response, textStatus, jqXHR){
            // log a message to the console
            logit("Got a latest_version response");
            logit(response);
            latest_version = response['result'];
            cmp_result = version_compare(latest_version, cfg_swversion);
            if (cmp_result == 1){
                logit('new version available');
                native_alert
            }
            else if(cmp_result == 0){
                logit('no new version');
            }
            //if response['result'] == ""
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
function btnCancel(){
    logit('btnCancel');
}
*/



//----------------- ranking -----------------------
/*
function ajax_load_ranking(){
    logit("loading ranks...");    
    $.ajax({
        url: server_addr + "/score/near_20/",
        type: "post",
        data:null,
        // callback handler that will be called on success
        success: function(response, textStatus, jqXHR){
            // log a message to the console
            //logit("Hooray, it worked!");
            //var datax = response;
            logit(response);
            ranks = response;
            ranks_updated = new Date();
            //$("#ranking-list").listview("destroy").listview();
            //$('#ranking-list').children().remove('li');
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
        complete: function(jqXHR, textStatus){
            // enable the inputs
            logit("completed loading ranks.");
        }
    });
}

function display_ranking(ranks)
{
    //msg = ranks[0].nickname;
    app_request('','','display_ranking:2222','');

    for (var i=0; i<20; i++){
        list_add_rank(ranks[i].icon, ranks[i].rank, ranks[i].nickname, ranks[i].score);
    }
}

function list_add_rank(icon, rank, nickname, points)
{
	icon= server_addr + "/site_media/mobindex/images/smile_2_icon.png";
    logit(nickname+"new object added");
    html = '<li><img src="'+ icon + '" class="ui-li-icon" height="32px" width="32px">' + rank + ' ' + nickname + '<span class="ui-li-count">'+points+'</span></li>'
    $('#ranking-list').append(html);
}
//--------------- endof - ranking -----------------


//----------------- checkin -----------------------
clientId = 'UKSUC1PGOQ014EKAORXA0XSXYKYWECNW3BAFADTCXLZNEVHW';
clientSecret = 'G0MFUR0LAJDUD3GULQ0I3JZK0G5VUNDYWTNIC5CRHQPDWBZ0';
redirectUri = location.href;

function ajax_load_venues(){
    logit("loading venues...");
    $.ajax({
        url: server_addr + "/venues/list/",
        type: "post",
        data: null,
        // callback handler that will be called on success
        success: function(response, textStatus, jqXHR){
            // log a message to the console
            //logit("Hooray, it worked!");
            //var datax = response;
            logit(response);
            venues = response;
            venues_updated = new Date();
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
        complete: function(jqXHR, textStatus){
            // enable the inputs
            logit("completed loading venues.");
        }
    });
}

function display_venues(venues)
{
    for (var i=0; i<venues.length; i++){
        if (venues[i].fields.icon != null){
            icon = venues[i].fields.icon;
        } else {
            icon = "http://foursquare.com/img/categories/building/default_32.png"
        }
        list_add_venue(icon, venues[i].fields.name, venues[i].fields.description, venues[i].fields.points);
    }
}

function list_add_venue(icon, name, distance, points)
{
    venue_src = "https://foursquare.com/img/categories/arts_entertainment/stadium_soccer_32.png";
    venue_name = "Saray Muhallebi";
    venue_info = "Sagligini dusunenlere ekonomik lezzetler";
    venue_points = "200";
    venue_link = "#";
    html = '<li><a href="#"><img src="' + icon +'" class="ui-li-icon">' + '<span class="ui-li-desc-checkin">' + name + '</span>' + '<p class="ui-li-desc-checkin">' + distance + '</p>' + '<span class="ui-li-count">' + points + '</span></a></li>'
    $('#venues-list').append(html);
}
//--------------- endof - checkin -----------------

//-------------------- diet -----------------------
function ajax_load_diets(){
    logit("loading diets...");
    $.ajax({
        url: server_addr + "/diet/sync/",
        type: "post",
        data:null,
        // callback handler that will be called on success
        success: function(response, textStatus, jqXHR){
            // log a message to the console
            //logit("Hooray, it worked!");
            //var datax = response;
            logit(response);
            diets = response;
            diets_updated = new Date();
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
        complete: function(jqXHR, textStatus){
            // enable the inputs
            logit("completed loading diets.");
        }
    });
}

function display_diets(diets)
{
    for (var i=0; i<diets.length; i++){
        list_add_diet(diets[i].fields.name, diets[i].fields.desc, diets[i].fields.rating);
    }
}

function list_add_diet(name, description, num_people)
{
    html = '<li><a href="index.html"><h3>' + name + '</h3><p>' + description + '</p><span class="ui-li-count">' + num_people +' people is on this diet</span></a></li>'
    $('#diet-list').append(html);
}
//--------------- endof - diet --------------------
*/



