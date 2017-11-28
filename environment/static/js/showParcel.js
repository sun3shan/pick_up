

function Parcel(option){
	this._init(option);
}

Parcel.prototype = {
	_init:function(option){
		this.imgSrc = option.imgSrc;
		//canvas上显示的宽度和高度
		this.w = 650;
		this.h = 612;
		this.pos = option.pos;
		this.value = option.value;
	},
	//画图
	render:function(ctx, mapSize){
		var img = new Image();
		img.src = this.imgSrc;
		var that = this;
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
	},
	//包裹价值减1
	decValue:function(ctx, mapSize){
		if(this.value == 0){
			ctx.clearRect(that.pos.X * ctx.canvas.height/mapSize + 1,
					that.pos.Y * ctx.canvas.width/mapSize + 1,
					ctx.canvas.height/mapSize - 2,
					ctx.canvas.width/mapSize - 2);
			this.destroy();
		}
	}
}