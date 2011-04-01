var FileBrowserDialogue = {
    
    init : function () {},
    
    fileSubmit : function (FileURL) {
        var URL = FileURL;
        var win = tinyMCEPopup.getWindowArg("window");
        
        // insert information now
        win.document.getElementById(tinyMCEPopup.getWindowArg("input")).value = URL;
        
        // change width/height & show preview
        if (win.ImageDialog){
            if (win.ImageDialog.getImageData)
                win.ImageDialog.getImageData();
            if (win.ImageDialog.showPreviewImage)
                win.ImageDialog.showPreviewImage(URL);
        }
        
        // close popup window
        tinyMCEPopup.close();
    }
}

tinyMCEPopup.onInit.add(FileBrowserDialogue.init, FileBrowserDialogue);