
function Position(option){
	this._init(option);
}

Position.prototype = {
	_init:function(option){
		this.X = option.X;
		this.Y = option.Y;
	},

	set:function(x, y){
		this.X = x;
		this.Y = y;
	}
}