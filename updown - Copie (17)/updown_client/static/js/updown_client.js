/**
 * @fileOverview UPDOWN dashboard. It utilizes the Forum API to 
                 handle user information (retrieve currencies exchange, edit , 
                 as well as add and remove new choices from the system). It also 
                 permits to list and user's choices.
 * @author <a href="mailto:nadir.bengana@oulu.fi">Nadir be,gana</a>
 * @version 1.0
 * 
 * NOTE: The documentation utilizes jQuery syntax to refer to classes and ids in
         the HTML code: # is utilized to refer to HTML elements ids while . is
         utilized to refer to HTML elements classes.
**/


/**** START CONSTANTS****/

/** 
 * Set this to true to activate the debugging messages. 
 * @constant {boolean}
 * @default 
 */
var DEBUG = true;

/** 
 * Mason+JSON mime-type 
 * @constant {string}
 * @default 
 */
const MASONJSON = "application/vnd.mason+json";

const PLAINJSON = "application/json";

/** 
 * Link to Users_profile
 * @constant {string}
 * @default 
 */
const UPDOWN_USER_PROFILE = "/profiles/users";

/** 
 * Link to Choices_profile
 * @constant {string}
 * @default 
 */
const FORUM_MESSAGE_PROFILE = "/profiles/choices";

/** 
 * Default datatype to be used when processing data coming from the server.
 * Due to JQuery limitations we should use json in order to process Mason responses
 * @constant {string}
 * @default 
 */
const DEFAULT_DATATYPE = "json";

/** 
 * Entry point of the application
 * @constant {string}
 * @default 
 */
const ENTRYPOINT = "/updown/api/users/"; //Entrypoint: Resource Users
const SERVER = "http://localhost:5000/updown/api/user/"; //Entrypoint: Resource Users

/**** END CONSTANTS****/


/**** START RESTFUL CLIENT****/

/**** Description of the functions that call UPDOWN API by means of jQuery.ajax()
      calls. We have implemented one function per link relation in both profiles.
      Since we are not interesting in the whole API functionality, some of the
      functions does not do anything. Hence, those link relations are ignored
****/ 


/**
 * This function is for the user choices.
 *
 * 
 * Sends an AJAX GET request to retrive the list of all the users of the application
 * 
 * ONSUCCESS=> Show user choice in the #choices_list. 
 *             After processing the response it utilizes the method {@link #appendChoiceToList}
 *             to append the choice to the list.  
 *             Each choice is an anchor pointing to the respective choice url.
 * ONERROR => Show an alert to the user.
 *
 * @param {string} [apiurl = ENTRYPOINT] - The url of the User choices instance.
**/
function getUserChoices(apiurl) {
    apiurl = apiurl || ENTRYPOINT;
    return $.ajax({
        url: apiurl,
        dataType:DEFAULT_DATATYPE
    }).always(function(){
        //Remove old list of users
        //clear the form data hide the content information(no selected)
        $("#user_list").empty();
        $("#mainContent").hide();

    }).done(function (data, textStatus, jqXHR){
		if (DEBUG) {
            console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus);
        }
        //Extract the choices
        choices = data.items;
        for (var i=0; i < choices.length; i++){
            var choice = choices[i];
            //Extract the choices 
            appendChoiceToList(choice.from_currency,choice.to_currency,choice.date_from,choice.date_to);
        }

        //Prepare the new_user_form to create a new user
        /*var create_ctrl = data["@controls"]["forum:add-user"]
        
        if (create_ctrl.schema) {
            createFormFromSchema(create_ctrl.href, create_ctrl.schema, "new_user_form");
        }
        else if (create_ctrl.schemaUrl) {
            $.ajax({
                url: create_ctrl.schemaUrl,
                dataType: DEFAULT_DATATYPE
            }).done(function (data, textStatus, jqXHR) {
                createFormFromSchema(create_ctrl.href, data, "new_user_form");
            }).fail(function (jqXHR, textStatus, errorThrown) {
                if (DEBUG) {
                    console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown);
                }
                alert ("Could not fetch form schema.  Please, try again");
            });
        }
		*/
    }).fail(function (jqXHR, textStatus, errorThrown){
        /*if (DEBUG) {
            console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown);
        }
        //Inform user about the error using an alert message.
        alert ("Could not fetch the list of users.  Please, try again");*/
    });
}


function getUsers(apiurl) {
    apiurl = apiurl || ENTRYPOINT;
    $("#mainContent").hide();
    return $.ajax({
        url: apiurl,
        dataType:DEFAULT_DATATYPE
    }).always(function(){
        //Remove old list of users
        //clear the form data hide the content information(no selected)
        $("#user_list").empty();
        $("#mainContent").hide();

    }).done(function (data, textStatus, jqXHR){
        if (DEBUG) {
            console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus);
        }
        //Extract the users
        users = data.items;
        for (var i=0; i < users.length; i++){
            var user = users[i];
            //Extract the nickname by getting the data values. Once obtained
            // the nickname use the method appendUserToList to show the user
            // information in the UI.
            appendUserToList(user["@controls"].self.href, user.nickname)
        }

        //Prepare the new_user_form to create a new user
        var create_ctrl = data["@controls"]["forum:add-user"]
        
        if (create_ctrl.schema) {
            createFormFromSchema(create_ctrl.href, create_ctrl.schema, "new_user_form");
        }
        else if (create_ctrl.schemaUrl) {
            $.ajax({
                url: create_ctrl.schemaUrl,
                dataType: DEFAULT_DATATYPE
            }).done(function (data, textStatus, jqXHR) {
                createFormFromSchema(create_ctrl.href, data, "new_user_form");
            }).fail(function (jqXHR, textStatus, errorThrown) {
                if (DEBUG) {
                    console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown);
                }
                alert ("Could not fetch form schema.  Please, try again");
            });
        }
    }).fail(function (jqXHR, textStatus, errorThrown){
        if (DEBUG) {
            console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown);
        }
        //Inform user about the error using an alert message.
        alert ("Could not fetch the list of users.  Please, try again");
    });
}


/*** RELATIONS USED IN MESSAGES AND USERS PROFILES ***/

/**
 * Associated rel attribute: users-all
 * @see {@link #getUsers}
**/
function users_all(apiurl){
    return getUsers(apiurl);
}

/**
 * This client does not support this functionality.
 *
 * Associated rel attribute: messages-all
 *
 * @param {string} apiurl - The url of the Messages list.
**/
function messages_all(apiurl){
    return; //THE CLIENT DOES NOT KNOW HOW TO HANDLE LIST OF MESSAGES
}

/*** FUNCTIONS FOR MESSAGE PROFILE ***/

/*** Note, the client is mainly utilized to manage users, not to manage
messages ***/


/**
 * This client does not support this functionality.
 *
 * Associated rel attribute: reply
 *
 * @param {string} apiurl - The url of the parent message.
 * @param {object} body - An associative array with the new message
 * 
**/
function reply(apiurl,body){
    return; //THE CLIENT DOES NOT KNOW HOW TO ADD A NEW MESSAGE
}

/**
 * Sends an AJAX request to remove a message from the system. Utilizes the DELETE method.
 *
 * Associated rel attribute: delete (in Message profile)
 * ONSUCCESS=>
 *          a) Inform the user with an alert.
 *          b) Go to the initial state by calling the function {@link #reloadUserData} *
 *
 * ONERROR => Show an alert to the user
 *
 * @param {string} apiurl - The url of the Message
 * 
**/
    
function delete_message(apiurl){
    //TODO 3: Send an AJAX request to remove the current message
        // Do not implement the handlers yet, just show some DEBUG text in the console.
        // You just need to send a $.ajax request of type "DELETE". No extra parameters
        //are required.
    //TODO 4
       //Implemente the handlers following the instructions from the function documentation.
	   
	
	$.ajax({
        url: apiurl,
        type: "DELETE",
    }).done(function (data, textStatus, jqXHR){
        if (DEBUG) {
            console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus);
        }
        alert ("The messages  has been deleted from the database");
        //Update the list of messages from the server.
        reloadUserData();    
	
    }).fail(function (jqXHR, textStatus, errorThrown){
        if (DEBUG) {
            console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown);
        }
        alert ("The message could not be deleted from the database");
    });

	
	 
	return;
}

/**
 * This client does not support this functionality.
 *
 * Associated rel attribute: add-message
 *
 * @param {string} apiurl - The url of the parent Messages collection
 * 
**/
function add_message(apiurl,template){
    return; //THE CLIENT DOES NOT KNOW HOW TO HANDLE COLLECTION OF MESSAGES
}

/**
 * This client does not support this functionality.
 *
 * Associated rel attribute: author
 *
 * @param {string} apiurl - The url of the User instance.
**/
function author(apiurl){
    return; //THE CLIEND DOES NOT KNOW TO HANDLE THIS RELATION.
}

/**
 * This client does not support this functionality.
 *
 * Associated rel attribute: collection (message_profile)
 *
 * @param {string} apiurl - The url of the Messages list.
**/
function collection_messages(apiurl){
    return; //THE CLIENT DOES NOT KNOW HOW TO HANDLE A LIST OF MESSAGES
}

/**
 * This client does not support this functionality.
 *
 * Associated rel attribute: edit (in message profile)
 *
 * @param {string} apiurl - The url of the Message
 * @param {object} message - An associative array containing the new information 
 *   of the message
 * 
**/
function edit_message(apiurl, template){
    return; //THE CLIENT DOES NOT KNOW HOW TO HANDLE COLLECTION OF MESSAGES
}

/**
 * This client does not support this functionality.
 *
 * Associated rel attribute: in-reply-to
 *
 * @param {string} apiurl - The url of the Message
**/
function in_reply_to(apiurl){
    return; //THE CLIENT DOES NOT KNOW HOW TO REPRESENT A HIERARHCY OF MESSAGEs

}

/**
 * Sends an AJAX request to retrieve message information Utilizes the GET method.
 *
 * Associated rel attribute: self (in message profile)
 *
 * ONSUCCESS=>
 *          a) Extract message information from the response body. The response
 *             utilizes a HAL format.
 *          b) Show the message headline and articleBody in the UI. Call the helper
 *             method {@link appendMessageToList}
 *
 * ONERROR => Show an alert to the user
 *
 * @param {string} apiurl - The url of the Message
 * 
**/

function get_message(apiurl){
    $.ajax({
        url: apiurl,
        dataType:DEFAULT_DATATYPE
    }).done(function (data, textStatus, jqXHR){
        if (DEBUG) {
            console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus);
        }
        var message_url = data["@controls"].self.href;
        var headline = data.headline;
        var articleBody =  data.articleBody;
        appendMessageToList(message_url, headline, articleBody);

    }).fail(function (jqXHR, textStatus, errorThrown){
        if (DEBUG) {
            console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown);
        }
        alert("Cannot get information from message: "+ apiurl);
    });
}


/*** FUNCTIONS FOR USER PROFILE ***/

/**
 * Sends an AJAX request to retrieve information related to a User
 *
 * Associated link relation:self (inside the user profile)
 *
 *  ONSUCCESS =>
 *              Fill basic user choices
 *  ONERROR =>  Reopen the form
 * 
 *  @param {string} apiurl - The url of the User instance. 
**/
function get_user(template) {
    if (DEBUG) {
        console.log ("__________________________________________");
        console.log ("get_user function");
		console.log ("Local data :"+JSON.stringify(template));
        console.log ("local username"+template.username);
        console.log ("local password"+template.password);
	}

	return $.ajax({
        url: SERVER+template.username,
        dataType:DEFAULT_DATATYPE,
        processData:false,
    }).done(function (data, textStatus, jqXHR){
        if (DEBUG) {
            console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus);
            console.log ("RECEIVED RESPONSE: username:",data.username,"; textStatus:",textStatus);
            console.log ("RECEIVED RESPONSE: password:",data.password,"; textStatus:",textStatus);
            console.log ("RECEIVED RESPONSE: fullname:",data.fullname,"; textStatus:",textStatus);
			
			
        }
		if(template.password==data.password){			
			if (DEBUG) {
				console.log ("Login successful");
			}
			$.cookie("userid", data.userid); 
			$.cookie("username", data.username); 
			$.cookie("password", data.password); 
			$.cookie("fullname", data.fullname); 
			$.cookie("loggedin", "yes"); 
			onLoginSuccess();
			if (DEBUG) {
				console.log ("cookie var userid: "+ $.cookie("userid"));
				console.log ("cookie var username: "+ $.cookie("username"));
				console.log ("cookie var password: "+ $.cookie("password"));
				console.log ("cookie var fullname: "+ $.cookie("fullname"));
				console.log ("cookie var loggedin: "+ $.cookie("loggedin"));
			}
			
		}else{
			if (DEBUG) {
				console.log ("Login failed!");
			}
	        alert ("Cannot login. enter the right credentials!");
		}
		
		if (DEBUG) {
			console.log ("_______________________________________");
		}
    }).fail(function (jqXHR, textStatus, errorThrown){
        if (DEBUG) {
            console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown);
        }
        //Show an alert informing that I cannot get info from the user.
        alert ("Cannot login. enter the right credentials!");
		if (DEBUG) {
			console.log ("_______________________________________");
		}
    });

}


/**
 * Sends an AJAX GET request to retrieve information related to user history.
 *
 * Associated rel attribute: messages-history 
 *
 * ONSUCCESS =>
 *   a.1) Check the number of messages received (data.items) 
 *   a.2) Add the previous value to the #messageNumber input element (located in 
 *        #userHeader section).
 *   b.1) Iterate through all messages. 
 *   b.2) For each message in the history, access the message information by
 *        calling the corresponding Message instance (call {@link get_message})
 *        The url of the message is obtained from the href attribute of the
 *        message item. 
 * ONERROR =>
 *    a)Show an *alert* informing the user that the target user history could not be retrieved
 *    b)Deselect current user calling {@link #deselectUser}.
 * @param {string} apiurl - The url of the History instance.
**/
    //TODO 3: Send the AJAX to retrieve the history information. 
    //        Do not implement the handlers yet, just show some DEBUG text in the console.
    //TODO 4: Implement the handlers for done() and fail() responses 
    
function messages_history(apiurl){
	return $.ajax({
        url: apiurl,
        dataType:DEFAULT_DATATYPE
    }).always(function(){
    
    }).done(function (data, textStatus, jqXHR){
        if (DEBUG) {
            console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus);
        }
        messages = data.items;
		$("#messagesNumber").html(messages.length);
        for (var i=0; i < messages.length; i++){
            var message = messages[i];
			console.log("message data : "+message.id);
			console.log("message data : "+message.headline);
			console.log("message data : "+message["@controls"].self.href);
			message_url=message["@controls"].self.href;
			get_message(message_url);	
		}
	}).fail(function (jqXHR, textStatus, errorThrown){
        if (DEBUG) {
            //console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown);
        }
        //Inform user about the error using an alert message.
        $("#messagesNumber").html("0");

		alert ("Could not fetch the list of messages.  Please, try again");
		//deselectUser();
    });     
	
	
	return false;
}

/**
 * Sends an AJAX request to delete an user from the system. Utilizes the DELETE method.
 *
 * Associated rel attribute: delete (User profile)
 *
 *ONSUCCESS =>
 *    a)Show an alert informing the user that the user has been deleted
 *    b)Reload the list of users: {@link #getUsers}
 *
 * ONERROR =>
 *     a)Show an alert informing the user that the new information was not stored in the databse
 *
 * @param {string} apiurl - The url of the intance to delete. 
**/
function delete_user(apiurl){
    $.ajax({
        url: apiurl,
        type: "DELETE",
    }).done(function (data, textStatus, jqXHR){
        if (DEBUG) {
            console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus);
        }
        alert ("The user information has been deleted from the database");
        //Update the list of users from the server.
        getUsers();

    }).fail(function (jqXHR, textStatus, errorThrown){
        if (DEBUG) {
            console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown);
        }
        alert ("The user information could not be deleted from the database");
    });
}

/**
 * This client does not support handling public user information
 *
 * Associated rel attribute: public-data
 * 
 * @param {string} apiurl - The url of the Public profile instance.
**/
function public_data(apiurl){
    return; // THE CLIENT DOES NOT SHOW USER PUBLIC DATA SUCH AVATAR OR IMAGE

}

/**
 * Sends an AJAX request to retrieve the restricted profile information:
 * {@link http://docs.pwpforum2017appcompleteversion.apiary.io/#reference/users/users-private-profile/get-user's-restricted-profile | User Restricted Profile}
 * 
 * Associated rel attribute: private-data
 * 
 * ONSUCCESS =>
 *  a) Extract all the links relations and its corresponding URLs (href)
 *  b) Create a form and fill it with attribute data (semantic descriptors) coming
 *     from the request body. The generated form should be embedded into #user_restricted_form.
 *     All those tasks are performed by the method {@link #fillFormWithMasonData}
 *     b.1) If "user:edit" relation exists add its href to the form action attribute. 
 *          In addition make the fields editables and use template to add missing
 *          fields. 
 *  c) Add buttons to the previous generated form.
 *      c.1) If "user:delete" relation exists show the #deleteUserRestricted button
 *      c.2) If "user:edit" relation exists show the #editUserRestricted button
 *
 * ONERROR =>
 *   a)Show an alert informing the restricted profile could not be retrieved and
 *     that the data shown in the screen is not complete.
 *   b)Unselect current user and go to initial state by calling {@link #deselectUser}
 * 
 * @param {string} apiurl - The url of the Restricted Profile instance.
**/
function private_data(apiurl){
    return $.ajax({
            url: apiurl,
            dataType:DEFAULT_DATATYPE,
        }).done(function (data, textStatus, jqXHR){
            if (DEBUG) {
            console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus);
            }
            //Extract links
            var user_links = data["@controls"];
            var schema, resource_url = null;
            if ("edit" in user_links){
                resource_url = user_links["edit"].href;
                //Extract the template value
                schema = user_links["edit"].schema;
                if (user_links["edit"].schema) {
                    $form = createFormFromSchema(resource_url, schema, "user_restricted_form");
                    $("#editUserRestricted").show();
                    fillFormWithMasonData($form, data);
                }
                else if (user_links["edit"].schemaUrl) {
                    $.ajax({
                        url: user_links["edit"].schemaUrl,
                        dataType: DEFAULT_DATATYPE
                    }).done(function (schema, textStatus, jqXHR) {
                        $form = createFormFromSchema(resource_url, schema, "user_restricted_form");
                        $("#editUserRestricted").show();
                        fillFormWithMasonData($form, data);                        
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        if (DEBUG) {
                            console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown);
                        }
                        alert ("Could not fetch form schema.  Please, try again");
                    });
                }
                else {
                    alert("Form schema not found");
                }
            }            
            
        }).fail(function (jqXHR, textStatus, errorThrown){
            if (DEBUG) {
                console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown);
            }
            //Show an alert informing that I cannot get info from the user.
            alert ("Cannot extract all the information about this user from the server");
            deselectUser();
        });
}

/**
 * Sends an AJAX request to create a new user {@link http://docs.pwpforum2017appcompleteversion.apiary.io/#reference/users/user}
 *
 * Associated link relation: add_user
 *
 *  ONSUCCESS =>
 *       a) Show an alert informing the user that the user information has been modified
 *       b) Append the user to the list of users by calling {@link #appendUserToList}
 *          * The url of the resource is in the Location header
 *          * {@link #appendUserToList} returns the li element that has been added.
 *       c) Make a click() on the added li element. To show the created user's information.
 *     
 * ONERROR =>
 *      a) Show an alert informing that the new information was not stored in the databse
 * 
 * @param {string} apiurl - The url of the User instance. 
 * @param {object} user - An associative array containing the new user's information
 * 
**/   
function add_user(apiurl,user){
    var userData = JSON.stringify(user);
    var nickname = user.nickname;
    return $.ajax({
        url: apiurl,
        type: "POST",
        //dataType:DEFAULT_DATATYPE,
        data:userData,
        processData:false,
        contentType: PLAINJSON
    }).done(function (data, textStatus, jqXHR){
        if (DEBUG) {
            console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus);
        }
        alert ("User successfully added");
        //Add the user to the list and load it.
        $user = appendUserToList(jqXHR.getResponseHeader("Location"),nickname);
        $user.children("a").click();

    }).fail(function (jqXHR, textStatus, errorThrown){
        if (DEBUG) {
            console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown);
        }
        alert ("Could not create new user:"+jqXHR.responseJSON.message);
    });
}

/**Get all users.
 *
 * Associated rel attribute: collection (user profile)
 *
 * @param {string} apiurl - The url of the Users list.
 * @see {@link #getUsers}
**/
function collection_users(apiurl){
    return users_all(apirul);
}

/**
 * Get user information. 
 *
 * Associated rel attribute: up
 *
 * @param {string} apiurl - The url of the User instamce
**/
function up(apiurl){
    return; //We do not process this information. 
}

/**
 * Sends an AJAX request to modify the restricted profile of a user, using PUT
 *
 * NOTE: This is NOT utilizied in this application.
 *
 * Associated rel attribute: edit (user profile)
 *
 * ONSUCCESS =>
 *     a)Show an alert informing the user that the user information has been modified
 * ONERROR =>
 *     a)Show an alert informing the user that the new information was not stored in the databse
 * 
 * @param {string} apiurl - The url of the intance to edit. 
 * @param {object} body - An associative array containing the new data of the
 *  target user
 * 
**/
function edit_user(apiurl, body){
    $.ajax({
        url: apiurl,
        type: "PUT",
        data:JSON.stringify(body),
        processData:false,
        contentType: PLAINJSON
    }).done(function (data, textStatus, jqXHR){
        if (DEBUG) {
            console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus);
        }
        alert ("User information have been modified successfully");

    }).fail(function (jqXHR, textStatus, errorThrown){
        if (DEBUG) {
            console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown);
        }
        var error_message = $.parseJSON(jqXHR.responseText).message;
        alert ("Could not modify user information;\r\n"+error_message);
    });
}


/**** END RESTFUL CLIENT****/

/**** UI HELPERS ****/

/**** This functions are utilized by rest of the functions to interact with the
      UI ****/
	  
/**
 * Show the login form 
 *
**/	  
function getLoginForm() {
	console.log ("___________________________________");
	console.log ("getLoginForm loaded!");
    $("#sidebar").hide();
    $("#userInfo").hide();
    $("#userData").hide();
    $("#newUser").hide();
	if($.cookie("loggedin")=="yes"){
		if (DEBUG) {console.log ("Alredy Loggedin");}
		onLoginSuccess();
	}
	if (DEBUG) {
		console.log ("cookie var userid: "+ $.cookie("userid"));
		console.log ("cookie var username: "+ $.cookie("username"));
		console.log ("cookie var password: "+ $.cookie("password"));
		console.log ("cookie var fullname: "+ $.cookie("fullname"));
		console.log ("cookie var loggedin: "+ $.cookie("loggedin"));
	}
	console.log ("___________________________________");	
}

/**
 * Show the choices list  
 *
**/	  
function onLoginSuccess() {
	console.log ("___________________________________");	
	console.log ("onLoginSuccess!");	
	$("#userInfo").show();
	$("#loginForm").hide();
	$("#sidebar").show();
    $("#userData").hide();
    $("#newUser").hide();
	appendUserInfo();
	appendLogoutBtton();
	console.log ("___________________________________");	
}

/**
 * Append a the user to the #userInfo. 
**/
function appendUserInfo() {
    var $user = '<h5>Username : '+$.cookie("username")+'</h5><h5>Full name : '+$.cookie("fullname")+'</h5>';
    $("#userInfo").append($user);
}

function appendLogoutBtton() {
    var $btn = '<li ><a class="fa fa-edit"  href="/logoutFn"> Logout</a></li>';
    $("#logoutBtn").append($btn);
}


/**
 * Append a new user to the #user_list. It appends a new <li> element in the #user_list 
 * using the information received in the arguments.  
 *
 * @param {string} url - The url of the User to be added to the list
 * @param {string} nickname - The nickname of the User to be added to the list
 * @returns {Object} The jQuery representation of the generated <li> elements.
**/
function appendUserToList(url, nickname) {
    var $user = $('<li class="nav-item">').html('<a class= "user_link nav-link " href="'+url+'"><span  class="oi oi-person"></span>'+nickname+'</a>');
    //Add to the user list
    $("#user_list").append($user);
    return $user;
}

/**
 * Append a new user to the #user_list. It appends a new <li> element in the #user_list 
 * using the information received in the arguments.  
 *
 * @param {string} url - The url of the User to be added to the list
 * @param {string} nickname - The nickname of the User to be added to the list
 * @returns {Object} The jQuery representation of the generated <li> elements.
**/
function appendChoiceToList(from_currency, to_currency, from_date, to_date) {
    var $choice = $('<li class="nav-item" style="border:2px solid red;padding:20px;padding-bottom:10px;">').html('from_currency : '+from_currency+'<br/>to_currency : '+to_currency+'<br/>from_date : '+from_date+'<br/>to_date : '+to_date+'<hr />');
	$("#choices_list").append($choice);
}

/**
 * Populate a form with the <input> elements contained in the <i>schema</i> input parameter.
 * The action attribute is filled in with the <i>url</i> parameter. Values are filled
 * with the default values contained in the template. It also marks inputs with required property. 
 *
 * @param {string} url - The url of to be added in the action attribute
 * @param {Object} schema - a JSON schema object ({@link http://json-schema.org/}) 
 * which is utlized to append <input> elements in the form
 * @param {string} id - The id of the form is gonna be populated
**/
function createFormFromSchema(url,schema,id){
    $form=$('#'+ id);
    $form.attr("action",url);
    //Clean the forms
    $form_content=$(".form_content",$form);
    $form_content.empty();
    $("input[type='button']",$form).hide();
    if (schema.properties) {
        var props = schema.properties;
        Object.keys(props).forEach(function(key, index) {
            if (props[key].type == "object") {
                appendObjectFormFields($form_content, key, props[key]);
            }
            else {
                appendInputFormField($form_content, key, props[key], schema.required.includes(key));
            }
            
        });
    }
    return $form;
}
/**
 * Private class used by {@link #createFormFromSchema}
 *
 * @param {jQuery} container - The form container
 * @param {string} The name of the input field
 * @param {Object} object_schema - a JSON schema object ({@link http://json-schema.org/}) 
 * which is utlized to append properties of the input
 * @param {boolean} required- If it is a mandatory field or not.
**/
function appendInputFormField($container, name, object_schema, required) {
    var input_id = name;
    var prompt = object_schema.title;
    var desc = object_schema.description;
    

    $input = $('<input type="text" class="form-control"></input>');
    $input.addClass("editable");
    $input.attr('name',name);
    $input.attr('id',input_id);
    $label_for = $('<label></label>');
    $label_for.attr("for",input_id);
    $label_for.text(prompt);

    $container.append($label_for);
    $container.append($input);
    
    if(desc){
        $input.attr('placeholder', desc);
    }
    if(required){
        $input.prop('required',true);
        $label = $("label[for='"+$input.attr('id')+"']");
        $label.append("*");
    }    
}
/**
 * Private class used by {@link #createFormFromSchema}. Appends a subform to append
 * input
 *
 * @param {jQuery} $container - The form container
 * @param {string} The name of the input field
 * @param {Object} object_schema - a JSON schema object ({@link http://json-schema.org/}) 
 * which is utlized to append properties of the input
 * @param {boolean} required- If it is a mandatory field or not.
**/
function appendObjectFormFields($container, name, object_schema) {
    $div = $('<div class="subform form-group"></div>');
    $div.attr("id", name);
    Object.keys(object_schema.properties).forEach(function(key, index) {
        if (object_schema.properties[key].type == "object") {
            // only one nested level allowed
            // therefore do nothing            
        }
        else {
            appendInputFormField($div, key, object_schema.properties[key], false);
        }
    });
    $container.append($div);
}

/**
 * Populate a form with the content in the param <i>data</i>.
 * Each data parameter is going to fill one <input> field. The name of each parameter
 * is the <input> name attribute while the parameter value attribute represents 
 * the <input> value. All parameters are by default assigned as 
 * <i>readonly</i>.
 * 
 * NOTE: All buttons in the form are hidden. After executing this method adequate
 *       buttons should be shown using $(#button_name).show()
 *
 * @param {jQuery} $form - The form to be filled in
 * @param {Object} data - An associative array formatted using Mason format ({@link https://tools.ietf.org/html/draft-kelly-json-hal-07})
**/

function fillFormWithMasonData($form, data) {
    
    console.log(data);
    
    $(".form_content", $form).children("input").each(function() {
        if (data[this.id]) {
            $(this).attr("value", data[this.id]);
        }
    });
    
    $(".form_content", $form).children(".subform").children("input").each(function() {
        var parent = $(this).parent()[0];
        if (data[parent.id][this.id]) {
            $(this).attr("value", data[parent.id][this.id]);
        }
    });
}

/**
 * Serialize the input values from a given form (jQuery instance) into a
 * JSON document.
 * 
 * @param {Object} $form - a jQuery instance of the form to be serailized
 * @returs {Object} An associative array in which each form <input> is converted
 * into an element in the dictionary. 
**/
function serializeFormTemplate($form){
    var envelope={};
    // get all the inputs into an array.
    var $inputs = $form.find(".form_content input");
    $inputs.each(function() {
        envelope[this.id] = $(this).val();
    });
    
    var subforms = $form.find(".form_content .subform");
    subforms.each(function() {
        
        var data = {}
        
        $(this).children("input").each(function() {
            data[this.id] = $(this).val();
        });
        
        envelope[this.id] = data
    });
    return envelope;
}

/**
 * Add a new .message HTML element in the to the #messages_list <div> element.
 * The format of the generated HTML is the following:
 * @example
 *  //<div class='message'>
 *  //        <form action='#'>
 *  //            <div class="commands">
 *  //                <input type="button" class="editButton editMessage" value="Edit"/>
 *  //                <input type="button" class="deleteButton deleteMessage" value="Delete"/>
 *  //             </div>
 *  //             <div class="form_content">
 *  //                <input type=text class="headline">
 *  //                <input type="textarea" class="articlebody">
 *  //             </div>  
 *  //        </form>
 *  //</div>
 *
 * @param {string} url - The url of the created message
 * @param {string} headline - The title of the new message
 * @param {string} articlebody - The body of the crated message. 
**/
function appendMessageToList(url, headline, articlebody) {
        
    var $message = $("<div>").addClass('message').html(""+
                        "<form action='" + url + "' class='container'>"+
                        "   <div class='row'>"+
                        "       <div class='form_content col-md-8'>"+
                        "           <input type='text' class='headline form-control-plaintext font-weight-bold' value='"+headline+"' readonly='readonly'/>"+
                        "           <div class='articlebody form-control-plaintext' readonly='readonly'>"+articlebody+"</div>"+
                        "       </div>"+
                        "       <div class='commands col-md-4'>"+
                        "            <button  class='deleteButton deleteMessage btn' title='Remove message'><span class='fa fa-ban' ></span></button>"+
                        "       </div>" +
                        "   </div>" +
                        "</form>"
                    );
    //Append to list
    $("#messages_list").append($message);
}

/**
 * Helper method to be called before showing new user data information
 * It purges old user's data and hide all buttons in the user's forms (all forms
 * elements inside teh #userData)
 *
**/
function prepareUserDataVisualization() {
    
    //Remove all children from form_content
    $("#userProfile .form_content").empty();
    //Hide buttons
    $("#userData .commands input[type='button'").hide();
    //Reset all input in userData
    $("#userData input[type='text']").val("??");
    //Remove old messages
    $("#messages_list").empty();
    //Be sure that the newUser form is hidden
    $("#newUser").hide();
    //Be sure that user information is shown
    $("#userData").show();
    //Be sure that mainContent is shown
    $("#mainContent").show();
}

/**
 * Helper method to visualize the form to create a new user (#new_user_form)
 * It hides current user information and purge old data still in the form. It 
 * also shows the #createUser button.
**/
function showNewUserForm () {
    //Remove selected users in the sidebar
    deselectUser();

    //Hide the user data, show the newUser div and reset the form
    $("#userData").hide();
    var form =  $("#new_user_form")[0];
    form.reset();
    // Show butons
    $("input[type='button']",form).show();
    
    $("#newUser").show();
    //Be sure that #mainContent is visible.
    $("#mainContent").show();
}

/**
 * Helper method that unselects any user from the #user_list and go back to the
 * initial state by hiding the "#mainContent".
**/
function deselectUser() {
    $("#user_list li.active").removeClass("active");
    $("#mainContent").hide();
}

/**
 * Helper method to reload current user's data by making a new API call
 * Internally it makes click on the href of the active user.
**/
function reloadUserData() {
    var active = $("#user_list li.active a");
    active.click();
}

/**
 * Transform a date given in a UNIX timestamp into a more user friendly string
 * 
 * @param {number} timestamp - UNIX timestamp
 * @returns {string} A string representation of the UNIX timestamp with the 
 * format: 'dd.mm.yyyy at hh:mm:ss'
**/
function getDate(timestamp){
    // create a new javascript Date object based on the timestamp
    // multiplied by 1000 so that the argument is in milliseconds, not seconds
    var date = new Date(timestamp*1000);
    // hours part from the timestamp
    var hours = date.getHours();
    // minutes part from the timestamp
    var minutes = date.getMinutes();
    // seconds part from the timestamp
    var seconds = date.getSeconds();

    var day = date.getDate();

    var month = date.getMonth()+1;

    var year = date.getFullYear();

    // will display time in 10:30:23 format
    return day+"."+month+"."+year+ " at "+ hours + ':' + minutes + ':' + seconds;
}

/** 
 * Transforms an address with the format 'city, country' into a dictionary.
 * @param {string} input - The address to be converted into a dictionary with the
 * format 'city, country'
 * @returns {Object} a dictionary with the following format: 
 * {'object':{'addressLocality':locality, 'addressCountry':country}}
**/
function getAddress(address){
    var _address = address.split(",",2);
    return {'addressLocality':_address[0], 'addressCountry':_address[1]||"??"};

}
/**** END UI HELPERS ****/

/**** BUTTON HANDLERS ****/
/**
 * Uses the API to create authenticate the user with the form attributes in the present form.
 *
 * TRIGGER: #loginUser 
**/
function handleAuthenticateUser(event){
    if (DEBUG) {
        console.log ("Triggered handleAuthenticateUser");
    }
    var $form = $("#loginUser").closest("form");
    var template = serializeFormTemplate($form);
    //var username = $form.attr("username");
    //add_user(url, template);
    get_user(template);
	console.log ("template :"+JSON.stringify(template));
    return false; //Avoid executing the default submit
}



/**
 * Shows in #mainContent the #new_user_form. Internally it calls to {@link #showNewUserForm}
 *
 * TRIGGER: #addUserButton
**/
function handleShowUserForm(event){
    if (DEBUG) {
        console.log ("Triggered handleShowUserForm");
    }
    //Show the form. Note that the form was updated when I apply the user collection
    showNewUserForm();
    return false;
}

/**
 * Uses the API to delete the currently active user.
 *
 * TRIGGER: #deleteUserRestricted 
**/
function handleDeleteUser(event){
    //Extract the url of the resource from the form action attribute.
    if (DEBUG) {
        console.log ("Triggered handleDeleteUser");
    }
	event.preventDefault();
    //var userurl = $(this).closest("form").attr("action");
   	var userurl = $("#deleteUser").closest("form").attr("action");
    console.log ("url :"+userurl);	
    delete_user(userurl);
    return false;

	
	
}

/**
 * Uses the API to update the user's restricted profile with the form attributes in the present form.
 *
 * TRIGGER: #editRestrictedUser 
**/
function handleEditUserRestricted(event){
    //Extract the url of the resource from the form action attribute.
    if (DEBUG) {
        console.log ("Triggered handleDeleteUserRestricted");
    }
	event.preventDefault();
    var $form = $("#editUserRestricted").closest("form");
    var body = serializeFormTemplate($form);
    var user_restricted_url = $("#editUserRestricted").closest("form").attr("action");
    console.log ("url :"+user_restricted_url);
    console.log ("url :"+user_restricted_url);
	edit_user(user_restricted_url, body);
    return false;
}

/**
 * Uses the API to create a new user with the form attributes in the present form.
 *
 * TRIGGER: #createUser 
**/
function handleCreateUser(event){
    if (DEBUG) {
        console.log ("Triggered handleCreateUser");
    }
    //var $form = $(this).closest("form");
	//var userURL=$(event.target).attr("href");
    var $form = $("#createUser").closest("form");
    var template = serializeFormTemplate($form);
    var url = $form.attr("action");
    add_user(url, template);
	console.log ("url :"+url);
	console.log ("template :"+JSON.stringify(template));
    return false; //Avoid executing the default submit
}
/**
 * Uses the API to retrieve user's information from the clicked user. In addition, 
 * this function modifies the active user in the #user_list (removes the .active
 * class from the old user and add it to the current user)
 *
 * TRIGGER: click on #user_list li a 
**/
function handleGetUser(event) {
    if (DEBUG) {
        console.log ("Triggered handleGetUser");
    }
    //TODO 2
    // This event is triggered by an #user_list li a element. Hence, $(this)
    // is the <a> that the user has pressed. $(this).parent() is the li element
    // containing such anchor.
    //
    // Use the method event.preventDefault() in order to avoid default action
    // for anchor links.
    //
    // Remove the class "active" from the previous #user_list li element and
    // add it to the current #user_list li element. Remember, the current
    // #user_list li element is $(this).parent()
    //
    // Purge the forms by calling the function prepareUserDataVisualization()
    // 
    // Finally extract the href attribute from the current anchor ($(this))
    // and call the function get_user(url) to make the corresponding 
    // HTTP call to the RESTful API. You can extract an HTML attribute using the
    // attr("attribute_name") method from JQuery.
    
	event.preventDefault();
	
	$("#user_list").children().removeClass('active');
	$(event.target).parent().addClass("active");
	//$(this).$("#trying").parent().addClass("active");
    var userURL=$(event.target).attr("href");
	console.log ('user address : '+userURL);
	prepareUserDataVisualization();
	get_user(userURL);
    return;
}


/**
 * logout
 *
 * TRIGGER: click on #logot li a 
**/
function handleLogout(event) {
    if (DEBUG) {
        console.log ("___________________________________");
        console.log ("Triggered handleLogout");
	}
    
	event.preventDefault();
	$.cookie("loggedin", "no"); 
	location.reload();			
	
    return;
}


/**
 * Uses the API to delete the associated message
 *
 * TRIGGER: .deleteMessage
**/
function handleDeleteMessage(event){
    if (DEBUG) {
        console.log ("Triggered handleDeleteMessage");
    }
    //TODO 2:
    //  Extract the url of the resource to be deleted from the form action attribute.
    //  Call the method delete_message(messageurl).
    //  Check handleDeleteUser for more hints.
    //  Remember to return false in order to avoid default action
    
	event.preventDefault();
	
	var msgurl = $(".deleteMessage").closest("form").attr("action");
    console.log ('url : '+msgurl);
	delete_message(msgurl);
	
	
	
	return ;
}

/**** END BUTTON HANDLERS ****/

/*** START ON LOAD ***/
//This method is executed when the webpage is loaded.
$(function(){

    //TODO 1: Add corresponding click handler to all HTML buttons
    // The handlers are:
    // #addUserButton -> handleShowUserForm
    // #deleteUser -> handleDeleteUser
    // #editUserRestricted -> handleEditUserRestricted
    // #createUser -> handleCreateUser
    //
    // Check http://api.jquery.com/on/ for more help.
    
	$("#addUserButton").click(function() {
		console.log( "addUserButton click handled");
		handleShowUserForm();
	});
	
	$("#deleteUser").click(function(event) {
		console.log( "deleteUser click handled");
		handleDeleteUser(event);
	});
	
	$("#editUser ").click(function(event) {
		console.log( "editUser  click handled");
		handleEditUserRestricted(event);
	});
	
	$("#editUserRestricted").click(function(event) {
		console.log( "editUserRestricted click handled");
		handleEditUserRestricted(event);
	});
		
	$("#deleteUserRestricted ").click(function() {
		console.log( "deleteUserRestricted click handled");
		handleDeleteUserRestricted();
	});
	
	$("#createUser").click(function() {
		console.log( "createUser click handled");
		handleCreateUser();
	});

	$("#loginUser").click(function() {
		console.log( "user authentication starting!");
		handleAuthenticateUser();
	});


	$("#messages_list").on( "click", ".deleteMessage", function(event) {//delegated
		console.log( "deleteMessage delegated event handler ");
		handleDeleteMessage(event);
	});
	  
    $("#user_list").on( "click", "li a", function(event) {
		console.log( "user_list delegated event handler");
		handleGetUser(event);
	});

	$("#logoutBtn").on( "click", "li a", function(event) {
		console.log( "logout delegated event handler");
		handleLogout(event);
	});

	getUserChoices(ENTRYPOINT+'nadiro/choices');
    //getUsers(ENTRYPOINT);
	//getLoginForm();
	
});
/*** END ON LOAD**/