function html_unescape(text) {
    // Unescape a string that was escaped using django.utils.html.escape.
    text = text.replace(/&lt;/g, '<');
    text = text.replace(/&gt;/g, '>');
    text = text.replace(/&quot;/g, '"');
    text = text.replace(/&#39;/g, "'");
    text = text.replace(/&amp;/g, '&');
    return text;
}

function id_to_windowname(text) {
    text = text.replace(/\./g, '__dot__');
    text = text.replace(/\-/g, '__dash__');
    return text;
}

function windowname_to_id(text) {
    text = text.replace(/__dot__/g, '.');
    text = text.replace(/__dash__/g, '-');
    return text;
}

function dismissRelatedLookupPopup(win, chosenId) {
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
        elem.value += ',' + chosenId;
    } else {
        document.getElementById(name).value = chosenId;
    }
    win.close();
}

function dismissAddAnotherPopup(win, newId, newRepr) {
    newId = html_unescape(newId);
    newRepr = html_unescape(newRepr);
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem) {
        if (elem.nodeName == 'SELECT') {
            var o = new Option(newRepr, newId);
            elem.options[elem.options.length] = o;
            o.selected = true;
        } else if (elem.nodeName == 'INPUT') {
            if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
                elem.value += ',' + newId;
            } else {
                elem.value = newId;
            }
        }
    } else {
        var toId = name + "_to";
        elem = document.getElementById(toId);
        var o = new Option(newRepr, newId);
        SelectBox.add_to_cache(toId, o);
        SelectBox.redisplay(toId);
    }
    win.close();
}

$(document).ready(function(){
    $('a.related-lookup').click(function(){
        var name = this.id.replace(/^lookup_/, '');
        name = id_to_windowname(name);
        var href;
        if (this.href.search(/\?/) >= 0) {
            href = this.href + '&pop=1';
        } else {
            href = this.href + '?pop=1';
        }
        var win = window.open(
            href, name, 'height=500,width=850,resizable=yes,scrollbars=yes');
        win.focus();
        return false;
    });
    $('a.add-another').click(function(){
        var name = this.id.replace(/^add_/, '');
        name = id_to_windowname(name);
        var href = this.href;
        if (this.href.indexOf('?') == -1) {
            href += '?_popup=1';
        } else {
            href  += '&_popup=1';
        }
        var win = window.open(href, name, 'height=500,width=850,resizable=yes,scrollbars=yes');
        win.focus();
        return false;
    });
});