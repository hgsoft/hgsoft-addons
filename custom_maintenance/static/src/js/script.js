var list = $('.custom_kanban_state_h1 div a')

for (i = 0; i < list.length; i++) {
    $(list[i]).click(SyncAllColors)
    $(list[i]).change(SyncAllColors)
}

function SyncAllColors() {
    
    var list = $('.custom_kanban_state_h1 div a')

    for (i = 0; i < list.length; i++) {
	var title = list[i].title.trim().toLocaleLowerCase()
	var text = list[i].text.trim().toLocaleLowerCase()
	var value = title.length > 0 ? title : text;

        if (value == 'máquina energizada mas parada') {
            $(list[i]).find( "span" )[0].className = 'o_status badge-cm-red'
            
        } else if (value == 'preparação 1') {
            $(list[i]).find( "span" )[0].className = 'o_status badge-cm-dark_orange'
            
        } else if (value == 'preparação 2') {
            $(list[i]).find( "span" )[0].className = 'o_status badge-cm-orange'
            
        } else if (value == 'preparação 3') {
            $(list[i]).find( "span" )[0].className = 'o_status badge-cm-light_orange'
            
        } else if (value == 'máquina pronta') {
            $(list[i]).find( "span" )[0].className = 'o_status badge-cm-yellow'
            
        } else if (value == 'máquina sendo operada manualmente') {
            $(list[i]).find( "span" )[0].className = 'o_status badge-cm-dark_blue'
            
        } else if (value == 'máquina trabalhando sem repetibilidade') {
            $(list[i]).find( "span" )[0].className = 'o_status badge-cm-blue'
            
        } else if (value == 'máquina trabalhando com repetibilidade') {
            $(list[i]).find( "span" )[0].className = 'o_status badge-cm-light_blue'
            
        } else if (value == 'máquina produzindo com repetibilidade') {
            $(list[i]).find( "span" )[0].className = 'o_status badge-cm-dark_green'
            
        } else if (value == 'máquina produzindo com repetibilidade e qualidade') {
            $(list[i]).find( "span" )[0].className = 'o_status badge-cm-light_green'
            
        } else  {
            $(list[i]).find( "span" )[0].className = 'o_status badge-cm-transparent'
            
        }
    }
}


