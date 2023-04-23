const fileInput = document.getElementById('fileInput');
const textArea = document.getElementById('ves');

fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    const reader = new FileReader();
    
    reader.addEventListener('load', () => {
        textArea.value = reader.result;
    });
    
    reader.readAsText(file);
    });


    
document.getElementById("tlacitko").addEventListener("click", obrazok)

// var imageUrl = document.getElementById("adresaObrazka").value;

// document.getElementById("ves").addEventListener("keyup", obrazok)

function obrazok(){
    let data = document.getElementById("ves").value;
    // console.log(data);
    let w = window.innerWidth / 3;
    
    $.ajax({
        type: "POST",
        url: "/",
        data: {"data": data, "w": w},
        success: function(response) {
            let [sprava,image_base64, boo] = response;
            document.getElementById("messages").innerHTML = sprava;
            if (boo){
                var dalej;
                var img = new Image();
                img.onload = function(){
                    var canvas = document.getElementById("myCanvas");
                    if(canvas){
                        dalej =false;
                        document.getElementById("myCanvas").remove();
                        var canvas = document.createElement("canvas");
                        canvas.id = "myCanvas";
                        var skuska = document.getElementById("skuska");
                        skuska.appendChild(canvas);
                    }else {
                        dalej = true;
                        var skuska = document.createElement("div");
                        skuska.id = "skuska";
                        document.body.appendChild(skuska);

                        var canvas = document.createElement("canvas");
                        canvas.id = "myCanvas";
                        
                        skuska.appendChild(canvas);
                        let blob = document.getElementById("blob");
                        blob.replaceWith(skuska);
                    };
                    var canvas = document.getElementById("myCanvas");
                    var ctx = canvas.getContext("2d");
                    let w = img.width;
                    let h = img.height;
                    canvas.width = w ;
                    canvas.height = h;
                    const skuskaa = document.getElementById("skuska");
                    skuskaa.style.width = `${w}px`;
                    skuskaa.style.height = `${h}px`;

                    ctx.drawImage(img,0,0);
                    konecna(img, dalej, imageUrl);
                }
                // img.src = imageUrl;
                var imageUrl = `data:image/png;base64,${image_base64}`;
                document.getElementById("adresaObrazka").value = imageUrl;
                img.src = imageUrl;
                
            };
            // konecna(boo);
            
        }
    });
};

function konecna(img, dalej, imageUrl){
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");
    var skuska = document.getElementById("skuska");
   
    if (!dalej) return;
    img.onload = function() {
        let panel = document.createElement("span");
        panel.id = "panel";
        panel.innerHTML = "<button id='pero'>Pero </button>";
        panel.innerHTML += "<button id='guma'>Guma </button>";
        panel.innerHTML += "<button id='ulozit' style='float: right;'>Ulozit </button>";
        
        
        panel.style.transform = "translate(0px,-40px)";
        panel.style.transitionDuration = "1s";
        
        skuska.appendChild(panel);
        panel = document.getElementById("panel");
        
        skuska.addEventListener("mouseover", a1);
        skuska.addEventListener("mouseout", a2);
        
        let panel2 = document.createElement("span");
        panel2.id = "panel2";
        panel2.innerHTML += "<button id='filter'>Filtre </button>";
        panel2.innerHTML += "<button id='filterVlastny'>Vlastny filter </button>";
        skuska.appendChild(panel2);
        panel2= document.getElementById("panel2");
        panel2.style.transform = "translate(0px,40px)";
        panel2.style.transitionDuration = "1s";
        skuska.addEventListener("mouseover", a12);
        skuska.addEventListener("mouseout", a22);
        
        

        function pero(){
            var canvas = document.getElementById("myCanvas");
            var ctx = canvas.getContext("2d");
            var imageUrl = document.getElementById("adresaObrazka").value
            panel.style.transitionDuration = "0s";
            panel.style.visibility = "hidden";
            panel.style.transform = "translate(0px,-40px)";
            panel2.style.transitionDuration = "0s";
            panel2.style.visibility = "hidden";
            panel2.style.transform = "translate(0px,40px)";
            canvas.style.cursor = "crosshair";
            document.getElementById("filter").style.visibility ="hidden";
            

            let farba = document.createElement("input");
            farba.type = "color";
            farba.id = "colorpicker";
            farba.value = "#ff0000";
            skuska.style.overflow = "visible";
            skuska.appendChild(farba);
            var farbapera = "#000000";
            var hrubka = 2;

            let menu = document.createElement("select");
            menu.id = "menu"
            menu.name = "ciara";
            skuska.appendChild(menu);
            
            let option1 = document.createElement("option");
            option1.value = "2";
            option1.innerHTML = "___";
            option1.style.fontSize = "1rem";
            let option2 = document.createElement("option");
            option2.value = "5";
            option2.innerHTML = "___";
            option2.style.fontSize = "1.5rem";
            let option3 = document.createElement("option");
            option3.value = "10";
            option3.innerHTML = "___";
            option3.style.fontSize = "2rem";
            menu = document.getElementById("menu")
            menu.appendChild(option1);
            menu.appendChild(option2);
            menu.appendChild(option3);

            let zrusit = document.createElement("button");
            zrusit.innerHTML = "Zrusit";
            zrusit.id = "zrusit";
            skuska.appendChild(zrusit);
            zrusit = document.getElementById("zrusit");
            zrusit.addEventListener("click", vratitPanel);


            

            menu.addEventListener("change", function(e){
                hrubka = menu.value;
            })
            document.getElementById("colorpicker").addEventListener("change", function(e){
                farbapera = e.target.value;
            })
            
            
            
            skuska.removeEventListener("mouseover", a1);
            skuska.removeEventListener("mouseout", a2);
            const platno = document.getElementById("myCanvas");
            let drawing = false;
            
            let lastX ;
            let lastY ;
            
            
            platno.addEventListener("mousedown", kreslit1)

            platno.addEventListener("mousemove", kreslit2)

            platno.addEventListener("mouseup", kreslit3)

            function kreslit1(e){
                drawing = true;
                let x = e.offsetX;
                let y = e.offsetY;
                lastX = x;
                lastY = y; 
            };
            function kreslit2(e){
                if (!drawing) return;
                x = e.offsetX;
                y = e.offsetY;
                drawLine(lastX, lastY, x,y, farbapera, hrubka)
                lastX = x;
                lastY = y;
            };
            function kreslit3(e){
                drawing = false;
            };
            
            function vratitPanel(e){
                canvas.style.cursor = "default";
                menu.remove()
                zrusit.remove()
                farba.remove()
                panel.style.transitionDuration = "1s";
                panel.style.visibility = "visible";
                panel2.style.transitionDuration = "1s";
                panel2.style.visibility = "visible";
                skuska.addEventListener("mouseover", a1);
                skuska.addEventListener("mouseout", a2);
                skuska.style.overflow = "hidden";
                document.getElementById("filter").style.visibility ="visible";
                platno.removeEventListener("mousedown", kreslit1)
                platno.removeEventListener("mousemove", kreslit2)
                platno.removeEventListener("mouseup", kreslit3)
            }

        function drawLine(x,y,x2,y2,farba, hrubka){
            ctx.beginPath();
            ctx.lineWidth = hrubka;
            ctx.strokeStyle = farba;
            
            ctx.moveTo(x,y);
            ctx.lineTo(x2,y2);
            ctx.stroke();
            
        }

        };
        
        function a1(){
            panel.style.transform = "translate(0)";
            document.getElementById("pero").addEventListener("click", pero);
            document.getElementById("guma").addEventListener("click", guma);
            document.getElementById("ulozit").addEventListener("click", ulozit);
        };
        
        function a2(){
            panel.style.transform = "translate(0px,-40px)";
        };
        
        function guma(){
            // toto gumovanie je napicu zrobene, treba zohladnit ten cas kym sa nacita obarzok(pozri jak som to zrobil pri filtroch)
            //je tu chyba ze negumuje s filtrom ked das, asi preto hore co som pisal
            var canvas = document.getElementById("myCanvas");
            var ctx = canvas.getContext("2d");
            var imageUrl = document.getElementById("adresaObrazka").value;
            document.getElementById("filter").style.visibility ="hidden";
            panel2.style.transitionDuration = "0s";
            panel2.style.visibility = "hidden";
            panel2.style.transform = "translate(0px,40px)";
            skuska.style.overflow = "visible";
            let zmazatVsetko = document.createElement("button");
            zmazatVsetko.id = "zmazatvsetko";
            zmazatVsetko.innerHTML = "Zmazat vsetko";
            skuska.appendChild(zmazatVsetko);
            zmazatVsetko = document.getElementById("zmazatvsetko")
            zmazatVsetko.addEventListener("click", zmazat)

            let menu = document.createElement("select");
            menu.id = "menu"
            menu.name = "ciara";
            skuska.appendChild(menu);
            
            let option1 = document.createElement("option");
            option1.value = "1";
            option1.innerHTML = "___";
            option1.style.fontSize = "1rem";
            let option2 = document.createElement("option");
            option2.value = "5";
            option2.innerHTML = "___";
            option2.style.fontSize = "1.5rem";
            let option3 = document.createElement("option");
            option3.value = "8";
            option3.innerHTML = "___";
            option3.style.fontSize = "2rem";
            menu = document.getElementById("menu")
            menu.appendChild(option1);
            menu.appendChild(option2);
            menu.appendChild(option3);

            let zrusit = document.createElement("button");
            zrusit.innerHTML = "Zrusit";
            zrusit.id = "zrusit";
            skuska.appendChild(zrusit);
            zrusit = document.getElementById("zrusit");
            zrusit.addEventListener("click", vratitPanel);

            panel.style.transitionDuration = "0s";
            panel.style.visibility = "hidden";
            panel.style.transform = "translate(0px,-40px)";
            const platno = document.getElementById("myCanvas");
            const predloha = document.createElement("canvas");
            let ctx2 = predloha.getContext("2d");
            predloha.width = canvas.width;
            predloha.height = canvas.height;
            let imgPredloha = new Image();
            imgPredloha.src = imageUrl;
            
            ctx2.drawImage(img, 0, 0);
            let OriginalImageData = ctx2.getImageData(0, 0, predloha.width, predloha.height);
            let OrigialPixelData = OriginalImageData.data;
            //upraveny obrazok
            var imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            // var imageData = canvas.toDataURL();
            const pixelData = imageData.data;
            var gumovanie = false;
            platno.addEventListener("mousedown", gumovanie1);
            platno.addEventListener("mousemove", gumovanie2);
            platno.addEventListener("mouseup", gumovanie3);

            function gumovanie1(e){
                drawing = false;
                gumovanie = true;
            };
            function gumovanie2(e){
                if (!gumovanie) return;
                
                x = e.offsetX;
                y = e.offsetY;
                var startX = x;
                var startY = y;
                var pixelIndex;
                var red;
                var green;
                var blue;
                var alpha;
                var k = menu.value 

                for(var i= startX-(k>>1); i<= startX+ (k >> 1);i++){
                    x = i;
                    for(var j=startY- (k>>1); j<=startY+ (k >> 1);j++){
                        y = j;
                        pixelIndex = (y * canvas.width + x) * 4;
                        red = OrigialPixelData[pixelIndex];
                        green = OrigialPixelData[pixelIndex + 1];
                        blue = OrigialPixelData[pixelIndex + 2];
                        alpha = OrigialPixelData[pixelIndex + 3];

                        imageData.data[pixelIndex] = red;
                        imageData.data[pixelIndex+1] = green;
                        imageData.data[pixelIndex+2] = blue;
                        imageData.data[pixelIndex+3] = alpha;
                        
                        ctx.putImageData(imageData, 0, 0);
                    }
                    
                    y = e.offsetY;
                    
                }

                
            };
            function gumovanie3(e){
                gumovanie = false;
            };
            
            function zmazat(){
                ctx.drawImage(imgPredloha, 0,0);
            }

            function vratitPanel(){
                zrusit.remove();
                menu.remove();
                zmazatVsetko.remove();
                panel.style.transitionDuration = "1s";
                panel.style.visibility = "visible";
                panel2.style.transitionDuration = "1s";
                panel2.style.visibility = "visible";
                skuska.addEventListener("mouseover", a1);
                skuska.addEventListener("mouseout", a2);
                skuska.style.overflow = "hidden";
                document.getElementById("filter").style.visibility ="visible";
                platno.removeEventListener("mousedown", gumovanie1);
                platno.removeEventListener("mousemove", gumovanie2);
                platno.removeEventListener("mouseup", gumovanie3);
                
            }
        };
    
        function ulozit(){
            var imageUrl = document.getElementById("adresaObrazka").value;
            var canvas = document.getElementById("myCanvas");
            var ctx = canvas.getContext("2d");
            var panel = document.getElementById("panel");
            var panel2= document.getElementById("panel2");
            document.getElementById("filter").style.visibility ="hidden";
            panel.style.transitionDuration = "0s";
            panel.style.visibility = "hidden";
            panel.style.transform = "translate(0px,-40px)";
            panel2.style.transitionDuration = "0s";
            panel2.style.visibility = "hidden";
            panel2.style.transform = "translate(0px,40px)";
            
            let menu = document.createElement("select");
            menu.id = "menu"
            menu.name = "format";
            var format = "jpg";
            skuska.appendChild(menu);
            skuska.style.overflow ="visible";
            
            let option1 = document.createElement("option");
            option1.value = "jpg";
            option1.innerHTML = "jpg";
            option1.style.fontSize = "1rem";
            let option2 = document.createElement("option");
            option2.value = "png";
            option2.innerHTML = "png";
            option2.style.fontSize = "1rem";
            let option3 = document.createElement("option");
            option3.value = "pdf";
            option3.innerHTML = "pdf";
            option3.style.fontSize = "1rem";
            let option4 = document.createElement("option");
            option4.value = "gif";
            option4.innerHTML = "gif";
            option4.style.fontSize = "1rem";
            let option5 = document.createElement("option");
            option5.value = "webp";
            option5.innerHTML = "webp";
            option5.style.fontSize = "1rem";
            let option6 = document.createElement("option");
            option6.value = "bmp";
            option6.innerHTML = "bmp";
            option6.style.fontSize = "1rem";
            menu = document.getElementById("menu");
            menu.appendChild(option1);
            menu.appendChild(option2);
            menu.appendChild(option3);
            menu.appendChild(option4);
            menu.appendChild(option5);
            menu.appendChild(option6);

            
            menu.addEventListener("change", function(e){
                format = menu.value;
                ulozitBTN.download = `canvas.${format}`;
            })
            

            let ulozitBTN = document.createElement("a");
            ulozitBTN.innerHTML = "ULOZIT";
            ulozitBTN.href = canvas.toDataURL(imageUrl);
            
            ulozitBTN.download = `canvas.${format}`;
            skuska.appendChild(ulozitBTN);
            let zrusit = document.createElement("button");
            zrusit.innerHTML = "Zrusit";
            zrusit.id = "zrusit";
            skuska.appendChild(zrusit);
            zrusit = document.getElementById("zrusit");
            zrusit.addEventListener("click", vratitPanel);
            // ulozitBTN.click()
            function vratitPanel(){
                zrusit.remove();
                menu.remove();
                ulozitBTN.remove()
                skuska.style.overflow = "hidden";
                panel.style.transitionDuration = "1s";
                panel.style.visibility = "visible";
                panel2.style.transitionDuration = "1s";
                panel2.style.visibility = "visible";
                document.getElementById("filter").style.visibility ="visible";

            
            }

        
        }
            
        
        function a12(){
                panel2.style.transform = "translate(0)";
                document.getElementById("filter").addEventListener("click", zobrazitFiltre);
                document.getElementById("filterVlastny").addEventListener("click", filterVlastny);
            };
        function a22(){
            panel2.style.transform = "translate(0px,40px)";
        };
        
        function zobrazitFiltre(){
            var canvas = document.getElementById("myCanvas");
            var ctx = canvas.getContext("2d");
            var imageUrl = document.getElementById("adresaObrazka").value;
            let zrusit = document.createElement("button");
            zrusit.innerHTML = "Zrusit";
            zrusit.id = "zrusit";
            skuska.appendChild(zrusit);
            document.getElementById("zrusit").addEventListener("click", vratitPanel);
            skuska.style.overflow = "visible";
            panel.style.transitionDuration = "0s";
            panel.style.visibility = "hidden";
            panel.style.transform = "translate(0px,-40px)";
            skuska.removeEventListener("mouseover", a12);
            skuska.removeEventListener("mouseout", a22);
            document.getElementById("filter").style.visibility ="hidden";
            
            // panel2.style.height = "100px";
            let filtre = [];


            function pridatFilter(id, filtr){
                panel2.innerHTML += `<canvas id='${id}' class="filtreVsetky" width="100" height="100">  </canvas>`;
                filtre.push(id);
                let img1 = new Image();
                // img1.src = imageUrl;
                
                img1.onload = function() {
                    let filter1 = document.getElementById(id);
                    
                    filter1.style.borderStyle = "solid";
                    filter1.style.borderWidth = "1px";
                    filter1.style.borderColor = "black";
                    filter1.style.zIndex = "2";
                    
                    filter1.width = 100;
                    filter1.height = 100;
                    let ctx1 = filter1.getContext("2d");
                    ctx1.filter = filtr;
                    ctx1.drawImage(img1, 0, 0, 100, 100);
                    filter1.addEventListener("click", function(){
                        zmenitFilter(filtr);
                    });
                };
                img1.src = imageUrl;
            }

            pridatFilter("filter1", "blur(5px)");
            pridatFilter("filter2",  "contrast(1.4) sepia(1) drop-shadow(-9px 9px 3px #e81)");
            pridatFilter("filter3", "contrast(500%)");
            pridatFilter("filter4", "drop-shadow(16px 16px 20px red) invert(75%)");
            pridatFilter("filter5", "hue-rotate(90deg)");
            pridatFilter("filter6", "invert(100%) saturate(150%) contrast(125%)");
            pridatFilter("filter7", "drop-shadow(5px 5px 5px rgba(0, 0, 0, 0.5)) sepia(50%)");
            pridatFilter("filter8", "invert(100%) brightness(150%)");

            function zmenitFilter(filtr){
                const dataURL = canvas.toDataURL();
                const imgFromCanvas = new Image();
                imgFromCanvas.onload = function(){
                    ctx.filter = filtr;
                    ctx.drawImage(imgFromCanvas, 0, 0);
                    vratitPanel();
                }
                imgFromCanvas.src = dataURL;
            }
                
            function vratitPanel(){
                panel.style.visibility = "visible";
                
                document.getElementById("filter").style.visibility ="visible";
                zrusit.remove();
                panel.style.transitionDuration = "1s";
                panel.style.visibility = "visible";
                panel2.style.transitionDuration = "1s";
                panel2.style.visibility = "visible";
                skuska.addEventListener("mouseover", a1);
                skuska.addEventListener("mouseout", a2);
                skuska.addEventListener("mouseover", a12);
                skuska.addEventListener("mouseout", a22);
                skuska.style.overflow = "hidden";
                for(var i=0; i<filtre.length;i++){
                    document.getElementById(filtre[i]).remove()
                }
            }
            

        }

        function filterVlastny(){
            var canvas = document.getElementById("myCanvas");
            var ctx = canvas.getContext("2d");
            var imageUrl = document.getElementById("adresaObrazka").value;
            let container = document.createElement("div");
            container.id = "container";
            skuska.appendChild(container);
            let zrusit = document.createElement("button");
            zrusit.innerHTML = "Zrusit";
            zrusit.id = "zrusit";
            
            zrusit.style.display = "block";

            skuska.appendChild(zrusit);
            document.getElementById("zrusit").addEventListener("click", vratitPanel);
            skuska.style.overflow = "visible";
            panel.style.transitionDuration = "0s";
            panel.style.visibility = "hidden";
            panel.style.transform = "translate(0px,-40px)";
            panel2.style.transform = "translate(0px,40px)";
            panel2.style.visibility = "hidden";
            panel2.style.transitionDuration = "0s";
            document.getElementById("filter").style.visibility ="hidden";

            let currentImage = img;
            let slidery = [];

            vytvorSlider("brightness","brightness", "0", "200", "100");
            vytvorSlider("contrast","contrast", "0", "200", "100");
            vytvorSlider("grayscale","grayscale", "0", "100", "0");
            vytvorSlider("invert","invert", "0", "100", "0");
            vytvorSlider("saturate","saturation" ,"0", "200", "100");
            vytvorSlider("sepia","sepia", "0", "100", "0");
            
            function vytvorSlider(id,meno, min, max, value, l){
                let slider1 = document.createElement("input");
                slider1.class = "slider";
                slider1.id = id;
                slider1.type = "range";
                slider1.min = min;
                slider1.max = max;
                slider1.value = value;
                slidery.push(slider1);
                let label = document.createElement("div");
                label.innerHTML = `${meno}(${value})` ;
                label.style.color= "white";
                container.appendChild(label);
                container.appendChild(slider1);

                slider1.addEventListener("input", function(){
                    aplikovatFilter(slider1 ,label);
                } );
            }

            function aplikovatFilter(slider, label){
                const imgFromCanvas = new Image();
                
                imgFromCanvas.onload = function(){
                    let docasna = "";
                    
                    for(var i=0; i<slidery.length; i++){
                        docasna += ` ${slidery[i].id}(${slidery[i].value}%) `;
                    }
                    
                    ctx.filter = docasna;
                    ctx.drawImage(imgFromCanvas, 0, 0);
                    
                    label.innerHTML = `${slider.id}(${slider.value})`;
                }
                imgFromCanvas.src = imageUrl;
            }

            function vratitPanel(){
                panel.style.visibility = "visible";
                
                document.getElementById("filter").style.visibility ="visible";
                zrusit.remove();
                panel.style.transitionDuration = "1s";
                panel.style.visibility = "visible";
                panel2.style.transitionDuration = "1s";
                panel2.style.visibility = "visible";
                skuska.addEventListener("mouseover", a1);
                skuska.addEventListener("mouseout", a2);
                skuska.addEventListener("mouseover", a12);
                skuska.addEventListener("mouseout", a22);
                skuska.style.overflow = "hidden";
                container.remove();
                
            }

        }
    };

    img.src = imageUrl;
}
// aaa