


function Courier(option){
	this._init(option);
}

Courier.prototype = {
	_init:function(option){
		this.imgSrc=option.imgSrc;
        // //canvas上显示的款宽度和高度
        // this.w = 40;
        // this.h = 65;
        //裁剪后的宽高
        this.w0 = 40;
        this.h0 = 65;
  
        this.dirIndex = option.direction;
        this.speed = option.speed||10;
        this.pos = option.pos;
        this.step = 0;
        this.score = 0;
	},  
    //画图  
    render:function(ctx, mapSize){  
        var img=new Image();  
        img.src=this.imgSrc;  
        var that=this;  
        img.onload=function(){  
            var i=0;  
            setInterval(function(){  
                ctx.clearRect(that.pos.X * ctx.canvas.height/mapSize+1,
                            that.pos.Y * ctx.canvas.width/mapSize+1,
                            ctx.canvas.height/mapSize-2,
                            ctx.canvas.width/mapSize-2);//ctx就是传递过来的上下文  
                // ctx.canvas.width=ctx.canvas.width;  
                ctx.drawImage(  
                img,  
                that.w0*i,  
                that.h0*that.dirIndex,  
                that.w0,  
                that.h0,  
                that.pos.X * ctx.canvas.height/mapSize+1,  
                that.pos.Y * ctx.canvas.width/mapSize+1,  
                ctx.canvas.height/mapSize-2,  
                ctx.canvas.width/mapSize-4  
                );  
                i++;  
                i=i%4;  
            },1000/that.speed);
        }  
    },
    changeDirectionAndGoForward:function(dir){  
        if(dir=='left'){  
            this.dirIndex=1;
            this.step += 1;
            this.pos.X = this.pos.X==0?this.pos.X:this.pos.X - 1;
            ctx.clearRect((that.pos.X + 1) * ctx.canvas.height/mapSize+1,
                        that.pos.Y * ctx.canvas.width/mapSize+1,
                        ctx.canvas.height/mapSize-2,
                        ctx.canvas.width/mapSize-2);

        }else if(dir=='right'){  
            this.dirIndex=2;  
            this.step += 1;
            this.pos.X = this.pos.X==9?this.pos.X:this.pos.X + 1;
            ctx.clearRect((that.pos.X - 1) * ctx.canvas.height/mapSize+1,
                        that.pos.Y * ctx.canvas.width/mapSize+1,
                        ctx.canvas.height/mapSize-2,
                        ctx.canvas.width/mapSize-2);
        }  
        else if(dir=='up'){  
            this.dirIndex=3;
            this.step += 1;
            this.pos.Y = this.pos.Y==0?this.pos.Y:this.pos.Y - 1;
            ctx.clearRect(that.pos.X * ctx.canvas.height/mapSize+1,
                        (that.pos.Y + 1) * ctx.canvas.width/mapSize+1,
                        ctx.canvas.height/mapSize-2,
                        ctx.canvas.width/mapSize-2);
        }else{  
            this.dirIndex=0;
            this.step += 1;
            this.pos.Y = this.pos.Y==9?this.pos.Y:this.pos.Y + 1;
            ctx.clearRect(that.pos.X * ctx.canvas.height/mapSize+1,
                        (that.pos.Y - 1) * ctx.canvas.width/mapSize+1,
                        ctx.canvas.height/mapSize-2,
                        ctx.canvas.width/mapSize-2);
        }  
    }
}