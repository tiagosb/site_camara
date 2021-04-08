class Favo 
{
    constructor(args) 
    {
        if(! 'object' == typeof args)
            throw `Erro: args deve ser do tipo object e não ${typeof args}.`;
        
        if(! Object.keys(args).includes('selector'))
            throw `Erro: informe a chave selector com o seletor do slider.`;

        this.$favoSlider = document.querySelector(`${args.selector}`);

        if(! this.$favoSlider)
            throw `Erro: não foi possível selecionar o elemento com o seletor ${args.selector}.`;
        
        this.$favoSlides = this.$favoSlider.querySelectorAll(`.slide`);
        this.current = 0;
        this.slidesToShow = 1;
        this.slidesToScroll = 1;
        this.dotsEnabled = false;
        this.arrowsEnabled = true;
        this.autoRunEnabled = false;
        this.time = 2000;
        this.size = {
            height: 200,
        }
        this._config(args);
    }

    _validate_sizing_unit(unit) {
        //medida em pixels
        const px = /(\d+)(px)/.exec(unit);
        if(px)    
            return px;
        
        //medida em porcentagem
        const pc = /(\d+)(%)/.exec(unit);
        if(pc)
            return pc;

        console.warn(`Erro: width/height inválidos. As medidas devem ser em porcentagem ou pixel.\n Os valores padrão serão usados.`);
        return false;
    }

    _resize(args)
    {
        
        if(Object.keys(args).includes('width'))
        {
            const width = this._validate_sizing_unit(args.width);
            if(width)
                this.$favoSlider.style.width = width[0];
        }

        if(Object.keys(args).includes('height'))
        {
            const height = this._validate_sizing_unit(args.height);
            if(height)
                this.$favoSlider.style.height = height[0];
        }
        
        this.size.width = this.$favoSlider.clientWidth;
        this.size.height = this.$favoSlider.clientHeight;

        window.addEventListener("resize", () => {

            this.size.width = this.$favoSlider.clientWidth;
            this.size.height = this.$favoSlider.clientHeight;

            this.$favoSlides.forEach($slide => {
                $slide.style.width = (this.size.width / this.slidesToShow) + 'px';
                $slide.style.height = this.size.height + 'px';   
            });


            if(this.current > 0)
                this._updateDotActive((this.size.width / this.slidesToShow) * this.current);
            else 
                this._updateDotActive(0);
        });
    }
    

    _updateWraperPosition(left)
    {
        if(left > 0)
            left = left * -1;
        
        if(left > 0)
            return;

        this.$favoSliderfavoWraper.style.left = left + 'px';
    }

    _config(args)
    {   
        this.$favoSlider.classList.add("__favo-slider");
        this.$favoSlider.style.width = '100%';
        this.$favoSlider.style.height = this.size.height + 'px';
        this.size.width = this.$favoSlider.clientWidth;
        
        this._resize(args);
        
        this.$favoSliderfavoWraper = document.createElement("div");
        this.$favoSliderfavoWraper.classList.add("__favo-wraper");
        this._updateWraperPosition(0);

        if(Object.keys(args).includes('slidesToShow'))
        {
            if('number' == typeof args.slidesToShow)
                this.slidesToShow = args.slidesToShow;
            else
                console.warn(`slidesToShow deve ser do tipo number e não ${typeof args.slidesToShow}.`);
        }

        if(Object.keys(args).includes('slidesToScroll'))
        {   
            if('number' == typeof args.slidesToScroll)
                this.slidesToScroll = args.slidesToScroll;
            else
                console.warn(`slidesToScroll deve ser do tipo number e não ${typeof args.slidesToScroll}.`);
        }

        this.$favoSlides.forEach($slide => {
            
            const $img = $slide.querySelector("img");

            if($img)
                $slide.style.backgroundImage = `url(${$img.src})`;

            $slide.style.width = (this.size.width / this.slidesToShow) + 'px';
            $slide.style.height = this.size.height + 'px';
            this._touchConfig($slide);
            this.$favoSliderfavoWraper.appendChild($slide);
        });
        
        this.$favoSlider.appendChild(this.$favoSliderfavoWraper);

        if(Object.keys(args).includes('dotsEnabled'))
        {
            if('boolean' == typeof args.dotsEnabled)
                this.dotsEnabled = args.dotsEnabled;
            else 
                console.warn(`dotsEnabled deve ser do tipo boolean e não ${typeof args.dotsEnabled}.`);
        }

        if(this.dotsEnabled == true)
            this.enableDots();

        if(Object.keys(args).includes('arrowsEnabled'))
        {
            if('boolean' == typeof args.arrowsEnabled)
                this.arrowsEnabled = args.arrowsEnabled;
            else 
                console.warn(`arrowsEnabled deve ser boolean e não ${typeof args.arrowsEnabled}.`);
        }

        if(this.arrowsEnabled == true)
            this.enableArrows();

       
        if(Object.keys(args).includes('autoRunEnabled'))
        {
            if('boolean' == typeof args.autoRunEnabled)
            {
                this.autoRunEnabled = args.autoRunEnabled;
                
                if(Object.keys(args).includes('time'))
                {
                    if('number' == typeof args.time)
                        this.time = args.time;
                    else 
                        console.warn(`time dever ser numero e não ${args.time}`);
                }
            }
            else 
                console.warn(`autoRunEnabled deve ser boolean e não ${typeof args.autoRunEnabled}`);
        }

        if(this.autoRunEnabled == true)
            this.autoRun();
    }

    _updateDotActive()
    {
        const dotActive = this.$favoSlider.querySelector(".dot-active");
        const dotCurrent = this.$favoSlider.querySelector(`.d${this.current}`);
        
        if(dotActive)
            dotActive.classList.remove("dot-active");

        if(dotCurrent)
            dotCurrent.classList.add("dot-active");
    }

    _touchConfig($slide)
    {
        $slide.addEventListener("touchstart", event => {

            if(this.autoRunEnabled)
                clearInterval(this.mainloop);

            this.touchStart = event.changedTouches[0].clientX;
            this.$favoSliderfavoWraper.classList.add("__favo-no-transition");
        });

        $slide.addEventListener("touchend", event => {

            const left = this.current * (this.size.width / this.slidesToShow);
            const sensibility = (this.size.width / this.slidesToShow) / 5;
            const maxLeft = (this.$favoSlides.length-this.slidesToShow) * (this.size.width / this.slidesToShow);

            if(this.autoRunEnabled)
                this.autoRun();
                
            this.$favoSliderfavoWraper.classList.remove("__favo-no-transition");
            
            let touchEnd = event.changedTouches[0].clientX 
            
            if(touchEnd < 0) 
                touchEnd = touchEnd * -1;
            
            if(this.touchStart < 0) 
                this.touchStart = this.touchStart * -1;

            if(touchEnd > this.size.width)
                return;
        
            if(this.touchStart > touchEnd) 
            {
                if( ((this.touchStart - touchEnd) + left) > maxLeft) 
                    return;
                
                if(this.touchStart - touchEnd >= sensibility)
                    this.next();
                else 
                    this._updateWraperPosition(left);
            } 
            else 
            {
                if(left - (touchEnd - this.touchStart) < 0) 
                    return;
                if(touchEnd - this.touchStart >= sensibility)
                    this.prev()
                else
                    this._updateWraperPosition(left);
            }
        });

        $slide.addEventListener("touchmove", event => {

            const maxLeft = (this.$favoSlides.length-this.slidesToShow) * (this.size.width / this.slidesToShow);
            let touchPoint = event.changedTouches[0].clientX;
            let move = this.touchStart - touchPoint;
            let left = this.current * (this.size.width / this.slidesToShow);
            
            if(touchPoint < 0 || this.touchStart < 0 || this.current == 0 && move < 0 || touchPoint > this.size.width || left + move > maxLeft) 
                return;

            if(move > 0)
                left = left + move;
            else
                left = left - (move * -1);

            this._updateWraperPosition(left);
        });
    }

    next()
    {
        const maxLeft = (this.$favoSlides.length-this.slidesToShow) * (this.size.width / this.slidesToShow);
        const slideWidth = this.size.width / this.slidesToShow;
        
        this.current = this.current + this.slidesToScroll;
        let left = (this.current * slideWidth);

        if(left > maxLeft)
        {
            left = maxLeft;
            this.current = this.$favoSlides.length-1;
        }

        this._updateWraperPosition(left);
        this._updateDotActive();
    }  

    prev()
    {
        const slideWidth = this.size.width / this.slidesToShow;

        this.current = this.current - this.slidesToScroll;
        let left = (this.current * slideWidth);
        
        if(left < 0)
        {
            this.current = 0;
            left = 0;
        }

        this._updateWraperPosition(left);
        this._updateDotActive();    
    }

    //refatorar - repetição de código desnecessária
    enableArrows()
    {
        const nextBtn = document.createElement("input");
        const prevBtn = document.createElement("input");
        const arrowsContainer = document.createElement("nav");

        nextBtn.type = "button";
        nextBtn.value = "Next";
        nextBtn.classList.add("next");

        nextBtn.addEventListener("click", () => {

            if(this.autoRunEnabled)
                clearInterval(this.mainloop);

            this.next();

            if(this.autoRunEnabled)
                this.autoRun();
        });

        prevBtn.type = "button";
        prevBtn.value = "Prev";
        prevBtn.classList.add("prev");

        prevBtn.addEventListener("click", () => {

            if(this.autoRunEnabled)
                clearInterval(this.mainloop);

            this.prev();

            if(this.autoRunEnabled)
                this.autoRun();
        });

        arrowsContainer.classList.add("arrows-container");
        arrowsContainer.appendChild(prevBtn);
        arrowsContainer.appendChild(nextBtn);
        this.$favoSlider.appendChild(arrowsContainer);  
    }


    goTo(targetIndex)
    {
        const maxLeft = (this.$favoSlides.length - this.slidesToShow) * (this.size.width / this.slidesToShow);
        const target = parseInt(targetIndex);
        const slideWidth = this.size.width / this.slidesToShow;
        let left = target * (this.slidesToScroll * slideWidth);
        
        this.current = target;

        if(left > maxLeft)
            left = maxLeft; 

        this._updateWraperPosition(left);
        this._updateDotActive();
    }
    
    enableDots()
    {
        const $dotsContainer = document.createElement("nav");
        $dotsContainer.classList.add("dots-container");

        for(let index = 0; index < this.$favoSlides.length; index++)
        {
            const $slideDot = document.createElement("input");
            $slideDot.type = "button";
            $slideDot.value = index;
            $slideDot.classList.add("slide-dot");
            $slideDot.classList.add(`d${index}`);

            $slideDot.addEventListener("click", event => {
                if(this.autoRunEnabled)
                    clearInterval(this.mainloop);
                
                this.goTo(event.target.value);
                
                if(this.autoRunEnabled)
                    this.autoRun();
            });

            $dotsContainer.appendChild($slideDot);
        }

        $dotsContainer.firstChild.classList.add("dot-active");
        this.$favoSlider.appendChild($dotsContainer);
    }

    autoRun()
    {
        this.mainloop = setInterval(() => {
            if(this.current == this.$favoSlides.length-1)
                this.goTo(0);
            else
                this.next();
        }, this.time);
    }
}
