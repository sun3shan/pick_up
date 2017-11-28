

function Barrier(option){
	this._init(option);
}

Barrier.prototype = {
	_init:function(option){
		this.imgSrc = option.imgSrc;
		this.w = 128;
		this.h = 128;
		this.pos = option.pos;
	},
	// 画图
	render:function(ctx, mapSize){
		var img = new Image();
		img.src = this.imgSrc;
		var that = this
		img.onload = function(){
			ctx.clearRect(that.pos.X * ctx.canvas.height/mapSize + 1,
						that.pos.Y * ctx.canvas.width/mapSize + 1,
						ctx.canvas.height/mapSize - 2,
						ctx.canvas.width/mapSize - 2);
			ctx.drawImage(img, 0, 0, that.w, that.h,
					 that.pos.X * ctx.canvas.height/mapSize + 1, 
					 that.pos.Y * ctx.canvas.width/mapSize + 1, 
					 ctx.canvas.height/mapSize - 2,
					 ctx.canvas.width/mapSize - 2);
		}
	}
}