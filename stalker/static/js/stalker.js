/**
 * Created with PyCharm.
 * User: eoyilmaz
 * Date: 5/29/12
 * Time: 5:49 PM
 * To change this template use File | Settings | File Templates.
 */


require(["dijit/registry", "dijit/Dialog"],
    function(registry, Dialog){
        create_create_project_dialog = function (){
            // create the dialog
            return new Dialog({
                id: 'create_project_dialog',
                title: 'Create Project',
                href: '/create/project',
                resize: true,
                style: "width: 380px; height 360px;"
            });
        };
        
        create_create_image_format_dialog = function(){
            return new Dialog({
                id: 'create_image_format_dialog',
                title: 'Create Image Format',
                href: '/create/image_format',
                resize: true,
                style: "width: 380; height 360px;"
            })
        };
    }
)

