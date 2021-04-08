document.addEventListener("DOMContentLoaded", function (){
    tinymce.init({
        selector:'textarea',
        plugins: 'image',
        language: 'pt_BR',
        image_title: true,
        automatic_uploads: true,
        images_upload_url: "/upl",
        file_picker_types: 'image',
        relative_urls: false,
        file_picker_callback: function (cb, value, meta) {
                var input = document.createElement('input');
                input.setAttribute('type', 'file');
                input.setAttribute('accept', 'image/*');

                input.onchange = function () {
                    var file = this.files[0];

                    var reader = new FileReader();

                    reader.onload = function () {
                        var id = 'blobid' + (new Date()).getTime();
                        var blobCache =  tinymce.activeEditor.editorUpload.blobCache;
                        var base64 = reader.result.split(',')[1];
                        var blobInfo = blobCache.create(id, file, base64);
                        blobCache.add(blobInfo);

                        cb(blobInfo.blobUri(), { title: file.name });
                    };
                    reader.readAsDataURL(file);
                };
                input.click();
            }
    });

    /*Código para previw do upload da thumb*/
    try{
        const thumb = document.getElementById("thumb");
        const thumbPreview = document.getElementById("thumb-preview");

        thumb.onchange = function () {
            var reader = new FileReader();

            reader.onload = function (e) {
                // get loaded data and render thumbnail.
                thumbPreview.src = e.target.result;
            };

            // read the image file as a data URL.
            reader.readAsDataURL(this.files[0]);
        };
    }catch(err){}
});