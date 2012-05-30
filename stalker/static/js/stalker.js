/**
 * Created with PyCharm.
 * User: eoyilmaz
 * Date: 5/29/12
 * Time: 5:49 PM
 * To change this template use File | Settings | File Templates.
 */



function create_create_project_dialog(){
    
//    parent_element == parent_element || document;
    
    // create the dialog
    return new Jx.Dialog({
        id: 'create_project_dialog',
        label: 'Create Project',
        modal: true,
        contentURL: '/create/project',
        resize: false,
        width: 680,
        height: 360,
        maximize: false,
        useKeyboard: true,
        limit: document,
        destroyOnClose: true
    });
}

function create_create_image_format_dialog(){
    
    // create the dialog
    return new Jx.Dialog({
        id: 'create_image_format_dialog',
        label: 'Create Image Format',
        modal: true,
        contentURL: '/create/image_format',
        resize: false,
        width: 680,
        height: 360,
        maximize: false,
        useKeyboard: true,
        limit: document,
        destroyOnClose: true
    });
}

