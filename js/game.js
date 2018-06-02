var Game = {
    canvas: undefined,
    context: undefined,
    state: undefined,
    user: undefined,
    conn: undefined,
};

var opponent = null;

var SCREEN_WIDTH = undefined;
var SCREEN_HEIGHT = undefined;
var FPS = 1000/60;
var LOBBY_TITLE = "Alpha Lobby";

function User(handle, _id) {
    this._id = _id;
    this.handle = handle;
    this.state = "LOBBY_IDLE";
    this.deck = null;
}

function Conn() {
    this.ws = new WebSocket("ws://localhost:9001/");
    this.ws.onmessage = handle_ws;
    this.response = null;
}

Game.start = function() {
    Game.init();

    Game.canvas = document.getElementById("game");
    Game.context = Game.canvas.getContext("2d");
    SCREEN_WIDTH = Game.canvas.width;
    SCREEN_HEIGHT = Game.canvas.height;
    Game.context.fillStyle = "#FFFFFF";
    Game.context.fillRect(0, 0, Game.canvas.width, Game.canvas.height);

    //Game.draw_text();

    Game.canvas.addEventListener("mousedown", Game.handle_click);
    Game.main_loop();
};

document.addEventListener("DOMContentLoaded", Game.start);

Game.init = function() {
    _id = null;
    //handle = prompt("Please enter your handle");
    handle = "User_1"

    Game.conn = new Conn();

    Game.user = new User(handle, _id);

    Game.state = "LOBBY";  
}

Game.draw_text = function(text, color, x, y) {
    var text_length = text.width;
    Game.context.fillStyle = color;
    Game.context.font = "bold 16px Arial, sans-serif";
    Game.context.fillText(text,
                          //((SCREEN_WIDTH / 2) - (text_length / 2)),
                          x,
                          y);

};

Game.draw_ready_button = function(player, offset=0) {
    var x = 518;
    var y = 102 + offset;
    var w = 100;
    var h = 58;
    var ty = 136 + offset;
    var tx = 0;
    var text = "";
    var text_color = "#0000FF";

    if (player.state == "LOBBY_IDLE") {
        var text = "WAITING...";
        var text_color = "#FFFFFF";
        var tx = 530;
    }

    if (player.state == "LOBBY_READY") {
        var color = "#FF0000";
        var text = "READY?";
        var text_color = "#FFFFFF";
        var tx = 535;
    }

    if (player.state == "LOBBY_STANDBY") {
        var color = "#00FF00";
        var text = "STAND BY...";
        var text_color = "#000000";
        var tx = 522;   
    }

    Game.context.fillStyle = color;
    Game.context.fillRect(x, y, w, h);
    Game.draw_text(text, text_color, tx, ty);
}

Game.clear_canvas = function() {
    Game.context.clearRect(0,
                           0,
                           Game.canvas.width,
                           Game.canvas.height);
}

Game.draw_bg = function() {
    Game.context.fillStyle = "#FFFFFF";
    Game.context.fillRect(0, 0, Game.canvas.width, Game.canvas.height);
}

Game.draw_user_row = function(user, offset) {
    var border = 2;
    var x = 20;
    var y = 100 + offset;
    var w = SCREEN_WIDTH;
    var h = 60;
    Game.context.fillStyle = "#000000";
    Game.context.fillRect(x, y, w-(border * x), h+border);
    Game.context.fillStyle = "#FFFFFF";
    Game.context.fillRect(x+border, y+border, w-(border * x)-border*2, h-border);
    Game.draw_text(user, "#000000", x + 10, y + 40);
}

Game.handle_click = function(e) {
    var rect = Game.canvas.getBoundingClientRect();
    var p = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    };
    var message = "Mouse position: " + p.x + "," + p.y;
    //console.log(message);


    var x = 518;
    var y = 102;
    var w = 100;
    var h = 58;
    if ( (p.x >= x && p.x <= x + w) &&
         (p.y >= y && p.y <= y + h) &&
         opponent ) {
        if (Game.user.state == "LOBBY_READY") {
            standby_for_match();
        }
        else if (Game.user.state == "LOBBY_STANDBY") {
            waiting_for_match();
        }
    }
}

Game.draw_lobby = function() {
    //Game.draw_text();
    var user_text = Game.user.handle + " " + Game.user._id;
    var opponent_text = "";

    Game.draw_text(LOBBY_TITLE, "#000000", 20, 20);
    Game.draw_user_row(user_text, 0);
    
    if (opponent) {
        opponent_text = opponent.handle + " " + opponent._id;
    }
    
    Game.draw_user_row(opponent_text, 100);

    if (opponent) {
        Game.draw_ready_button(opponent, 100);
    }
    Game.draw_ready_button(Game.user);
}

Game.draw_room = function() {
    //Game.draw_text();
    var x = 500;
    var y = 300;
    var w = 40;
    var h = 60;
    user_text = Game.user.handle + " " + Game.user._id;

    if (opponent) {
        opponent_text = opponent.handle + " " + opponent._id;
    }

    Game.draw_text(user_text + " vs " + opponent_text, "#000000", 20, 20);

    Game.context.fillStyle = "#000000";
    Game.context.fillRect(x, y, w, h);
}

function waiting_for_match() {
    px = {
        "command": "user_waiting",
    }

    Game.user.state = "LOBBY_READY";
    Game.conn.ws.send(JSON.stringify(px));
}

function ready_for_match() {
    px = {
        "command": "user_ready",
    }

    Game.conn.ws.send(JSON.stringify(px));
}

function standby_for_match() {
    px = {
        "command": "user_standby",
    }

    Game.user.state = "LOBBY_STANDBY";
    Game.conn.ws.send(JSON.stringify(px));
}

Game.update = function() {
    Game.clear_canvas();
    Game.draw_bg();

    switch(Game.state) {
        case "LOBBY":
            Game.draw_lobby();
            break;
        case "MATCH":
            Game.draw_room();
            break;
    }
}

Game.main_loop = function() {
    Game.update();
    //Game.draw();
    window.setTimeout(Game.main_loop, FPS);
}

function get_users() {
    px = {
        command: "get_users",
    };
    Game.conn.ws.send(JSON.stringify(px));
}

function handle_ws(e) {
    msg = JSON.parse(e.data)
    switch(msg.type) {
        case "init":
            Game.user._id = msg.data._id;
            if (msg.data.users) {
                opponent = new User("Opponent",
                                    msg.data.users[0]);
                Game.user.state = "LOBBY_READY";
            }
            break;
        case "get_users":
            break;
        case "error":
            console.log(msg.data)
            break;
        case "player_join":
            opponent = new User("Opponent",
                                msg.data._id);
            Game.user.state = "LOBBY_READY";
            break;
        case "player_leave":
            opponent = null;
            Game.user.state = "LOBBY_IDLE";
            Game.state = "LOBBY";
            break;
        case "opponent_waiting":
            if (opponent) {
                opponent.state = "LOBBY_IDLE";
            }
            break;
        case "opponent_standby":
            if (opponent) {
                opponent.state = "LOBBY_STANDBY";
            }
            break;
        case "room_ready":
            console.log(msg.data)
            Game.user.deck = msg.data.deck;
            Game.state = "MATCH";
            break;
    }
};
