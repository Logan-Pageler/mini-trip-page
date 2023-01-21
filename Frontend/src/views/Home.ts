

export default function Upload() {
    var el = <HTMLInputElement>document.createElement("INPUT");
    el.type = "file";
    el.accept = ".csv";
  
    // (cancel will not trigger 'change')
    el.addEventListener('change', function(ev2) {
        // access el.files[] to do something with it (test its length!)
        
        // add first image, if available
        if (el.files!.length) {
            (<HTMLEmbedElement>document.getElementById('filedata'))!.src = URL.createObjectURL(el.files![0]);
            
            console.log(el.files![0].text());
        }


        // test some async handling
        new Promise(function(resolve) {
            setTimeout(function() { console.log(el.files); resolve(null); }, 1000);
        })
        .then(function() {
        // clear / free reference
            el.remove();
        });

    });

    el.click(); // open
}


