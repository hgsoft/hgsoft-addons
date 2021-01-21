odoo.define('custom_maintenance.my_js', function (require) {"use strict";

    console.log('[LOG GERAL] - [Iniciando o módulo JavaScript]')
    
    var rpc = require('web.rpc');
    
    console.log('[LOG GERAL] - [require(wep.rpc)]')

    if (location.toString().includes('model=maintenance.equipment') && location.toString().includes('view_type=kanban')) {
        console.log('[LOG GERAL] - [Chamando a função run()]')
        run()
        console.log('[LOG GERAL] - [Função run() concluida]')
    }
    
    async function run() {
        console.log('[LOG RUN] - [Iniciando a função run()]')
        rpc.query({
            model: 'maintenance.equipment',
            method: 'get_setting',
        }).then(function(data){
            console.log('[LOG RUN] - [Iniciando a função run()]')
            console.log('[LOG RUN] - [data]')
            console.log(data)
            refresh_page_in(data.refresh_time_seconds)
            console.log('[LOG RUN] - [Finalizando a função run()]')
        });
    }

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function refresh_page_in(refresh_time_seconds) {
        if (refresh_time_seconds > 0) {
            await sleep(refresh_time_seconds*1000);
            location.reload();
        }
    }
});
